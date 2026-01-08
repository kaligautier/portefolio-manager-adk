"""Helper functions to parse and validate agent outputs using Pydantic models."""

import json
import logging
import re
from typing import Any, Dict, Optional, Type, TypeVar

from pydantic import BaseModel, ValidationError

from app.models.agent_data import (
    DecisionPlan,
    ExecutionSummary,
    MarketAnalysis,
    PortfolioSnapshot,
    RiskAssessment,
)

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)


def extract_json_from_text(text: str) -> Optional[str]:
    """
    Extract JSON content from text that may contain markdown code blocks or other formatting.

    Args:
        text: Text that may contain JSON, possibly wrapped in ```json ... ``` or ```...```

    Returns:
        Extracted JSON string, or None if no valid JSON found
    """
    # Try to find JSON in code blocks first
    json_block_pattern = r"```(?:json)?\s*\n?(.*?)\n?```"
    matches = re.findall(json_block_pattern, text, re.DOTALL)

    if matches:
        # Return the first match
        return matches[0].strip()

    # Try to find raw JSON object
    # Look for opening { and closing }
    try:
        start = text.index("{")
        # Find the matching closing brace
        brace_count = 0
        for i in range(start, len(text)):
            if text[i] == "{":
                brace_count += 1
            elif text[i] == "}":
                brace_count -= 1
                if brace_count == 0:
                    return text[start : i + 1]
    except (ValueError, IndexError):
        pass

    # If all else fails, try to parse the entire text as JSON
    try:
        json.loads(text)
        return text
    except json.JSONDecodeError:
        pass

    return None


def parse_agent_output(
    agent_output: str,
    model_class: Type[T],
    output_key: Optional[str] = None,
) -> Optional[T]:
    """
    Parse and validate agent output using a Pydantic model.

    Args:
        agent_output: Raw text output from an agent
        model_class: Pydantic model class to validate against
        output_key: Optional key to identify this output (for logging)

    Returns:
        Validated Pydantic model instance, or None if parsing fails

    Example:
        >>> output = agent.query("Get portfolio")
        >>> snapshot = parse_agent_output(output, PortfolioSnapshot, "portfolio_snapshot")
        >>> if snapshot:
        >>>     print(f"Total value: ${snapshot.total_market_value}")
    """
    key_label = f" [{output_key}]" if output_key else ""
    logger.debug(f"Parsing agent output{key_label} with {model_class.__name__}")

    # Extract JSON from the text
    json_str = extract_json_from_text(agent_output)

    if not json_str:
        logger.error(f"Could not extract JSON from agent output{key_label}")
        logger.debug(f"Raw output: {agent_output[:500]}...")
        return None

    # Parse JSON
    try:
        data = json.loads(json_str)
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in agent output{key_label}: {e}")
        logger.debug(f"JSON string: {json_str[:500]}...")
        return None

    # Validate with Pydantic
    try:
        instance = model_class.model_validate(data)
        logger.info(
            f"Successfully parsed and validated {model_class.__name__}{key_label}"
        )
        return instance
    except ValidationError as e:
        logger.error(f"Validation failed for {model_class.__name__}{key_label}: {e}")
        logger.debug(f"Data: {json.dumps(data, indent=2)}")
        return None


def parse_workflow_state(state: Dict[str, Any]) -> Dict[str, Optional[BaseModel]]:
    """
    Parse all outputs from a workflow state using the appropriate Pydantic models.

    Args:
        state: State dictionary from SequentialAgent containing output_key values

    Returns:
        Dictionary mapping output_key to validated Pydantic model instances

    Example:
        >>> state = {
        ...     "portfolio_snapshot": '{"account_id": "DUO316496", ...}',
        ...     "market_analysis": '{"vix_level": 18.5, ...}',
        ... }
        >>> parsed = parse_workflow_state(state)
        >>> snapshot = parsed["portfolio_snapshot"]
        >>> analysis = parsed["market_analysis"]
    """
    parsers = {
        "portfolio_snapshot": PortfolioSnapshot,
        "market_analysis": MarketAnalysis,
        "risk_assessment": RiskAssessment,
        "decision_plan": DecisionPlan,
        "execution_summary": ExecutionSummary,
    }

    results = {}

    for key, model_class in parsers.items():
        if key in state:
            logger.info(f"Parsing state['{key}'] with {model_class.__name__}")
            parsed = parse_agent_output(state[key], model_class, output_key=key)
            results[key] = parsed
        else:
            logger.debug(f"State key '{key}' not found, skipping")
            results[key] = None

    return results


def validate_and_log(
    agent_output: str,
    model_class: Type[T],
    output_key: str,
    raise_on_error: bool = False,
) -> Optional[T]:
    """
    Parse, validate, and log agent output with detailed error handling.

    Args:
        agent_output: Raw text output from an agent
        model_class: Pydantic model class to validate against
        output_key: Key to identify this output
        raise_on_error: If True, raise ValidationError on failure

    Returns:
        Validated Pydantic model instance, or None if parsing fails

    Raises:
        ValidationError: If raise_on_error=True and validation fails
    """
    result = parse_agent_output(agent_output, model_class, output_key)

    if result is None and raise_on_error:
        raise ValidationError(f"Failed to parse {output_key} as {model_class.__name__}")

    if result:
        logger.info(
            f"✓ {output_key}: Successfully validated {model_class.__name__}",
            extra={"output_key": output_key, "model": model_class.__name__},
        )
    else:
        logger.error(
            f"✗ {output_key}: Failed to validate {model_class.__name__}",
            extra={"output_key": output_key, "model": model_class.__name__},
        )

    return result


# Convenience functions for each step


def parse_portfolio_snapshot(agent_output: str) -> Optional[PortfolioSnapshot]:
    """Parse portfolio snapshot from IBKR Reader Agent."""
    return parse_agent_output(agent_output, PortfolioSnapshot, "portfolio_snapshot")


def parse_market_analysis(agent_output: str) -> Optional[MarketAnalysis]:
    """Parse market analysis from Market Reader Agent."""
    return parse_agent_output(agent_output, MarketAnalysis, "market_analysis")


def parse_risk_assessment(agent_output: str) -> Optional[RiskAssessment]:
    """Parse risk assessment from Portfolio Evaluator Agent."""
    return parse_agent_output(agent_output, RiskAssessment, "risk_assessment")


def parse_decision_plan(agent_output: str) -> Optional[DecisionPlan]:
    """Parse decision plan from Decision Maker Agent."""
    return parse_agent_output(agent_output, DecisionPlan, "decision_plan")


def parse_execution_summary(agent_output: str) -> Optional[ExecutionSummary]:
    """Parse execution summary from Order Executor Agent."""
    return parse_agent_output(agent_output, ExecutionSummary, "execution_summary")
