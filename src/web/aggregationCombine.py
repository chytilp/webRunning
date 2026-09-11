from typing import Any

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from libRunning import get_routes, RouteModel, get_aggregations

from src.model.dashboard import Cell
from src.model.section import SectionDates
from src.service.cache import AppCache
from src.web.aggregation import prepare_aggregation

router = APIRouter(prefix = "/aggregationCombine")
templates = Jinja2Templates(directory="src/templates")

def get_cell(data: dict[str, SectionDates], row: int, agg_name: str) -> tuple[str, Cell] | None:
    agg_data = data.get(agg_name)
    if len(agg_data.output) - 1 < row:
        return None
    item: tuple[str, Cell] = agg_data.output[row]
    return item


@router.get("", response_class=HTMLResponse)
def show_aggregations_combine_form(request: Request, route: str) -> Any:
    route_obj = RouteModel(name=route, description="")
    routes: list[RouteModel] = get_routes()
    routes_list = [{"name": route.name, "description": route.description} for route in routes]
    aggregations = get_aggregations(route_obj)

    return templates.TemplateResponse(
        request=request, name="aggregationsForm.html",
        context={"route_name": route, "routes": routes_list, "aggregations": aggregations},
    )

@router.post("", response_class=HTMLResponse)
async def run_aggregations_combine(request: Request, route: str) -> Any:
    route_obj = RouteModel(name=route, description="")
    routes = get_routes()
    routes_list = [{"name": route.name, "description": route.description} for route in routes]
    form = await request.form()

    aggregations: list[str] = []
    for (k, v) in form.items():
        if k.startswith("chk_"):
            aggregations.append(v)
    output: dict[str, SectionDates] = {}
    max_items: int = 0
    for aggregation_name in aggregations:
        agg_item = prepare_aggregation(aggregation_name, route_obj)
        if len(agg_item.output) > max_items:
            max_items = len(agg_item.output)
        output[aggregation_name] = agg_item
    # mark from cache
    cache = AppCache(route=route)
    mark: str = cache.get_mark() or ""

    return templates.TemplateResponse(
        request=request, name="aggregationsCombine.html", context={"route_name": route, "routes": routes_list,
                                                                   "aggregation_names": aggregations,
                                                                   "aggregations": output, "mark": mark,
                                                                   "get_cell": get_cell,
                                                                   "max_items": max_items},
    )