"""Functionality serving to inspect the Client's Sym Deployment.  These are primarily intended for
clients themselves writing Templates and Integrations"""
from typing import Dict, Optional

from sym.sdk.errors import SymSystemError
from sym.sdk.user import User
from sym.sdk._internal.integrations.sym_handler import SymHandler, SymHandlerErrors
from sym.sdk._internal.utils import wrap_with_typed_error

@wrap_with_typed_error(SymSystemError, SymHandlerErrors)
def get_flows(
    user_id: str,
    org_id: str,
    environment_name: Optional[str] = None,
    flow_name: Optional[str] = None,
    show_all_environments: bool = False,
) -> Dict[str, dict]:
    """Accessor for the collection of flows visible to the given user/suborganization.

    Args:
        user_id: The user on who's behalf flows are being sought.
        org_id: Suborganization of the organization hosting this deployment. An exception
                will be thrown if this does not match the hosting organization structure and privileges.
        environment_name: If set, filters out flows to the specified environment.
                            Otherwise implicitly filters to the client's main ("prod") environment
        flow_name: Selects the given flow name, error if not found.
        show_all_environments: Ignore environments and show all specified flows across all environments

    Returns:
        Dict[str, dict]: Flow details keyed by Flow slugs
    """
    return SymHandler.get_handler().get_flows(user_id, org_id, environment_name, flow_name)
"""Introspection tools and helpers for the Sym API."""

from typing import Optional




def debug(message: str, *, user: Optional[User] = None):
    """Send a debug message.

    This method takes a message and sends it to a :class:`~sym.sdk.user.User`
    via an appropriate channel (e.g. Slack).

    It can be helpful to debug the output of various Integrations.

    Args:
        user: The :class:`~sym.sdk.user.User` to send the message to. Defaults to the Implementer of this Flow.
    """
