from pathlib import Path

from agents import Agent,Runner, trace, gen_trace_id
from baseline_analyst import BaselineAnalyst
from suite_analyst import SuiteAnalyst
from suite_evaluator import SuiteEvaluator
from dotenv import load_dotenv
from assessment import Assessment

PROJECT_ROOT = Path(__file__).resolve().parent.parent

class Orchestrator:
    def __init__(self):
        self.instrucoes_orchestrator = """
            Você é um orquestrador para realizar o trabalho de comparar o resultado da bateria de teste com as baterias já realizadas.
            você deverá seguir os seguintes passos:
            1 - Repassar a bateriaToAnalyze para o suiteAgent
            2 - Receber o resultado da bateria de teste do suiteAgent
            3 - Receber a baseline da baselineAnalyst
            4 - Repassar a baseline para o suiteEvaluatorAgent
            5 - realizar o handoff para o suiteEvaluatorAgent para comparar o resultado da bateria de teste com a baseline
            6 - Retornar o resultado da comparação para o suiteAgent
        """

    async def run(self, query: str) -> Assessment:
        load_dotenv(override=True)
        trace_id = gen_trace_id()
        print("Starting Orchestrator...")
        with trace("Orchestrator trace {trace_id}", trace_id=trace_id):
            self.openFilesToRead()
            print("Files opened, starting to analyze...")  

            history = self.history
            bateriaToAnalyze = self.bateriaToAnalyze
            baselineAnalyst = BaselineAnalyst()
            baselineAgent = baselineAnalyst.getBaselineAgent(history)

            suiteAnalyst = SuiteAnalyst()
            suiteAgent = suiteAnalyst.getSuiteAgent(bateriaToAnalyze)

            tools = [baselineAgent, suiteAgent]
            print("Tools created...")  

            suiteEvaluator = SuiteEvaluator()
            suiteEvaluatorAgent = suiteEvaluator.getSuiteEvaluatorAgent()

            handoff_tools = [suiteEvaluatorAgent]
            print("Handoff tools created...")  


            orchestratorAgent = Agent(
                name="Orchestrator",
                instructions=self.instrucoes_orchestrator,
                tools=tools,
                handoffs=handoff_tools,
                model="gpt-5-mini",
                output_type=Assessment,
            )
                
            print("Orchestrator agent created...")  

            message = f"""
                realize a comparação do resultado da bateria de teste com a baseline
                {query}
            """
            result = await Runner.run(orchestratorAgent, message)

            print("Orchestrator agent executed...")
        
            return result.final_output   

    def openFilesToRead(self):

        history_path = PROJECT_ROOT / "recursos" / "history.csv"
        with open(history_path, "r", encoding="utf-8") as history_file:
            self.history = history_file.read()

        bateria_path = PROJECT_ROOT / "recursos" / "bateria-teste-1.csv"
        with open(bateria_path, "r", encoding="utf-8") as bateria_file:
            self.bateriaToAnalyze = bateria_file.read()
       
        