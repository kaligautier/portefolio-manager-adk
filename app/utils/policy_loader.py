"""Policy Loader Utility

Loads investment policy from YAML files.
"""
import yaml
from pathlib import Path
from typing import Dict, Any


class PolicyLoader:
    """Loads and manages investment policies from YAML files."""

    def __init__(self, policy_dir: str = "investment_policy"):
        """Initialize policy loader.

        Args:
            policy_dir: Directory containing policy YAML files
        """
        self.policy_dir = Path(policy_dir)
        if not self.policy_dir.is_absolute():
            # Make path relative to project root
            self.policy_dir = Path(__file__).parent.parent.parent / policy_dir

    def load_policy(self, policy_name: str = "default_policy") -> Dict[str, Any]:
        """Load a policy from YAML file.

        Args:
            policy_name: Name of the policy file (without .yaml extension)

        Returns:
            Dictionary containing the policy configuration

        Raises:
            FileNotFoundError: If policy file doesn't exist
            yaml.YAMLError: If policy file is invalid YAML
        """
        policy_file = self.policy_dir / f"{policy_name}.yaml"

        if not policy_file.exists():
            raise FileNotFoundError(
                f"Policy file not found: {policy_file}. "
                f"Available policies: {self.list_policies()}"
            )

        with open(policy_file, 'r') as f:
            policy = yaml.safe_load(f)

        return policy

    def list_policies(self) -> list[str]:
        """List all available policy files.

        Returns:
            List of policy names (without .yaml extension)
        """
        if not self.policy_dir.exists():
            return []

        return [
            p.stem for p in self.policy_dir.glob("*.yaml")
        ]

    def get_policy_summary(self, policy_name: str = "default_policy") -> str:
        """Get a human-readable summary of a policy.

        Args:
            policy_name: Name of the policy file

        Returns:
            Formatted string summary of the policy
        """
        policy = self.load_policy(policy_name)

        summary = []
        summary.append(f"Policy: {policy.get('policy_metadata', {}).get('name', policy_name)}")
        summary.append(f"Version: {policy.get('policy_metadata', {}).get('version', 'unknown')}")
        summary.append("")

        # Investor profile
        profile = policy.get('investor_profile', {})
        summary.append("Investor Profile:")
        summary.append(f"  - Risk Tolerance: {profile.get('risk_tolerance', 'unknown')}")
        summary.append(f"  - Investment Horizon: {profile.get('investment_horizon', 'unknown')}")
        summary.append(f"  - Account ID: {profile.get('account_id', 'unknown')}")
        summary.append("")

        # Risk management
        risk = policy.get('risk_management', {})
        summary.append("Risk Management:")
        summary.append(f"  - Max Drawdown: {risk.get('max_drawdown_percent', 'N/A')}%")
        summary.append(f"  - Max Position Concentration: {risk.get('max_position_concentration_percent', 'N/A')}%")
        summary.append(f"  - Stop Loss: {risk.get('stop_loss_percent', 'N/A')}%")
        summary.append(f"  - Take Profit: {risk.get('take_profit_percent', 'N/A')}%")
        summary.append("")

        # Asset allocation
        allocation = policy.get('asset_allocation', {}).get('target_allocation', {})
        summary.append("Target Asset Allocation:")
        for asset, pct in allocation.items():
            summary.append(f"  - {asset.capitalize()}: {pct}%")

        return "\n".join(summary)


# Global instance
policy_loader = PolicyLoader()


def load_default_policy() -> Dict[str, Any]:
    """Convenience function to load the default policy."""
    return policy_loader.load_policy("default_policy")


def get_account_id_from_policy(policy: Dict[str, Any]) -> str:
    """Extract account ID from policy."""
    return policy.get('investor_profile', {}).get('account_id', '')
