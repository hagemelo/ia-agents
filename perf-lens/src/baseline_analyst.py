from agents import Agent
from perf_data import PerfData
from dotenv import load_dotenv

class BaselineAnalyst:
    def __init__(self):
        self.instrucoes_baseline = """
            Você é um especialista em análise de desempenho de software.
            Sua tarefa é analisar as baterias de teste e identificar a melhor performance.
            deve definir como baseline o resultado final de uma das baterias de testes de desempenho já realizadas. 
            Baseline é uma bateria que obteve o melhor resultado, seguindo os seguintes critérios: latência mais baixa, 
            taxa de erro mais baixo e vazão mais alta. Você deve apontar com base nesta relação de csv de baterias de testes, 
            com data da execução, vazão, latência e Taxa de Erro, 
            Você não precisa ser detalhista, apenas apontar a melhor bateria de teste de desempenho.
            Deve-se retorna a melhor bateria nos critérios apontado acima, apontando no seguinte formato json: 
            {{
                "data": "data de execução da bateria", 
                "vazao": "vazão alcançada na bateria", 
                "latencia": "A latência alcançada na bateria", 
                "erro": "taxa de erro alcançado na bateria"
            }}
        """

    def getBaselineAgent(self, history: str) -> Agent:
        load_dotenv(override=True)
        instrucoes_baseline = self.instrucoes_baseline + f"""
            a baseline deve ser selecionada entre os itens de histórico de testes anteriores em: {history}
        """
        baselineAnalyst = Agent(
                name="Baseline Analyst",
                instructions=instrucoes_baseline,
                output_type=PerfData,
                model="gpt-5-mini",
        )

        baselineAnalystTool = baselineAnalyst.as_tool(tool_name="baselineAnalyst", tool_description="Selecionar a melhor bateria de teste de desempenho")
        return baselineAnalystTool
