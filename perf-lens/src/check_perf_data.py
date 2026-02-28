from pydantic import BaseModel
from perf_data import PerfData

class CheckPerfDataOutput(BaseModel):
    is_perf_data_valid: bool
    perf_data: PerfData