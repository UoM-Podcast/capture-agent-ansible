from ansible.module_utils.basic import *
import requests
from requests.auth import HTTPDigestAuth
import datetime

dubs = '<?xml version="1.0" encoding="UTF-8"?><dublincore xmlns="http://www.opencastproject.org/xsd/1.0/dublincore/" xmlns:dcterms="http://purl.org/dc/terms/"><dcterms:isPartOf>{}</dcterms:isPartOf><dcterms:license>Creative Commons 3.0: Attribution-NonCommercial-NoDerivs</dcterms:license><dcterms:temporal>start={}; end={}; scheme=W3C-DTF;</dcterms:temporal><dcterms:title>{}</dcterms:title><dcterms:spatial>{}</dcterms:spatial></dublincore>'

aparams = '#Capture Agent specific data\n' \
         '#{}\n' \
         'event.title={}\n' \
         'event.location={}\n' \
         'capture.device.names=defaults\n' \
         'event.series={}'

wfprop = 'org.opencastproject.workflow.config.emailAddresses=admin@localhost\n' \
         'org.opencastproject.workflow.config.archiveOp=false\n' \
         'org.opencastproject.workflow.config.videoPreview=false\n' \
         'org.opencastproject.workflow.config.usePublicStore=false\n' \
         'org.opencastproject.workflow.definition=manchester\n' \
         'org.opencastproject.workflow.config.publishHarvesting=true\n' \
         'org.opencastproject.workflow.config.publishEngage=true\n' \
         'org.opencastproject.workflow.config.trimHold=false'


def opencast_schedule(data):
    # Create and ingest the mediapackage POST request to opencast ingest endpoint
    url = data['server'] + data['schedule_endpoint']
    dublincore_submit = dubs.format(data['series'], data['time_start'],data['time_end'], data['title'], data['location'])
    agentparams_submit = aparams.format(datetime.datetime.now(), data['title'], data['location'], data['series'])
    # wfprops_submit = wfprop.format()

    headers = {'X-Requested-Auth': 'Digest'}
    postfield = {'dublincore': dublincore_submit, 'agentparameters': agentparams_submit, 'wfproperties': wfprop}

    result = requests.post(url, headers=headers, auth=HTTPDigestAuth(data['username'], data['password']), data=postfield)
    if result.status_code == 201:
        return False, True, result.headers['Location'].split('/')[-1].split('.')[0]
    if result.status_code == 401:
        return False, False, result.status_code
    if result.status_code == 400:
        return False, False, result.status_code
        # default: something went wrong
    meta = {"status": result.status_code, 'response': result.status_code}
    return True, False, meta


def main():

    fields = {
        "server": {"required": True, "type": "str"},
        "username": {"required": True, "type": "str"},
        "password": {"required": True, "type": "str"},
        "schedule_endpoint": {"default": "/recordings/", "type": "str"},
        "series": {"required": True, "type": "str"},
        "time_start": {"required": True, "type": "str"},
        "time_end": {"required": True, "type": "str"},
        "title": {"default": 'Test-schedule-ansible', "type": "str"},
        "location": {"required": True, "type": "str"},
    }


    module = AnsibleModule(argument_spec=fields)
    is_error, has_changed, result = opencast_schedule(module.params)

    if not is_error:
        module.exit_json(changed=has_changed, meta=result)
    else:
        module.fail_json(msg="Error scheduling opencast event", meta=result)


if __name__ == '__main__':
    main()
