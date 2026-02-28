from pydantic import BaseModel
from perf_data import PerfData

class Assessment(BaseModel):
    assessment: str
    baseline: PerfData
    suiteResult: PerfData
