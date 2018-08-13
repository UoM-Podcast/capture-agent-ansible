# Capture Agent Configuration #

Ansible configuration management for UoM IT Services Lecture Capture Captures Agents.

### Resources ###
* [Ansible](http://docs.ansible.com)

### Running ###
local running Ansible version ansible 2.1.2.0 + required
remote using ubuntu 16.04
remote configured with the user 'galicaster'
remote user configured with root level key based ssh access
An ssh key file to access the root account on the remote client

### Examples ###
all hosts:
```
ansible-playbook capture-agent.yml -i hosts --private-key=~/.ssh/ca-ansible --ask-vault-pass

```
all staging hosts:
```
ansible-playbook capture-agent.yml -i hosts --private-key=~/.ssh/ca-ansible --ask-vault-pass

```
just a single host:
```
ansible-playbook capture-agent.yml -i hosts --private-key=~/.ssh/ca-ansible --ask-vault-pass --limit mtt-test-a

```
specific tag:
```
ansible-playbook capture-agent.yml -i hosts --private-key=~/.ssh/ca-ansible --ask-vault-pass --limit mtt-test-a --tags apt,galicaster

```
just wifi hosts as a subset:

```
ansible-playbook capture-agent.yml -i hosts --private-key=~/.ssh/ca-ansible --ask-vault-pass --limit capture-agents-datapath-split-wifi:capture-agents-datapath-usb-wifi:capture-agents-blackmagic-split-wifi:capture-agents-blackmagic-usb-wifi

```

reinstall hosts (must be on 12.04, precise):
```
ansible-playbook capture-agent.yml -i hosts --private-key=~/.ssh/ca-ansible --ask-vault-pass -e reinstall_os=true

```
the special variables are:
```
reinstall_os=true (reinstall the os if precise)
do_hard_reboot=true (force a shutdown and wakeup on RTC timer)
upgrade_os=true (apt-get dist upgrade)

```

You can also set ANSIBLE_VAULT_PASSWORD_FILE environment variable, e.g. ```export ANSIBLE_VAULT_PASSWORD_FILE=~/.vault_pass.txt``` and Ansible will automatically search for the password in that file.

### Running On Staging/production Operations nodes ###
All the env vars have been set ready to use, this cuts down on the amount of typing and more importantly prohibits accidental production runs on a staging environment.
```
ansible-playbook capture-agent.yml --limit <comma separated list of hosts> --tags <comma separated list of tags> --skip-tags <comma separated list of tags to skip>

```
To run, specifying a hosts file (e.g running prod ansible on staging):
```
ansible-playbook capture-agent.yml -i hosts --limit <comma separated list of hosts> --tags <comma separated list of tags> --skip-tags <comma separated list of tags to skip>

```
To get a list of tags:
```
ansible-playbook capture-agent.yml --list-tags

```
Example, updating a galicaster conf.ini parameter on evey staging agent:
```
ansible-playbook capture-agent.yml --limit mtt-test-* --tags galicaster_config --skip-tags cronjobs,scripts

```
