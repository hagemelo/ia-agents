from agents import Agent, Runner, GuardrailFunctionOutput, input_guardrail
from check_perf_data import CheckPerfDataOutput


instrucoes_perf_data_guard = """
    Verifique se os dados obtidos pelo SuiteAnalyst são válidos.
    Deve-se retorna os dados de desempenho de software válidos, apontando no seguinte formato json: 
    {
        "is_perf_data_valid": "true ou false",
        "perf_data": "dados de desempenho de software, com data, vazão, latência e taxa de erro"
    }
"""

guardrail_agent = Agent( 
        name="Perf Data Guard",
        instructions=instrucoes_perf_data_guard,
        output_type=CheckPerfDataOutput,
        model="gpt-4o-mini"
        )

@input_guardrail
async def guardrail_perf_data_guard(ctx, agent, message):
    result = await Runner.run(guardrail_agent, message, context=ctx.context)
    is_perf_data_valid = result.final_output.is_perf_data_valid
    return GuardrailFunctionOutput(output_info={"perf_data_valid": result.final_output},tripwire_triggered=is_perf_data_valid)


