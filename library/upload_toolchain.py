#!/usr/bin/python3

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

import sys, os
sys.path.append('/var/tmp/f5-ansible/')


import requests, json, time, bigip
from ansible.module_utils.basic import AnsibleModule


if __name__ == '__main__':
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        server=dict(type='str', required=True),
        token=dict(type='str', required=True),
        package=dict(type='str', required=True)
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # change is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        ok=False,
        changed=False,
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)

    # use whatever logic you need to determine whether or not this module
    # made any modifications to your target
    host = module.params['server']
    file = module.params['package']
    token = module.params['token']
    f5ve = bigip.tmos(host, token = token)
    if f5ve.upload('/mgmt/shared/file-transfer/uploads/', file) == 0:
        module.fail_json(msg='Upload Failed', **result)
    task_id = f5ve.iapplx_install_package(file)
    if task_id == "":
        module.fail_json(msg='Install Failed', **result)
    
    result['json'] = {"Task_id": task_id }
    install_result = 1
    timeout = time.time() + 5*60
    while f5ve.iapplx_check_task_status(task_id) != 1:
        if time.time() > timeout:
            install_result = 0
            break
        time.sleep(15)
 
    if install_result == 1:
      result['ok'] = True
      result['changed'] = False
      result['failed'] = False
      module.exit_json(**result)
    else:
      module.fail_json(msg='Validation Failed', **result)
