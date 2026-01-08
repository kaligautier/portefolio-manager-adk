import logging

from google.adk.agents import SequentialAgent

from app.components.sub_agents.ibkr_reader_agent.agent import create_agent as create_ibkr_reader_agent
from app.components.sub_agents.market_reader_agent.agent import create_agent as create_market_reader_agent
from app.components.sub_agents.portfolio_evaluator_agent.agent import create_agent as create_portfolio_evaluator_agent
from app.components.sub_agents.decision_maker_agent.agent import create_agent as create_decision_maker_agent
from app.components.sub_agents.order_executor_agent.agent import create_agent as create_order_executor_agent
from app.components.callbacks.after_agent import log_agent_end
from app.components.callbacks.before_agent import log_agent_start
from app.config.constants import PORTEFOLIO_MANAGER_AGENT_DESCRIPTION

logger = logging.getLogger(__name__)

root_agent = SequentialAgent(
    name="portefolio_master_agent",
    description=PORTEFOLIO_MANAGER_AGENT_DESCRIPTION,
    sub_agents=[
        create_ibkr_reader_agent(),
        create_market_reader_agent(),
        create_portfolio_evaluator_agent(),
        create_decision_maker_agent(),
        create_order_executor_agent(),
    ],
    before_agent_callback=log_agent_start,
    after_agent_callback=log_agent_end,
)
