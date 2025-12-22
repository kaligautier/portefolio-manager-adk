from app.instructions.instructions_manager import InstructionsManager

instructions_manager = InstructionsManager()

AGENT_BQ_DESCRIPTION = """Analyste de données BigQuery - Expert en interrogation et analyse de grands ensembles de données."""
AGENT_BQ_INSTRUCTION = instructions_manager.get_instructions("bigquery_agent/bigquery_agent_instruction_v1")

VERTEX_AI_RAG_DESCRIPTION = """Utilise l'outil de récupération RAG de Vertex AI pour obtenir des réponses contextuelles du corpus RAG."""
VERTEX_AI_RAG_INSTRUCTION = """Use the Vertex AI RAG retrieval tool to get context-aware responses from the RAG corpus."""

VERTEX_AI_SEARCH_DESCRIPTION = """Utilise l'outil de recherche Vertex AI pour obtenir des réponses contextuelles du magasin de données Search."""
VERTEX_AI_SEARCH_INSTRUCTION = """Simple single-purpose agent that demonstrates basic ADK patterns. Use the Vertex AI Search tool to get 
context-aware responses from the Search datastore."""

PORTEFOLIO_MANAGER_AGENT_DESCRIPTION = "Agent principal pour la gestion de portefeuille, orchestrant des spécialistes de l'immobilier, des actions et du marché."
PORTEFOLIO_MANAGER_AGENT_INSTRUCTION = instructions_manager.get_instructions("portefolio_manager/portefolio_manager_agent_instruction_v1")

REAL_ESTATE_AGENT_DESCRIPTION = "Agent spécialiste en immobilier."
REAL_ESTATE_AGENT_INSTRUCTION = instructions_manager.get_instructions("real_estate_specialist_agent/real_estate_specialist_agent_instruction_v1")

STOCK_PORTFOLIO_AGENT_DESCRIPTION = "Agent spécialiste de l'analyse de porte feuille d'actions."
STOCK_PORTFOLIO_AGENT_INSTRUCTION = instructions_manager.get_instructions("stock_portfolio_agent/stock_portfolio_agent_instruction_v1")

MARKET_SPECIALIST_AGENT_DESCRIPTION = "Agent spécialiste des marchés."
MARKET_SPECIALIST_AGENT_INSTRUCTION = instructions_manager.get_instructions("market_specialist_agent/market_specialist_agent_instruction_v1")

