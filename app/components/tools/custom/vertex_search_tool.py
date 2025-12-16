"""Vertex AI Search tool for direct search in datastores."""

import logging

from google.adk.tools import VertexAiSearchTool

from app.config.settings import settings

logger = logging.getLogger(__name__)

# Initialize Vertex AI Search tool for direct search queries
# This tool provides more control over search results compared to RAG retrieval
# Note: VertexAiSearchTool ne supporte pas 'name' et 'description' - ces métadonnées
# sont générées automatiquement par ADK
vertex_search_tool = VertexAiSearchTool(
    data_store_id=settings.SEARCH_DATASTORE_ID,  # Full resource path
    max_results=10,  # Nombre maximum de résultats
    filter="",  # Filtre optionnel (ex: "category:brand")
)
