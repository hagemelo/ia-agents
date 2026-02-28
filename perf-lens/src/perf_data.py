from pydantic import BaseModel

class PerfData(BaseModel):
    data: str
    vazao: float
    latencia: float
    erro: float
    