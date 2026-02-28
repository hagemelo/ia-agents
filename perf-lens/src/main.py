from fastapi import FastAPI

from health_controller import router as health_router
from perf_lens_controller import router as perf_lens_router

app = FastAPI()


app.include_router(health_router)
app.include_router(perf_lens_router)