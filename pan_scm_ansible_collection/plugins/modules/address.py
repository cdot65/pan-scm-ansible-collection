from __future__ import absolute_import, division, print_function
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_native
from ansible_collections.cdot65.scm.plugins.module_utils.authenticate import get_scm_client
from scm.config.objects.address import Address
from scm.models.objects.address import AddressCreateModel
from scm.exceptions import NotFoundError
from pydantic import ValidationError

argument_spec = dict(
    name=dict(type='str', required=True),
    description=dict(type='str', required=False),
    tag=dict(type='list', elements='str', required=False),
    ip_netmask=dict(type='str', required=False),
    ip_range=dict(type='str', required=False),
    ip_wildcard=dict(type='str', required=False),
    fqdn=dict(type='str', required=False),
    folder=dict(type='str', required=False),
    snippet=dict(type='str', required=False),
    device=dict(type='str', required=False),
    provider=dict(
        type='dict',
        required=True,
        options=dict(
            client_id=dict(type='str', required=True),
            client_secret=dict(type='str', required=True),
            tsg_id=dict(type='str', required=True),
            log_level=dict(type='str', required=False, default='INFO'),
        ),
    ),
    state=dict(type='str', choices=['present', 'absent'], required=True),
)

def validate_params(module):
    params = module.params
    # Validate address types
    address_fields = ['ip_netmask', 'ip_range', 'ip_wildcard', 'fqdn']
    provided_address_fields = [field for field in address_fields if params.get(field)]
    if len(provided_address_fields) != 1:
        module.fail_json(msg="Exactly one of 'ip_netmask', 'ip_range', 'ip_wildcard', or 'fqdn' must be provided.")

    # Validate container types
    container_fields = ['folder', 'snippet', 'device']
    provided_container_fields = [field for field in container_fields if params.get(field)]
    if len(provided_container_fields) != 1:
        module.fail_json(msg="Exactly one of 'folder', 'snippet', or 'device' must be provided.")

def main():
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True,)
    validate_params(module)
    params = module.params

    # Get the SCM client
    client = get_scm_client(module)
    address_api = Address(client)

    # Build the data dictionary
    address_data = {
        'name': params['name'],
        'description': params.get('description'),
        'tag': params.get('tag'),
        'ip_netmask': params.get('ip_netmask'),
        'ip_range': params.get('ip_range'),
        'ip_wildcard': params.get('ip_wildcard'),
        'fqdn': params.get('fqdn'),
        'folder': params.get('folder'),
        'snippet': params.get('snippet'),
        'device': params.get('device'),
    }

    # Validate using Pydantic
    try:
        address_model = AddressCreateModel(**address_data)
    except ValidationError as e:
        module.fail_json(msg=str(e))

    # Check if the address exists
    try:
        existing_address = address_api.fetch(
            name=address_model.name,
            folder=address_model.folder,
            snippet=address_model.snippet,
            device=address_model.device,
        )
        address_exists = True
    except NotFoundError:
        address_exists = False

    if params['state'] == 'present':
        if not address_exists:
            # Create address
            try:
                result = address_api.create(data=address_data)
                module.exit_json(changed=True, address=result.model_dump())
            except Exception as e:
                module.fail_json(msg=str(e))


        else:
            # Compare existing and desired configurations
            need_update = False
            if existing_address.description != address_model.description:
                need_update = True
            # Add more comparison logic as needed

            if need_update:
                # Update address
                try:
                    result = address_api.update(address=address_model)
                    module.exit_json(changed=True, address=result.model_dump())
                except Exception as e:
                    module.fail_json(msg=str(e))
            else:
                module.exit_json(changed=False, address=existing_address.model_dump())

    elif params['state'] == 'absent':
        if address_exists:
            # Delete address
            try:
                address_api.delete(object_id=str(existing_address.id))
                module.exit_json(changed=True)
            except Exception as e:
                module.fail_json(msg=str(e))
        else:
            module.exit_json(changed=False)

if __name__ == '__main__':
    main()
