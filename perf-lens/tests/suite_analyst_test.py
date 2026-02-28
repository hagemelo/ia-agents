"""
Testes unitários para a classe SuiteAnalyst.

Execute (a partir da pasta perf-lens/tests):
  python -m unittest suite_analyst_test -v
"""
import importlib.util
import os
import sys

_here = os.path.dirname(os.path.abspath(__file__))
_root = os.path.dirname(_here)
if _root not in sys.path:
    sys.path.insert(0, _root)

import unittest
from unittest.mock import MagicMock, patch

import src.perf_data as _perf_data_module
from src.perf_data import PerfData

class SuiteAnalystTest(unittest.TestCase):
    """Testes da classe TestSuiteAnalyst e do método get_test_suite_agent(test_suite_result)."""

    def tearDown(self):
        if "src.suite_analyst" in sys.modules:
            del sys.modules["src.suite_analyst"]

    def _load_test_suite_analyst_module(self):
        """Carrega o módulo test-suite_analyst com Agent, OpenAIChatCompletionsModel e AsyncOpenAI mockados."""
        mock_agent = MagicMock()
        mock_model = MagicMock()
        fake_agents = MagicMock()
        fake_agents.Agent = mock_agent
        fake_agents.OpenAIChatCompletionsModel = MagicMock(return_value=mock_model)
        fake_openai = MagicMock()
        fake_openai.AsyncOpenAI = MagicMock(return_value=MagicMock())
        path_module = os.path.join(_root, "src", "suite_analyst.py")
        spec = importlib.util.spec_from_file_location("src.suite_analyst", path_module)
        with patch.dict(
            sys.modules,
            {"agents": fake_agents, "openai": fake_openai, "perf_data": _perf_data_module},
        ), patch.dict(os.environ, {"GOOGLE_API_KEY": "fake-key"}):
            module = importlib.util.module_from_spec(spec)
            sys.modules["src.suite_analyst"] = module
            spec.loader.exec_module(module)
        return module, mock_agent

    def test_get_test_suite_agent_retorna_agente(self):
        """get_test_suite_agent(test_suite_result) deve retornar a instância do Agent criada."""
        module, mock_agent = self._load_test_suite_analyst_module()
        analyst = module.SuiteAnalyst()
        result = analyst.get_suite_agent("2025-01-01,100,200,0.0")
        self.assertIs(result, mock_agent.return_value)

    def test_get_test_suite_agent_inclui_resultado_nas_instrucoes(self):
        """As instruções do agente devem incluir o resultado da bateria passado para get_test_suite_agent."""
        fake_result = "2025-01-01,410,300,0.0"
        module, mock_agent = self._load_test_suite_analyst_module()
        analyst = module.SuiteAnalyst()
        analyst.get_suite_agent(fake_result)
        mock_agent.assert_called_once()
        kwargs = mock_agent.call_args[1]
        self.assertIn("instructions", kwargs)
        self.assertIn(fake_result, kwargs["instructions"])

    def test_get_test_suite_agent_cria_agente_com_nome_e_output_type(self):
        """O Agent deve ser criado com name 'Suite Analyst' e output_type PerfData."""
        module, mock_agent = self._load_test_suite_analyst_module()
        analyst = module.SuiteAnalyst()
        analyst.get_suite_agent("csv,data")
        mock_agent.assert_called_once()
        kwargs = mock_agent.call_args[1]
        self.assertEqual(kwargs["name"], "Suite Analyst")
        self.assertIs(kwargs["output_type"], PerfData)

    def test_instrucoes_contem_criterios_de_desempenho(self):
        """As instruções devem mencionar latência, taxa de erro, vazão e os limites (400ms, 0.3%)."""
        module, mock_agent = self._load_test_suite_analyst_module()
        analyst = module.SuiteAnalyst()
        analyst.get_suite_agent("2025-01-01,100,200,0.0")
        instructions = mock_agent.call_args[1]["instructions"]
        self.assertIn("latência", instructions.lower())
        self.assertIn("400", instructions)
        self.assertIn("0.3", instructions)
        self.assertTrue(
            "vazão" in instructions.lower() or "vazao" in instructions.lower()
        )
        self.assertIn("erro", instructions.lower())


if __name__ == "__main__":
    unittest.main()
