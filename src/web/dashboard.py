from typing import Any

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from libRunning import RouteModel, get_routes, get_dashboard, DashboardModel

from src.model.dashboard import Dashboard, get_cell

router = APIRouter(prefix = "/dashboard")
templates = Jinja2Templates(directory="src/templates")


@router.get("", response_class=HTMLResponse)
def show_dashboard(request: Request, route: str) -> Any:
    routes: list[RouteModel] = get_routes()
    route_obj: RouteModel = RouteModel(name=route, description="")
    routes_list = [{"name": route.name, "description": route.description} for route in routes]
    dashboard_obj: DashboardModel = get_dashboard(route_obj)

    return templates.TemplateResponse(
        request=request, name="dashboard.html", context={"dashboard": Dashboard.create_instance(dashboard_obj), "route_name": route,
                                                         "routes": routes_list, "get_cell": get_cell}
    )

@router.post("", response_class=HTMLResponse)
def run_dashboard(request: Request, route: str) -> Any:
    routes: list[RouteModel] = get_routes()
    route_obj: RouteModel = RouteModel(name=route, description="")
    routes_list = [{"name": route.name, "description": route.description} for route in routes]
    dashboard_obj: DashboardModel = get_dashboard(route_obj)

    return templates.TemplateResponse(
        request=request, name="dashboard.html", context={"dashboard": Dashboard.create_instance(dashboard_obj), "route_name": route,
                                                         "routes": routes_list, "get_cell": get_cell}
    )