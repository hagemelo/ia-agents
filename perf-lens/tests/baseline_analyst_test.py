"""
Testes unitários para o baseline-analyst (classe BaselineAnalyst e PerfData).

Execute (a partir da pasta perf-lens/tests):
  python -m unittest baseline_analyst_test -v
"""
import importlib.util
import os
import sys

# Raiz do projeto (perf-lens) no path para importar perf_data e baseline_analyst
_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _root not in sys.path:
    sys.path.insert(0, _root)

import unittest
from unittest.mock import MagicMock, patch

import src.perf_data as _perf_data_module
from src.perf_data import PerfData

class BaselineAnalystTest(unittest.TestCase):
    """Testes da classe BaselineAnalyst e do método get_baseline_agent(history)."""

    def tearDown(self):
        if "src.baseline_analyst" in sys.modules:
            del sys.modules["src.baseline_analyst"]

    def _load_baseline_analyst_module(self):
        """Carrega o módulo baseline_analyst com Agent mockado; retorna (módulo, mock_agent)."""
        mock_agent = MagicMock()
        fake_agents = MagicMock()
        fake_agents.Agent = mock_agent
        path_baseline = os.path.join(_root, "src/baseline_analyst.py")
        spec = importlib.util.spec_from_file_location("src.baseline_analyst", path_baseline)
        with patch.dict(sys.modules, {"agents": fake_agents, "perf_data": _perf_data_module}):
            module = importlib.util.module_from_spec(spec)
            sys.modules["src.baseline_analyst"] = module
            spec.loader.exec_module(module)
        return module, mock_agent

    def test_get_baseline_agent_retorna_agente(self):
        """get_baseline_agent(history) deve retornar a instância do Agent criada."""
        module, mock_agent = self._load_baseline_analyst_module()
        analyst = module.BaselineAnalyst()
        result = analyst.get_baseline_agent("2025-01-01,100,200,0.0")
        self.assertIs(result, mock_agent.return_value)

    def test_get_baseline_agent_inclui_historico_nas_instrucoes(self):
        """As instruções do agente devem incluir o histórico passado para get_baseline_agent."""
        fake_history = "2025-01-01,100,200,0.1"
        module, mock_agent = self._load_baseline_analyst_module()
        analyst = module.BaselineAnalyst()
        analyst.get_baseline_agent(fake_history)
        mock_agent.assert_called_once()
        kwargs = mock_agent.call_args[1]
        self.assertIn("instructions", kwargs)
        self.assertIn(fake_history, kwargs["instructions"])

    def test_get_baseline_agent_cria_agente_com_nome_e_output_type(self):
        """O Agent deve ser criado com name 'Baseline Analyst', output_type PerfData e model."""
        module, mock_agent = self._load_baseline_analyst_module()
        analyst = module.BaselineAnalyst()
        analyst.get_baseline_agent("csv,data")
        mock_agent.assert_called_once()
        kwargs = mock_agent.call_args[1]
        self.assertEqual(kwargs["name"], "Baseline Analyst")
        self.assertIs(kwargs["output_type"], PerfData)
        self.assertEqual(kwargs["model"], "gpt-5-mini")

    def test_instrucoes_contem_criterios_baseline(self):
        """As instruções devem mencionar latência, vazão, erro e baseline."""
        module, mock_agent = self._load_baseline_analyst_module()
        analyst = module.BaselineAnalyst()
        analyst.get_baseline_agent("2025-01-01,100,200,0.0")
        instructions = mock_agent.call_args[1]["instructions"]
        self.assertIn("latência", instructions.lower())
        self.assertTrue(
            "vazão" in instructions.lower() or "vazao" in instructions.lower()
        )
        self.assertIn("erro", instructions.lower())
        self.assertIn("baseline", instructions.lower())


if __name__ == "__main__":
    unittest.main()
