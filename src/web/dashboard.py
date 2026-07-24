from typing import Any

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from libRunning import (RouteModel, get_routes, get_dashboard, DashboardModel, get_sections, get_aggregations,
                        get_dashboard_sections, get_dashboard_aggregations)

from src.model.dashboard import Dashboard, get_cell

router = APIRouter(prefix = "/dashboard")
templates = Jinja2Templates(directory="src/templates")


def _create_section_and_aggregation_data(sections: list[str], aggregations: list[str],
                                         default_sections: list[str], default_aggregations:list[str]
                                         ) -> list[dict[str, Any]]:
    count_: int = max(len(sections), len(aggregations))
    items: list[dict[str, Any]] = []
    for index in range(count_):
        item = {}
        try:
            section = sections[index]
        except IndexError:
            section = ""
        item["section"] = section
        item["section_selected"] = section in default_sections
        try:
            aggregation = aggregations[index]
        except IndexError:
            aggregation = ""
        item["aggregation"] = aggregation
        item["aggregation_selected"] = aggregation in default_aggregations
        items.append(item)
    return items

@router.get("", response_class=HTMLResponse)
def show_dashboard_form(request: Request, route: str) -> Any:
    routes: list[RouteModel] = get_routes()
    route_obj: RouteModel = RouteModel(name=route, description="")
    routes_list = [{"name": route.name, "description": route.description} for route in routes]
    sections = sorted(get_sections(route_obj), key=lambda x: int(x.split(".")[0]))
    aggregations = get_aggregations(route_obj)
    default_sections = get_dashboard_sections(route_obj)
    default_aggregations = get_dashboard_aggregations(route_obj)
    items: list[dict[str, Any]] = _create_section_and_aggregation_data(sections, aggregations, default_sections,
                                                                        default_aggregations)

    return templates.TemplateResponse(
        request=request, name="dashboardForm.html", context={"route_name": route, "routes": routes_list,
                                                             "items": items}
    )

@router.post("", response_class=HTMLResponse)
async def run_dashboard(request: Request, route: str) -> Any:
    form = await request.form()
    sections: list[str] = []
    aggregations: list[str] = []
    for (k, v) in form.items():
        if k.startswith("chks_"):
            sections.append(v)
        elif k.startswith("chka_"):
            aggregations.append(v)
    routes: list[RouteModel] = get_routes()
    route_obj: RouteModel = RouteModel(name=route, description="")
    routes_list = [{"name": route.name, "description": route.description} for route in routes]
    dashboard_obj: DashboardModel = get_dashboard(route_obj, sections=sections, aggregations=aggregations)

    return templates.TemplateResponse(
        request=request, name="dashboard.html", context={"dashboard": Dashboard.create_instance(dashboard_obj), "route_name": route,
                                                         "routes": routes_list, "get_cell": get_cell}
    )