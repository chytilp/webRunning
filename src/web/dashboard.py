from typing import Any

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from libRunning import (RouteModel, get_routes, get_dashboard, DashboardModel, get_sections, get_aggregations,
                        get_dashboard_sections, get_dashboard_aggregations)

from src.model.dashboard import Dashboard, get_cell
from src.service.cache import AppCache

router = APIRouter(prefix = "/dashboard")
templates = Jinja2Templates(directory="src/templates")

def _sort_aggregations(aggregations: list[str], default_aggregations: list[str]) -> list[str]:
    # at first take defaults and than rest from aggregations
    output = []
    for default_aggregation in default_aggregations:
        if default_aggregation in aggregations:
            output.append(default_aggregation)
    for aggregation in aggregations:
        if aggregation not in output:
            output.append(aggregation)
    return output


def _create_section_and_aggregation_data(sections: list[str], aggregations: list[str],
                                         default_sections: list[str], default_aggregations:list[str]
                                         ) -> list[dict[str, Any]]:
    count_: int = max(len(sections), len(aggregations))
    items: list[dict[str, Any]] = []
    last: bool = False
    aggregations = _sort_aggregations(aggregations, default_aggregations)

    for index in range(count_):
        if index == count_ - 1:
            last = True

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

        # button disabled
        item["button_up_disabled"] = ""
        item["button_dw_disabled"] = ""
        if index == 0:
            item["button_up_disabled"] = "disabled"
        if last:
            item["button_dw_disabled"] = "disabled"

        # button names
        if item["aggregation"] != "":
            item["button_name_dw"] = f"btn_{aggregation.replace('.', '_')}_d"
            item["button_name_up"] = f"btn_{aggregation.replace('.', '_')}_u"

        items.append(item)
    return items

@router.get("", response_class=HTMLResponse)
def show_dashboard_form(request: Request, route: str) -> Any:
    routes: list[RouteModel] = get_routes()
    route_obj: RouteModel = RouteModel(name=route, description="")
    routes_list = [{"name": route.name, "description": route.description} for route in routes]
    sections = sorted(get_sections(route_obj), key=lambda x: int(x.split(".")[0]))
    aggregations = get_aggregations(route_obj)
    # read sections and aggregations from cache
    cache = AppCache(route=route)
    default_sections = cache.get_default_sections()
    default_aggregations = cache.get_default_aggregations()
    # ---
    if not default_sections:
        default_sections = get_dashboard_sections(route_obj)
    if not default_aggregations:
        default_aggregations = get_dashboard_aggregations(route_obj)
    items: list[dict[str, Any]] = _create_section_and_aggregation_data(sections, aggregations, default_sections,
                                                                        default_aggregations)

    return templates.TemplateResponse(
        request=request, name="dashboardForm.html", context={"route_name": route, "routes": routes_list,
                                                             "items": items, "jquery": True}
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
    # save sections and aggregations to cache
    cache = AppCache(route=route)
    cache.set_default_sections(sections)
    cache.set_default_aggregations(aggregations)
    # ---
    routes: list[RouteModel] = get_routes()
    route_obj: RouteModel = RouteModel(name=route, description="")
    routes_list = [{"name": route.name, "description": route.description} for route in routes]
    dashboard_obj: DashboardModel = get_dashboard(route_obj, sections=sections, aggregations=aggregations)

    return templates.TemplateResponse(
        request=request, name="dashboard.html", context={"dashboard": Dashboard.create_instance(dashboard_obj), "route_name": route,
                                                         "routes": routes_list, "get_cell": get_cell}
    )