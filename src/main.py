from fastapi import FastAPI
import uvicorn
from src.web import section, dashboard, aggregation, app_date, compare
from fastapi.staticfiles import StaticFiles
app = FastAPI()
app.mount("/static", StaticFiles(directory="src/static"), name="static")

app.include_router(section.router)
app.include_router(dashboard.router)
app.include_router(aggregation.router)
app.include_router(app_date.router)
app.include_router(compare.router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)