"""
    Agent Tools vs Sub-Agents: What's the Difference?
        This is a common question! Both involve using multiple agents, but they work very differently:

        Agent Tools (what we're using):

        Agent A calls Agent B as a tool
        Agent B's response goes back to Agent A
        Agent A stays in control and continues the conversation
        Use case: Delegation for specific tasks (like calculations)
    
    Sub-Agents (different pattern):

        Agent A transfers control completely to Agent B
        Agent B takes over and handles all future user input
        Agent A is out of the loop
        Use case: Handoff to specialists (like customer support tiers)
        In our currency example: We want the currency agent to get calculation results and continue working with them, so we use Agent Tools, not sub-agents.
"""
import logging

from google.adk.agents import LlmAgent
from google.adk.tools import AgentTool
from google.adk.code_executors import BuiltInCodeExecutor

from app.components.callbacks.after_agent import log_agent_end
from app.components.callbacks.before_agent import log_agent_start
from app.components.callbacks.tool_callbacks import log_after_tool, log_before_tool

from app.config.settings import settings
from app.components.tools.custom.example_tool import (
    get_exchange_rate_tool,
    get_fee_for_payment_method_tool,
)

logger = logging.getLogger(__name__)

calculation_agent = LlmAgent(
    name="CalculationAgent",
    model=settings.MODEL,
    instruction="""You are a specialized calculator that ONLY responds with Python code. You are forbidden from providing any text, explanations, or conversational responses.
 
     Your task is to take a request for a calculation and translate it into a single block of Python code that calculates the answer.
     
     **RULES:**
    1.  Your output MUST be ONLY a Python code block.
    2.  Do NOT write any text before or after the code block.
    3.  The Python code MUST calculate the result.
    4.  The Python code MUST print the final result to stdout.
    5.  You are PROHIBITED from performing the calculation yourself. Your only job is to generate the code that will perform the calculation.
   
    Failure to follow these rules will result in an error.
       """,
    code_executor=BuiltInCodeExecutor(),  # Use the built-in Code Executor Tool. This gives the agent code execution capabilities
    before_agent_callback=log_agent_start,  # Log when agent starts
    after_agent_callback=log_agent_end,  # Log when agent completes
    before_tool_callback=log_before_tool,  # Log before each tool call
    after_tool_callback=log_after_tool,  # Log after each tool call
)

root_agent = LlmAgent(
    name="agent_with_tools",
    model=settings.MODEL,
    description="""Currency conversion assistant with payment method fee tools""",
    instruction="""You are a smart currency conversion assistant. You must strictly follow these steps and use the available tools.

  For any currency conversion request:

   1. Get Transaction Fee: Use the get_fee_for_payment_method() tool to determine the transaction fee.
   2. Get Exchange Rate: Use the get_exchange_rate() tool to get the currency conversion rate.
   3. Error Check: After each tool call, you must check the "status" field in the response. If the status is "error", you must stop and clearly explain the issue to the user.
   4. Calculate Final Amount (CRITICAL): You are strictly prohibited from performing any arithmetic calculations yourself. You must use the calculation_agent tool to generate Python code that calculates the final converted amount. This 
      code will use the fee information from step 1 and the exchange rate from step 2.
   5. Provide Detailed Breakdown: In your summary, you must:
       * State the final converted amount.
       * Explain how the result was calculated, including:
           * The fee percentage and the fee amount in the original currency.
           * The amount remaining after deducting the fee.
           * The exchange rate applied.
           """,
    tools=[get_fee_for_payment_method_tool, get_exchange_rate_tool, AgentTool(agent=calculation_agent)],
    sub_agents=[],
    before_agent_callback=log_agent_start,  # Log when agent starts
    after_agent_callback=log_agent_end,  # Log when agent completes
    before_tool_callback=log_before_tool,  # Log before each tool call
    after_tool_callback=log_after_tool,  # Log after each tool call
)
