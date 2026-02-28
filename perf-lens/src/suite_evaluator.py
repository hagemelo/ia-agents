from agents import Agent
from assessment import Assessment

class SuiteEvaluator:
    def __init__(self):
        self.instrucoes_suite_evaluator = """
            Você é um especialista em análise de desempenho de software.
            Sua tarefa é comparar o resultado da bateria de teste com a baseline.
            você receberá do BaselineAnalyst a baseline com os dados de data,vazao,latencia e erro.
            você receberá do SuiteAnalyst o resultado da bateria de teste com os dados de data,vazao,latencia e erro.
            você deve avaliar se o resultado da bateria de teste é melhor que a baseline, seguindo os seguintes critérios: latência mais baixa, 
            taxa de erro mais baixo e vazão mais alta.
            Deve-se retorna a melhor bateria nos critérios apontado acima, apontando no seguinte formato json: 
            {
                "assessment": "Avaliação se o resultado da bateria de teste é melhor que a baseline",
                "baseline": {
                    "data": "data de execução da bateria", 
                    "vazao": "vazão alcançada na bateria", 
                    "latencia": "A latência alcançada na bateria", 
                    "erro": "taxa de erro alcançado na bateria"
                },
                "suiteResult": {
                    "data": "data de execução da bateria", 
                    "vazao": "vazão alcançada na bateria", 
                    "latencia": "A latência alcançada na bateria", 
                    "erro": "taxa de erro alcançado na bateria"
                }
            }
        """
    
    def getSuiteEvaluatorAgent(self) -> Agent:
        
        suiteEvaluator =Agent(
            name="Suite Evaluator",
            instructions=self.instrucoes_suite_evaluator,
            model="gpt-5-mini",
            output_type=Assessment,
            handoff_description="Comparar resultado da bateria de teste com a baseline")
        return suiteEvaluator