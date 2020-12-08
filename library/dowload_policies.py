#!/usr/bin/python

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

import sys
sys.path.append('/root/git/f5-ansible/module_utils')
import requests, json, os, time, bigip
from ansible.module_utils.basic import AnsibleModule


if __name__ == '__main__':
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        server = dict(type='str', required=True),
        token = dict(type='str', required=True),
        directory = dict(type='str', required=True)
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
    #if module.check_mode:
    #    module.exit_json(**result)

    # use whatever logic you need to determine whether or not this module
    # made any modifications to your target
    host = module.params['server']
    directory = module.params['directory']
    token = module.params['token']
    bigip_device = bigip.tmos(host, token = token)
    bigip_device.update_session_timeout(3600)
    asm_device=bigip.asm(bigip_device)

    if bigip_device.upload('/mgmt/shared/file-transfer/uploads/', file) == 0:
        module.fail_json(msg='Upload Failed', **result)
    f5ve.install_custom_monitor(file)
    install_result = 1
    bigip_asm.get_policy_list()
    asm_policy_list_length = len(bigip_asm.policies)
    file_list = []
    for index, p in enumerate(bigip_asm.policies, start=1):
      print('['+ str(index) +'/' + str(asm_policy_list_length) +'] - Policy ' + p[1])
      filename = p[0] + '.xml'
      res = bigip_device.post('/mgmt/tm/asm/tasks/export-policy', {"filename": filename,"policyReference":{"link":"https://localhost/mgmt/tm/asm/policies/" + p[0]}})
      export_id = res.json()['id']
      while res.json()['status'] != 'COMPLETED':
        res = bigip_device.get('/mgmt/tm/asm/tasks/export-policy/' + export_id)
        time.sleep(5)
      bigip_device.download('/mgmt/tm/asm/file-transfer/downloads/', os.path.join(directory, filename))
      file_list.append ({'file' : os.path.join(directory, filename), 'policy_name' : p[1]})


    if install_result == 1:
      result['json'] = file_list
      result['ok'] = True
      result['changed'] = False
      result['failed'] = False
      module.exit_json(**result)
    else:
      module.fail_json(msg='Validation Failed', **result)
