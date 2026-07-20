from typing import Any

from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.requests import Request

from libRunning import get_routes, RouteModel, get_compare, CompareModel

from src.model.compare import Difference, CompareObj
from src.model.training import Training

router = APIRouter(prefix = "/compare")
templates = Jinja2Templates(directory="src/templates")


@router.get("", response_class=HTMLResponse)
def show_compare(request: Request, route: str, dates: str) -> Any:
    dates_list = dates.split(",")
    date_1: str = dates_list[0]
    date_2: str = dates_list[1]
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