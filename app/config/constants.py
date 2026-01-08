from app.instructions.instructions_manager import InstructionsManager

instructions_manager = InstructionsManager()

VERTEX_AI_RAG_DESCRIPTION = "Utilise l'outil de récupération RAG de Vertex AI pour obtenir des réponses contextuelles du corpus RAG. Tu disposes aussi du mcp IBKR pour rechercher des données de marché et de portefeuille."
VERTEX_AI_RAG_INSTRUCTION = instructions_manager.get_instructions("vertex_ai_rag/vertex_ai_rag_instruction_v1")

PORTEFOLIO_MANAGER_AGENT_DESCRIPTION = "Agent principal orchestrant séquentiellement le workflow autonome de gestion de portefeuille."

IBKR_READER_AGENT_DESCRIPTION = "Agent spécialisé dans la lecture des données de portefeuille IBKR: positions, cash, PnL."
IBKR_READER_AGENT_INSTRUCTION = instructions_manager.get_instructions("ibkr_reader_agent/ibkr_reader_agent_instruction_v2")

MARKET_READER_AGENT_DESCRIPTION = "Agent spécialisé dans la lecture des conditions de marché: prix, volatilité, tendances."
MARKET_READER_AGENT_INSTRUCTION = instructions_manager.get_instructions("market_reader_agent/market_reader_agent_instruction_v2")

PORTFOLIO_EVALUATOR_AGENT_DESCRIPTION = "Agent spécialisé dans l'évaluation des risques de portefeuille: drawdown, concentration, exposition."
PORTFOLIO_EVALUATOR_AGENT_INSTRUCTION = instructions_manager.get_instructions("portfolio_evaluator_agent/portfolio_evaluator_agent_instruction_v2")

DECISION_MAKER_AGENT_DESCRIPTION = "Agent spécialisé dans la prise de décisions de portefeuille: hold, reinforce, rotate, cut losers."
DECISION_MAKER_AGENT_INSTRUCTION = instructions_manager.get_instructions("decision_maker_agent/decision_maker_agent_instruction_v2")

ORDER_EXECUTOR_AGENT_DESCRIPTION = "Agent spécialisé dans l'exécution autonome d'ordres IBKR avec vérifications de sécurité."
ORDER_EXECUTOR_AGENT_INSTRUCTION = instructions_manager.get_instructions("order_executor_agent/order_executor_agent_instruction_v2")


def get_daily_workflow_message(policy: dict, account_id: str) -> str:
    """
    Generate daily workflow message from Jinja template.

    Args:
        policy: Investment policy dictionary
        account_id: IBKR account ID

    Returns:
        Formatted workflow message
    """
    return instructions_manager.get_instructions(
        "portefolio_manager/daily_workflow_message_v1",
        policy_name=policy.get('policy_metadata', {}).get('name', 'Default'),
        account_id=account_id,
        risk_tolerance=policy.get('investor_profile', {}).get('risk_tolerance', 'moderate'),
        max_drawdown=policy.get('risk_management', {}).get('max_drawdown_percent', 15),
        max_position_concentration=policy.get('risk_management', {}).get('max_position_concentration_percent', 20),
        stop_loss=policy.get('risk_management', {}).get('stop_loss_percent', -10),
        take_profit=policy.get('risk_management', {}).get('take_profit_percent', 50),
    )
