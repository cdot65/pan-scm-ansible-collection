# -*- coding: utf-8 -*-

# This code is part of Ansible, but is an independent component.
# This particular file snippet, and this file snippet only, is Apache2.0 licensed.
# Modules you write using this snippet, which is embedded dynamically by Ansible
# still belong to the author of the module, and may assign their own license
# to the complete work.
#
# Copyright (c) 2024 Calvin Remsburg (@cdot65)
# All rights reserved.

"""
Ansible module for managing address objects in SCM.

This module provides functionality to create, update, and delete address objects
in the SCM (Security Control Manager) system. It handles various address types
and supports check mode operations.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible.module_utils._text import to_text
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.cdot65.scm.plugins.module_utils.api_spec import ScmSpec  # noqa: F401
from ansible_collections.cdot65.scm.plugins.module_utils.authenticate import get_scm_client  # noqa: F401
from ansible_collections.cdot65.scm.plugins.module_utils.serialize_response import serialize_response  # noqa: F401
from scm.config.objects.address import Address
from scm.exceptions import NotFoundError


def build_address_data(module_params):
    """
    Build address data dictionary from module parameters.

    Args:
        module_params (dict): Dictionary of module parameters

    Returns:
        dict: Filtered dictionary containing only relevant address parameters
    """
    return {k: v for k, v in module_params.items() if k not in ['provider', 'state'] and v is not None}


def get_existing_address(address_api, address_data):
    """
    Attempt to fetch an existing address object.

    Args:
        address_api: Address API instance
        address_data (dict): Address parameters to search for

    Returns:
        tuple: (bool, object) indicating if address exists and the address object if found
    """
    try:
        existing = address_api.fetch(
            name=address_data['name'],
            folder=address_data.get('folder'),
            snippet=address_data.get('snippet'),
            device=address_data.get('device'),
        )
        return True, existing
    except NotFoundError:
        return False, None


def main():
    """
    Main execution path for the address object module.
    """
    module = AnsibleModule(
        argument_spec=ScmSpec.address_spec(),
        supports_check_mode=True,
    )

    try:
        client = get_scm_client(module)
        address_api = Address(client)

        address_data = build_address_data(module.params)
        exists, existing_address = get_existing_address(
            address_api,
            address_data,
        )

        if module.params['state'] == 'present':
            if not exists:
                if not module.check_mode:
                    result = address_api.create(data=address_data)
                    module.exit_json(
                        changed=True,
                        address=serialize_response(result),
                    )
                module.exit_json(changed=True)
            else:
                # Compare and update if needed
                need_update = False  # TODO: Implement comparison logic here
                if need_update and not module.check_mode:
                    result = address_api.update(address=existing_address)
                    module.exit_json(
                        changed=True,
                        address=serialize_response(result),
                    )
                module.exit_json(
                    changed=False,
                    address=serialize_response(existing_address),
                )

        elif module.params['state'] == 'absent':
            if exists:
                if not module.check_mode:
                    address_api.delete(str(existing_address.id))
                module.exit_json(changed=True)
            module.exit_json(changed=False)

    except Exception as e:
        module.fail_json(msg=to_text(e))


if __name__ == '__main__':
    main()
