from fastapi import APIRouter
from perf_lens_service import PerfLensService
from assessment import Assessment


router = APIRouter(prefix="/perf-lens", tags=["Perf Lens"])

service = PerfLensService()

@router.post("/analyze-performance")
async def analyzePerformance() -> Assessment:
    analise_desempenho = await service.analyzePerformance()

    return analise_desempenho