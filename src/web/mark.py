from collections import defaultdict
from http.client import HTTPException
from typing import Any

from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.requests import Request
from fastapi import status

from libRunning import RouteModel, get_routes, get_dates

from src.service.cache import AppCache

router = APIRouter(prefix = "/mark")
templates = Jinja2Templates(directory="src/templates")

@router.get("", response_class=HTMLResponse)
def show_mark_form(request: Request, route: str) -> Any:
    routes: list[RouteModel] = get_routes()
    route_obj: RouteModel = RouteModel(name=route, description="")
    routes_list = [{"name": route.name, "description": route.description} for route in routes]
    dates_obj = get_dates(route_obj)
    dates = dates_obj.dates
    # read mark from cache
    cache = AppCache(route=route)
    mark: str = cache.get_mark() or ""
    # ---

    return templates.TemplateResponse(
        request=request, name="markForm.html",
        context={"route_name": route, "routes": routes_list, "dates": dates, "mark": mark},
    )

@router.post("", response_class=HTMLResponse)
async def run_mark(request: Request, route: str) -> Any:
    form = await request.form()
    send = form.get("btnSend")
    mark = form.get("txtMark")

    if send:
        cache = AppCache(route=route)
        cache.set_mark(mark)
    redirect_url = f"/dashboard?route={route}"
    return RedirectResponse(redirect_url, status_code=status.HTTP_303_SEE_OTHER)