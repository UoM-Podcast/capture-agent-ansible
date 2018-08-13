from ansible.module_utils.basic import *
import requests
from requests.auth import HTTPDigestAuth

# WORKFLOW_ENDPOINT = OPENCAST_ADMIN_SERVER + "/workflow/instances.json?state=hold&op={}&count={}"

def opencast_workflow(data):

    headers = {'X-Requested-Auth': 'Digest'}
    endp = data['server'] + data['workflow_endpoint'] + data['workflow_id'] + '.json'
    print endp
    result = requests.get(endp, headers=headers, auth=HTTPDigestAuth(data['username'], data['password']))

    if result.status_code == 200:
        if result.json()['workflow']['state'] == "SUCCEEDED":
            return False, True, result.json()
        else:
            return True, False, "workflow has not succeeded"
    if result.status_code == 401:
        return True, False, result.status_code
    if result.status_code == 400:
        return True, False, result.status_code
    if result.status_code == 404:
        return True, False, result.status_code
        # default: something went wrong
    meta = {"status": result.status_code, 'response': result.status_code}
    return True, False, meta


def main():

    fields = {
        "server": {"required": True, "type": "str"},
        "username": {"required": True, "type": "str"},
        "password": {"required": True, "type": "str"},
        "workflow_endpoint": {"default": "/workflow/instance/", "type": "str"},
        "workflow_id": {"required": True, "type": "str"}
    }


    module = AnsibleModule(argument_spec=fields)
    is_error, has_changed, result = opencast_workflow(module.params)

    if not is_error:
        module.exit_json(changed=has_changed, meta=result)
    else:
        module.fail_json(msg="Error looking up workflow instance for opencast event", meta=result)


if __name__ == '__main__':
    main()