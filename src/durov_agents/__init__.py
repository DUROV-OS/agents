"""Durov.House MVP multi-agent runtime.

Eight fixed specialists, one shared company context, a hard legal gate,
and a labeling contract that says who marks what.
"""

from durov_agents.ids import AgentId
from durov_agents.passport import AgentPassport, load_roster
from durov_agents.runtime.coordinator import run_task
from durov_agents.runtime.types import RunResult

__all__ = ["AgentId", "AgentPassport", "load_roster", "run_task", "RunResult"]
__version__ = "0.1.0"
