from typing import Dict, Any


class ScmSpec:
    """API specifications for SCM Ansible modules."""

    @staticmethod
    def address_spec() -> Dict[str, Any]:
        """Returns Ansible module spec for address objects."""
        return dict(
            name=dict(
                type='str',
                required=True,
            ),
            description=dict(
                type='str',
                required=False,
            ),
            tag=dict(
                type='list',
                elements='str',
                required=False,
            ),
            ip_netmask=dict(
                type='str',
                required=False,
            ),
            ip_range=dict(
                type='str',
                required=False,
            ),
            ip_wildcard=dict(
                type='str',
                required=False,
            ),
            fqdn=dict(
                type='str',
                required=False,
            ),
            folder=dict(
                type='str',
                required=False,
            ),
            snippet=dict(
                type='str',
                required=False,
            ),
            device=dict(
                type='str',
                required=False,
            ),
            provider=dict(
                type='dict',
                required=True,
                options=dict(
                    client_id=dict(
                        type='str',
                        required=True,
                    ),
                    client_secret=dict(
                        type='str',
                        required=True,
                        no_log=True,
                    ),
                    tsg_id=dict(
                        type='str',
                        required=True,
                    ),
                    log_level=dict(
                        type='str',
                        required=False,
                        default='INFO',
                    ),
                ),
            ),
            state=dict(
                type='str',
                choices=['present', 'absent'],
                required=True,
            ),
        )
