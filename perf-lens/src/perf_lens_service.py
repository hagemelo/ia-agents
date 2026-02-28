from pathlib import Path
from orchestrator import Orchestrator
from assessment import Assessment


PROJECT_ROOT = Path(__file__).resolve().parent.parent

class PerfLensService:

    async def analyzePerformance(self) -> Assessment:

        self.openFilesToRead()

        message = f"""
            realize a comparação do resultado da bateria de teste com a baseline
             a bateria de teste é: {self.bateriaToAnalyze}
             a baseline deve ser selecionada entre as baterias: {self.history}
        """
        orchestrator = Orchestrator()
        
        result = await orchestrator.run(message)

        return result

    def openFilesToRead(self):

        history_path = PROJECT_ROOT / "recursos" / "history.csv"
        with open(history_path, "r", encoding="utf-8") as history_file:
            self.history = history_file.read()

        bateria_path = PROJECT_ROOT / "recursos" / "bateria-teste-1.csv"
        with open(bateria_path, "r", encoding="utf-8") as bateria_file:
            self.bateriaToAnalyze = bateria_file.read()