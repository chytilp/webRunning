from typing import Any

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from libRunning import get_routes, get_aggregation, RouteModel, SectionsModel, get_aggregation_grades, GradeModel, get_aggregations

from src.model.section import SectionDates
from src.model.grade import Grade

router = APIRouter(prefix = "/aggregation")
templates = Jinja2Templates(directory="src/templates")
@router.get("/{name}", response_class=HTMLResponse)
def show_aggregation(request: Request, name: str, route: str) -> Any:
    route_obj = RouteModel(name=route, description="")
    routes = get_routes()
    routes_list = [{"name": route.name, "description": route.description} for route in routes]
    aggregation: SectionsModel = get_aggregation(route_obj, name)
    aggregation_obj: SectionDates = SectionDates()
    for date, values in aggregation.date_sections.items():
        aggregation_obj.add_date(date, values)
    aggregation_obj.prepare()
    grades: list[GradeModel] = get_aggregation_grades(route_obj, name)
    return templates.TemplateResponse(
        request=request, name="aggregation.html", context={"aggregation_name": name, "route_name": route,
                                                           "routes": routes_list, "aggregation": aggregation_obj,
                                                           "aggregation_grades": Grade.convert(grades)}
    )

@router.get("", response_class=HTMLResponse)
def show_aggregations(request: Request, route: str) -> Any:
    route_obj = RouteModel(name=route, description="")
    routes = get_routes()
    routes_list = [{"name": route.name, "description": route.description} for route in routes]
    aggregations = get_aggregations(route_obj)
    return templates.TemplateResponse(
        request=request, name="aggregations.html", context={"route_name": route, "routes": routes_list,
                                                            "aggregations": aggregations}
    )