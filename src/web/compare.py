from collections import defaultdict
from http.client import HTTPException
from typing import Any

from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.requests import Request

from libRunning import get_routes, RouteModel, get_compare, CompareModel, get_dates

from src.model.compare import Difference, CompareObj
from src.model.training import Training

router = APIRouter(prefix = "/compare")
templates = Jinja2Templates(directory="src/templates")

def get_months_items(dates: list[str]) -> dict[str, list[str]]:
    output = defaultdict(list)
    for date in dates:
        output[date[:7]].append(date)
    return output

def get_max_items(months_items: dict[str, list[str]]) -> int:
    return max(len(items) for items in months_items.values())

def create_objects_for_template(dates: list[str]) -> dict[str, Any]:
    months_items = get_months_items(dates)
    rows = get_max_items(months_items)
    rows_list = list(range(1,rows+1))
    data: dict[tuple[str, int], str] = {}
    for month, values in months_items.items():
        values = sorted(values)
        for row in rows_list:
            index = row - 1
            try:
                value = values[index]
            except IndexError:
                value = ""
            data[(month, row)] = value

    return {
        "months": sorted(list(months_items.keys())),
        "rows": rows_list,
        "data": data,
    }


@router.get("", response_class=HTMLResponse)
def show_compare_form(request: Request, route: str) -> Any:
    routes: list[RouteModel] = get_routes()
    route_obj: RouteModel = RouteModel(name=route, description="")
    routes_list = [{"name": route.name, "description": route.description} for route in routes]
    dates_obj = get_dates(route_obj)
    dates = dates_obj.dates
    data_for_template: dict[str, Any] = create_objects_for_template(dates)

    return templates.TemplateResponse(
        request=request, name="compareForm.html",
        context={"route_name": route, "routes": routes_list, "months": data_for_template["months"],
                 "rows": data_for_template["rows"], "data": data_for_template["data"]},
    )

@router.post("", response_class=HTMLResponse)
async def run_compare(request: Request, route: str) -> Any:
    form = await request.form()
    dates: list[str] = []
    for (k, v) in form.items():
        if k.startswith("chk_"):
            dates.append(v)
    if len(dates) != 2:
        raise ValueError(f"For compare must be selected just 2 dates.")

    date_1: str = dates[0]
    date_2: str = dates[1]
    routes: list[RouteModel] = get_routes()
    route_obj: RouteModel = RouteModel(name=route, description="")
    routes_list = [{"name": route.name, "description": route.description} for route in routes]
    compare_obj: CompareModel = get_compare(route_obj, date_1, date_2)
    training_1 = Training.convert(compare_obj.data_1)
    training_2 = Training.convert(compare_obj.data_2)
    difference: Difference = Difference(training_1=training_1, training_2=training_2)
    compare_wrapped: CompareObj = difference.calculate()
    return templates.TemplateResponse(
        request=request, name="compare.html",
        context={"route_name": route, "routes": routes_list, "compare": compare_wrapped}
    )