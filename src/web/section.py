from typing import Any

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from libRunning import get_section, RouteModel, get_routes, SectionsModel, get_section_grades, GradeModel, get_sections

from src.model.section import SectionDates
from src.model.grade import Grade
from src.service.cache import AppCache

router = APIRouter(prefix = "/section")
templates = Jinja2Templates(directory="src/templates")
@router.get("/{name}", response_class=HTMLResponse)
def show_section(request: Request, name: str, route: str) -> Any:
    route_obj = RouteModel(name=route, description="")
    routes = get_routes()
    routes_list = [{"name": route.name, "description": route.description} for route in routes]
    section: SectionsModel = get_section(route_obj, name)
    section_obj: SectionDates = SectionDates()
    for date, values in section.date_sections.items():
        section_obj.add_date(date, values)
    section_obj.prepare()
    grades: list[GradeModel] = get_section_grades(route_obj, name)
    # mark from cache
    cache = AppCache(route=route)
    mark: str = cache.get_mark() or ""

    context = {"section_name": name, "route_name": route, "routes": routes_list,
               "section": section_obj, "section_grades": Grade.convert(grades), "mark": mark}

    return templates.TemplateResponse(
        request=request, name="section.html", context=context)

@router.get("", response_class=HTMLResponse)
def show_sections(request: Request, route: str) -> Any:
    route_obj = RouteModel(name=route, description="")
    routes = get_routes()
    routes_list = [{"name": route.name, "description": route.description} for route in routes]
    sections = get_sections(route_obj)
    return templates.TemplateResponse(
        request=request, name="sections.html", context={"route_name": route, "routes": routes_list,
                                                       "sections": sections}
    )