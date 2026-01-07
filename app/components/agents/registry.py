"""
Agent Registry - Central registry for all agents in the portfolio manager.

This module provides a dictionary mapping agent names to their factory functions,
making it easy to discover and create agent instances programmatically.
"""

from typing import Callable, Dict

from google.adk.agents import LlmAgent

# Import factory functions
from app.components.agents.ibkr_reader_agent.agent import create_agent as create_ibkr_reader_agent
from app.components.agents.market_reader_agent.agent import create_agent as create_market_reader_agent
from app.components.agents.portfolio_evaluator_agent.agent import create_agent as create_portfolio_evaluator_agent
from app.components.agents.decision_maker_agent.agent import create_agent as create_decision_maker_agent
from app.components.agents.order_executor_agent.agent import create_agent as create_order_executor_agent
from app.components.agents.portefolio_master_agent.agent import root_agent as portefolio_master_agent


# Agent factory registry: maps agent names to factory functions
AGENT_FACTORIES: Dict[str, Callable[[], LlmAgent]] = {
    "ibkr_reader_agent": create_ibkr_reader_agent,
    "market_reader_agent": create_market_reader_agent,
    "portfolio_evaluator_agent": create_portfolio_evaluator_agent,
    "decision_maker_agent": create_decision_maker_agent,
    "order_executor_agent": create_order_executor_agent,
}

# Pre-instantiated agents (orchestrator only)
AGENTS_REGISTRY: Dict[str, LlmAgent] = {
    "portefolio_master_agent": portefolio_master_agent,
}


def create_agent(agent_name: str) -> LlmAgent:
    """
    Create a new instance of an agent by name.

    Args:
        agent_name: Name of the agent to create

    Returns:
        A new agent instance

    Raises:
        KeyError: If agent name is not found in registry
    """
    if agent_name in AGENT_FACTORIES:
        return AGENT_FACTORIES[agent_name]()
    elif agent_name in AGENTS_REGISTRY:
        return AGENTS_REGISTRY[agent_name]
    else:
        available = ", ".join(list(AGENT_FACTORIES.keys()) + list(AGENTS_REGISTRY.keys()))
        raise KeyError(
            f"Agent '{agent_name}' not found. Available agents: {available}"
        )


def get_agent(agent_name: str) -> LlmAgent:
    """
    Get a pre-instantiated agent by name (orchestrators only).

    Args:
        agent_name: Name of the agent to retrieve

    Returns:
        The agent instance

    Raises:
        KeyError: If agent name is not found in pre-instantiated registry
    """
    if agent_name not in AGENTS_REGISTRY:
        available = ", ".join(AGENTS_REGISTRY.keys())
        raise KeyError(
            f"Pre-instantiated agent '{agent_name}' not found. Available: {available}"
        )
    return AGENTS_REGISTRY[agent_name]


def list_agent_names() -> list[str]:
    """
    Get a list of all registered agent names.

    Returns:
        List of agent names
    """
    return list(AGENT_FACTORIES.keys()) + list(AGENTS_REGISTRY.keys())
