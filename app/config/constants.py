from app.instructions.instructions_manager import InstructionsManager

instructions_manager = InstructionsManager()

MASTER_AGENT_DESCRIPTION = """Simple single-purpose agent that demonstrates basic ADK patterns."""

MASTER_AGENT_INSTRUCTION = instructions_manager.get_instructions("master_agent/master_agent_instruction_v1")

AGENT_BRAND_STRATEGIST_DESCRIPTION = """
Assistant Brand Strategist - Le Cerveau de la Marque (Agent dont la mission est d'assurer la cohérence et l'identité de marque).
"""

AGENT_BRAND_STRATEGIST_INSTRUCTION = instructions_manager.get_instructions("brand_strategist/agent_brand_strategist_v1")

AGENT_BRAND_GUARDIAN_DESCRIPTION = """
Assistant Le Gardien de la Marque : Agent de contrôle qualité (technique et cohérence) pour assurer la protection de l'identité de marque.
"""

AGENT_BRAND_GUARDIAN_INSTRUCTION = instructions_manager.get_instructions("brand_guardian/brand_guardian_v1")

AGENT_SOCIAL_DIRECTOR_DESCRIPTION = """
Agent Social Director - Le garant de la performance et de l'identité de marque "Chronodrive" sur les réseaux sociaux. 
S'assure que la marque est à la fois tendance et unique, jamais dépassée, jamais générique.
"""

AGENT_SOCIAL_DIRECTOR_INSTRUCTION = instructions_manager.get_instructions("social_director/agent_social_director_v1")

AGENT_BQ_DESCRIPTION = """BigQuery Data Analyst - Expert in querying and analyzing large-scale datasets."""

AGENT_BQ_INSTRUCTION = instructions_manager.get_instructions("bigquery_agent/bigquery_agent_instruction_v1")

VERTEX_AI_RAG_DESCRIPTION = """Use the Vertex AI RAG retrieval tool to get context-aware responses from the RAG corpus."""

VERTEX_AI_RAG_INSTRUCTION = """Use the Vertex AI RAG retrieval tool to get context-aware responses from the RAG corpus."""

VERTEX_AI_SEARCH_DESCRIPTION = """Use the Vertex AI Search tool to get context-aware responses from the Search datastore."""

VERTEX_AI_SEARCH_INSTRUCTION = """Simple single-purpose agent that demonstrates basic ADK patterns. Use the Vertex AI Search tool to get 
context-aware responses from the Search datastore."""

