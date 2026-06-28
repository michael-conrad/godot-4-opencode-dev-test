#!/usr/bin/env python3
"""
Multi-Agent Orchestrator

Routes tasks to specialized agents based on capability profiles and dispatch rules.
"""

import argparse
import logging
import yaml
import sys
from pathlib import Path
from typing import Optional, Dict, List, Any
from ollama_client import OllamaClient, OllamaConfig

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class AgentRegistry:
    """Manages agent capability profiles."""

    def __init__(self, agent_cards_dir: Path):
        self.agent_cards_dir = agent_cards_dir
        self.agents: Dict[str, Dict[str, Any]] = {}
        self.load_agents()

    def load_agents(self):
        """Load all agent card YAML files."""
        for card_file in self.agent_cards_dir.glob("*.yaml"):
            if card_file.name.startswith("."):
                continue
            try:
                with open(card_file, 'r') as f:
                    agent_data = yaml.safe_load(f)
                    if agent_data and 'name' in agent_data:
                        agent_id = card_file.stem
                        self.agents[agent_id] = agent_data
                        logger.debug(f"Loaded agent: {agent_id}")
            except Exception as e:
                logger.error(f"Failed to load {card_file}: {e}")

    def get_agent(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get agent by ID."""
        return self.agents.get(agent_id)

    def list_agents(self) -> List[str]:
        """List all loaded agent IDs."""
        return list(self.agents.keys())


class Dispatcher:
    """Routes tasks to appropriate agents."""

    def __init__(self, registry: AgentRegistry, rules_file: Path):
        self.registry = registry
        self.rules = self.load_rules(rules_file)
        self.client = OllamaClient()

    def load_rules(self, rules_file: Path) -> Dict[str, Any]:
        """Load dispatch rules."""
        try:
            with open(rules_file, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.error(f"Failed to load rules: {e}")
            return {}

    def select_agent(self, task: str, explicit_agent: Optional[str] = None) -> str:
        """
        Select best agent for task.
        
        Args:
            task: Task description
            explicit_agent: If provided, use this agent
        
        Returns:
            Selected agent ID
        """
        if explicit_agent:
            if explicit_agent in self.registry.list_agents():
                logger.info(f"Using explicitly specified agent: {explicit_agent}")
                return explicit_agent
            else:
                logger.warning(f"Explicit agent {explicit_agent} not found, using orchestrator")

        # Try keyword-based routing first
        keyword_rules = self.rules.get('keyword_routing', [])
        for rule in keyword_rules:
            for keyword in rule.get('keywords', []):
                if keyword.lower() in task.lower():
                    agent_id = rule['primary'].replace(':', '').replace('.', '_').lower()
                    logger.info(f"Matched keyword '{keyword}' -> {agent_id}")
                    return agent_id

        # Default to orchestrator if no match
        logger.info("No keyword match, using orchestrator")
        return "qwen3.6-orchestrator"

    def dispatch(self, task: str, explicit_agent: Optional[str] = None) -> str:
        """
        Dispatch task to selected agent and return response.
        
        Args:
            task: Task description
            explicit_agent: Override agent selection
        
        Returns:
            Agent response
        """
        agent_id = self.select_agent(task, explicit_agent)
        agent_data = self.registry.get_agent(agent_id)

        if not agent_data:
            logger.error(f"Agent {agent_id} not found")
            return "Error: Agent not found"

        model = agent_data.get('model', 'qwen3.6:35b')
        temperature = agent_data.get('parameters', {}).get('temperature', 0.7)

        logger.info(f"Dispatching to {agent_data.get('name', agent_id)}")
        logger.info(f"Model: {model}")
        logger.info(f"Task: {task}")

        try:
            response = self.client.chat(
                model=model,
                messages=[
                    {"role": "user", "content": task}
                ],
                temperature=temperature
            )
            return response.get('message', {}).get('content', 'No response')
        except Exception as e:
            logger.error(f"Dispatch failed: {e}")
            return f"Error: {e}"


def main():
    parser = argparse.ArgumentParser(
        description="Multi-agent orchestrator for Godot game development"
    )
    parser.add_argument(
        "--task",
        type=str,
        help="Task to dispatch"
    )
    parser.add_argument(
        "--agent",
        type=str,
        help="Explicitly specify agent (override auto-selection)"
    )
    parser.add_argument(
        "--list-agents",
        action="store_true",
        help="List all available agents"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Verbose logging"
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Interactive mode (read tasks from stdin)"
    )

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Setup paths
    script_dir = Path(__file__).parent
    agent_cards_dir = script_dir / "agent-cards"
    rules_file = script_dir / "dispatch-rules.yaml"

    # Initialize
    registry = AgentRegistry(agent_cards_dir)
    dispatcher = Dispatcher(registry, rules_file)

    if args.list_agents:
        print("\nAvailable agents:")
        for agent_id in registry.list_agents():
            agent = registry.get_agent(agent_id)
            print(f"  {agent_id}: {agent.get('name', 'Unknown')}")
        return

    if args.interactive:
        print("Interactive mode (Ctrl+C to exit)")
        while True:
            try:
                task = input("\nTask> ").strip()
                if not task:
                    continue
                response = dispatcher.dispatch(task, args.agent)
                print(f"\nResponse:\n{response}\n")
            except KeyboardInterrupt:
                print("\nExiting")
                break
        return

    if args.task:
        response = dispatcher.dispatch(args.task, args.agent)
        print(response)
        return

    parser.print_help()


if __name__ == "__main__":
    main()
