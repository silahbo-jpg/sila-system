"""
Script para executar os testes de cenários de erro do módulo de cidadania.

Este script pode ser executado diretamente sem depender do pytest ou conftest global.
"""
from test_error_scenarios import TestCitizenErrorScenarios

if __name__ == "__main__":
    tester = TestCitizenErrorScenarios()
    success = tester.run_all_tests()
    exit(0 if success else 1)

