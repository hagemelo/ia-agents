from agents import Agent, OpenAIChatCompletionsModel
from openai import AsyncOpenAI
import os
from perf_data import PerfData
from dotenv import load_dotenv


class SuiteAnalyst:
    def __init__(self):
        self.instrucoes_suite = """
            Você é um especialista em análise de desempenho de software.
            Sua tarefa é analisar o resultado de uma bateria de teste e identificar o melhor resultado alcançado.
            O melhor resultado deve obedecer aos seguintes critérios: 
                latência não deve ser maior que 400ms, 
                taxa de erro não deve ser maior que 0.3% e 
                vazão deve ser a maior possível. 
            Você deve analisar os dados da bateria de teste no aquivo csv fornecido no com as seguintes colunas, 
            com data da execução, vazão, latência e Taxa de Erro, 
            Você não precisa ser detalhista, apenas apontar a melhor resultado alcançado.
            Deve-se retorna a melhor bateria nos critérios apontado acima, apontando no seguinte formato json: 
            {
                "data": "Deve ser a data atual", 
                "vazao": "vazão alcançada na bateria", 
                "latencia": "A latência alcançada na bateria", 
                "erro": "taxa de erro alcançado na bateria"
            }
        """

    def getSuiteAgent(self, bateriaToAnalyze: str) -> Agent:
        load_dotenv(override=True)
        instrucoes_suite = self.instrucoes_suite + f"""
            o resultado da bateria de teste é: {bateriaToAnalyze}
        """

        GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
        google_api_key = os.getenv('GOOGLE_API_KEY')

        gemini_client = AsyncOpenAI(base_url=GEMINI_BASE_URL, api_key=google_api_key)
        gemini_model = OpenAIChatCompletionsModel(model="gemini-2.5-flash", openai_client=gemini_client)
        
        suiteAnalyst = Agent(
            name="Suite Analyst",
            instructions=instrucoes_suite,
            output_type=PerfData,
            model=gemini_model,
        )
        suiteAnalystTool = suiteAnalyst.as_tool(tool_name="suiteAnalyst", tool_description="Analise o resultado da bateria de teste")
        return suiteAnalystTool