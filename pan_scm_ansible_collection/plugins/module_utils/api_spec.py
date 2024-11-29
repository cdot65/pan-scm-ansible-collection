# -*- coding: utf-8 -*-

# This code is part of Ansible, but is an independent component.
# This particular file snippet, and this file snippet only, is Apache2.0 licensed.
# Modules you write using this snippet, which is embedded dynamically by Ansible
# still belong to the author of the module, and may assign their own license
# to the complete work.
#
# Copyright (c) 2024 Calvin Remsburg (@cdot65)
# All rights reserved.

from typing import Dict, Any


class ScmSpec:
    """
    API specifications for SCM Ansible modules.

    This class provides standardized specifications for SCM (Source Control Management)
    related Ansible modules, ensuring consistent parameter definitions and validation
    across the module collection.
    """

    @staticmethod
    def address_spec() -> Dict[str, Any]:
        """
        Returns Ansible module spec for address objects.

        This method defines the structure and requirements for address-related
        parameters in SCM modules.

        Returns:
            Dict[str, Any]: A dictionary containing the module specification with
                           parameter definitions and their requirements.
        """
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

    @staticmethod
    def address_group_spec():
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
            dynamic=dict(
                type='dict',
                required=False,
                options=dict(
                    filter=dict(
                        type='str',
                        required=True,
                    ),
                ),
            ),
            static=dict(
                type='list',
                elements='str',
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

    @staticmethod
    def application_spec() -> Dict[str, Any]:
        """Returns Ansible module spec for application objects."""
        return dict(
            name=dict(
                type='str',
                required=True,
            ),
            category=dict(
                type='str',
                required=False,
            ),
            subcategory=dict(
                type='str',
                required=False,
            ),
            technology=dict(
                type='str',
                required=False,
            ),
            risk=dict(
                type='str',
                required=False,
            ),
            description=dict(
                type='str',
                required=False,
            ),
            default_timeout=dict(
                type='int',
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
            tag=dict(
                type='list',
                elements='str',
                required=False,
            ),
            ports=dict(
                type='list',
                elements='str',
                required=False,
            ),
            transfers_files=dict(
                type='bool',
                required=False,
            ),
            has_known_vulnerabilities=dict(
                type='bool',
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

    @staticmethod
    def application_group_spec() -> Dict[str, Any]:
        """
        Returns Ansible module spec for application group objects.

        This method defines the structure and requirements for application group-related
        parameters in SCM modules.

        Returns:
            Dict[str, Any]: A dictionary containing the module specification with
                           parameter definitions and their requirements.
        """
        return dict(
            name=dict(
                type='str',
                required=True,
            ),
            members=dict(
                type='list',
                elements='str',
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

    @staticmethod
    def service_spec() -> Dict[str, Any]:
        """Returns Ansible module spec for service objects."""
        return dict(
            name=dict(
                type='str',
                required=True,
            ),
            protocol=dict(
                type='dict',
                required=False,
                options=dict(
                    tcp=dict(
                        type='dict',
                        required=False,
                        options=dict(
                            port=dict(
                                type='str',
                                required=True,
                            ),
                            override=dict(
                                type='dict',
                                required=False,
                                options=dict(
                                    timeout=dict(
                                        type='int',
                                        required=False,
                                        default=3600,
                                    ),
                                    halfclose_timeout=dict(
                                        type='int',
                                        required=False,
                                        default=120,
                                    ),
                                    timewait_timeout=dict(
                                        type='int',
                                        required=False,
                                        default=15,
                                    ),
                                ),
                            ),
                        ),
                    ),
                    udp=dict(
                        type='dict',
                        required=False,
                        options=dict(
                            port=dict(
                                type='str',
                                required=True,
                            ),
                            override=dict(
                                type='dict',
                                required=False,
                                options=dict(
                                    timeout=dict(
                                        type='int',
                                        required=False,
                                        default=30,
                                    ),
                                ),
                            ),
                        ),
                    ),
                ),
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
