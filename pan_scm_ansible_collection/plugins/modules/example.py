#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
from scm.client import Scm
from scm.config.objects import Address

def run_module():
    module_args = dict(
        name=dict(type='str', required=True),
        description=dict(type='str', required=False, default='')
    )

    result = dict(
        changed=False,
        original_message='',
        message=''
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    if module.check_mode:
        module.exit_json(**result)

    name = module.params['name']
    description = module.params['description']

    try:
        scm_client = Scm(
            client_id="client_id",
            client_secret="client_secret",
            tsg_id="tsg_id",
        )
        address_client = Address(scm_client)
        address_data = {
            "name": name,
            "description": description,
        }
        address_client.create(address_data)
        result['changed'] = True
        result['message'] = f'Repository {name} created successfully.'
    except Exception as e:
        module.fail_json(msg=str(e))

    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()