from ansible.module_utils._text import to_native
from traceback import format_exc
from scm.client import Scm

def get_scm_client(module):
    try:
        provider = module.params.get("provider")
        client_id = provider.get("client_id")
        client_secret = provider.get("client_secret")
        tsg_id = provider.get("tsg_id")
        log_level = provider.get("log_level", "INFO")

        client = Scm(
            client_id=client_id,
            client_secret=client_secret,
            tsg_id=tsg_id,
            log_level=log_level,
        )
        return client
    except Exception as e:
        module.fail_json(msg=to_native(e), exception=format_exc())
