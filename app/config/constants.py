from app.instructions.instructions_manager import InstructionsManager

instructions_manager = InstructionsManager()

VERTEX_AI_RAG_DESCRIPTION = """Utilise l'outil de récupération RAG de Vertex AI pour obtenir des réponses contextuelles du corpus RAG."""
VERTEX_AI_RAG_INSTRUCTION = """Use the Vertex AI RAG retrieval tool to get context-aware responses from the RAG corpus."""

PORTEFOLIO_MANAGER_AGENT_DESCRIPTION = "Agent principal pour la gestion de portefeuille, orchestrant des spécialistes de l'immobilier, des actions et du marché."
PORTEFOLIO_MANAGER_AGENT_INSTRUCTION = instructions_manager.get_instructions("portefolio_manager/portefolio_manager_agent_instruction_v1")

ORDER_AGENT_DESCRIPTION = "Agent spécialiste du passage d'ordres sur les marchés financiers."
ORDER_AGENT_INSTRUCTION = instructions_manager.get_instructions("order_agent/order_agent_instruction_v1")

STOCK_PORTFOLIO_AGENT_DESCRIPTION = "Agent spécialiste de l'analyse de porte feuille d'actions."
STOCK_PORTFOLIO_AGENT_INSTRUCTION = instructions_manager.get_instructions("stock_portfolio_agent/stock_portfolio_agent_instruction_v1")

MARKET_SPECIALIST_AGENT_DESCRIPTION = "Agent spécialiste des marchés."
MARKET_SPECIALIST_AGENT_INSTRUCTION = instructions_manager.get_instructions("market_specialist_agent/market_specialist_agent_instruction_v1")

