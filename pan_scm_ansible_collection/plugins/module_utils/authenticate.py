from traceback import format_exc

from ansible.module_utils._text import to_native
from scm.client import Scm
from scm.exceptions import AuthenticationError


def get_scm_client(module):
    """
    Initialize SCM client with proper error handling.
    """
    try:
        provider = module.params["provider"]
        client = Scm(
            client_id=provider["client_id"],
            client_secret=provider["client_secret"],
            tsg_id=provider["tsg_id"],
            log_level=provider.get("log_level", "INFO"),
        )
        return client
    except AuthenticationError as e:
        module.fail_json(
            msg=f"Authentication failed: {to_native(e)}",
            error_code=getattr(e, 'error_code', None),
            http_status=getattr(e, 'http_status_code', None),
        )
    except Exception as e:
        module.fail_json(msg=to_native(e), exception=format_exc())
