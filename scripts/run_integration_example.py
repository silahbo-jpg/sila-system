import sys
import os
import asyncio
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("run_integration_example")

# Adicionar o diretório raiz do projeto ao sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

async def run_example():
    """Executa o exemplo de integração."""
    try:
        logger.info("Importando o exemplo de integração")
        from backend.app.modules.integration.examples.integration_example import main
        
        logger.info("Executando o exemplo de integração")
        await main()
        
        logger.info("Exemplo executado com sucesso")
    except Exception as e:
        logger.error(f"Erro ao executar o exemplo: {str(e)}")
        raise

if __name__ == "__main__":
    logger.info("Iniciando script de exemplo de integração")
    asyncio.run(run_example())
    logger.info("Script finalizado")
