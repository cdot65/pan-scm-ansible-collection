#!/usr/bin/python
"""Ansible module for managing address objects in SCM."""
from __future__ import absolute_import, division, print_function

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.cdot65.scm.plugins.module_utils.api_spec import ScmSpec  # noqa: F401
from ansible_collections.cdot65.scm.plugins.module_utils.authenticate import get_scm_client  # noqa: F401
from scm.config.objects.address import Address
from scm.exceptions import NotFoundError


def serialize_response(response):
    """Convert response to Ansible-compatible format."""
    if hasattr(response, 'model_dump'):
        data = response.model_dump()
        # Convert UUID to string
        if 'id' in data and data['id']:
            data['id'] = str(data['id'])
        return data
    return response


def main():
    module = AnsibleModule(argument_spec=ScmSpec.address_spec(), supports_check_mode=True)

    try:
        client = get_scm_client(module)
        address_api = Address(client)

        # Build address data from module parameters
        address_data = {k: v for k, v in module.params.items() if k not in ['provider', 'state'] and v is not None}

        try:
            existing_address = address_api.fetch(
                name=address_data['name'], folder=address_data.get('folder'), snippet=address_data.get('snippet'), device=address_data.get('device')
            )
            exists = True
        except NotFoundError:
            exists = False

        if module.params['state'] == 'present':
            if not exists:
                if not module.check_mode:
                    result = address_api.create(data=address_data)
                    module.exit_json(changed=True, address=serialize_response(result))
                else:
                    module.exit_json(changed=True)
            else:
                # Compare and update if needed
                need_update = False
                if need_update and not module.check_mode:
                    result = address_api.update(address=existing_address)
                    module.exit_json(changed=True, address=serialize_response(result))
                module.exit_json(changed=False, address=serialize_response(existing_address))

        elif module.params['state'] == 'absent':
            if exists:
                if not module.check_mode:
                    address_api.delete(str(existing_address.id))
                module.exit_json(changed=True)
            module.exit_json(changed=False)

    except Exception as e:
        module.fail_json(msg=str(e))


if __name__ == '__main__':
    main()
