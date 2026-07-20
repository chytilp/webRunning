from typing import Any

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from libRunning import get_date, RouteModel, get_routes, TrainingModel, get_dates, TrainingsModel
from src.model.training import Training
from src.model.trainings import Trainings

router = APIRouter(prefix = "/date")
templates = Jinja2Templates(directory="src/templates")
@router.get("/{date}", response_class=HTMLResponse)
def show_date(request: Request, date: str, route: str) -> Any:
    routes: list[RouteModel] = get_routes()
    route_obj: RouteModel = RouteModel(name=route, description="")
    routes_list = [{"name": route.name, "description": route.description} for route in routes]
    date_page: TrainingModel = get_date(route_obj, date)
    training = Training.convert(date_page)
    return templates.TemplateResponse(
        request=request, name="training.html", context={"date": date, "route_name": route, "routes": routes_list,
                                                       "training": training}
    )


@router.get("", response_class=HTMLResponse)
def show_dates(request: Request, route: str) -> Any:
    routes: list[RouteModel] = get_routes()
    route_obj: RouteModel = RouteModel(name=route, description="")
    routes_list = [{"name": route.name, "description": route.description} for route in routes]
    dates_page: TrainingsModel = get_dates(route_obj)
    trainings = Trainings(dates=dates_page.dates)
    values = trainings.get_items_history()
    return templates.TemplateResponse(
        request=request, name="trainings.html", context={"route_name": route, "routes": routes_list,
                                                       "trainings": values}
    )
