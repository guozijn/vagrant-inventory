#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2019 Zijian Guo <guozijian@unitedstack.com>
# Copyright 2019 UnitedStack
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import subprocess
import sys


def get_vagrant_hosts():
    p = subprocess.Popen("vagrant ssh-config", stdout=subprocess.PIPE, shell=True)
    raw = p.communicate()[0]
    lines = raw.split("\n\n")
    vagrant_hosts = list()
    for line in lines:
        if line != '':
            sshconfig = dict()
            host_detail = line.strip().split("\n")
            for host_param in host_detail:
                kv = host_param.strip().split(' ')
                if len(kv) == 2:
                    sshconfig[kv[0]] = kv[1]
            vagrant_hosts.append(sshconfig)
    return vagrant_hosts


def to_ansible_inventory(hosts):
    ansible_hosts = dict()
    hosts_list = list()
    hosts_vars = dict()

    for host in hosts:
        hosts_list.append(host.get('Host'))
        hosts_vars[host.get('Host')] = {
            "ansible_ssh_host": host.get('HostName'),
            "ansible_ssh_port": host.get('Port'),
            "ansible_ssh_user": host.get('User'),
            "ansible_ssh_private_key_file": host.get('IdentityFile')
        }

    ansible_hosts['vagrant'] = {
        "hosts": hosts_list
    }

    ansible_hosts['_meta'] = {
        "hostvars": hosts_vars
    }

    return ansible_hosts


def main():
    output = to_ansible_inventory(get_vagrant_hosts())
    if sys.argv[1] == '--list':
        print(json.dumps(output))
    elif sys.argv[1] == '--host':
        print(json.dumps(output.get('_meta').get('hostvars').get(sys.argv[2])))
    else:
        print('Invalid argument.')


if __name__ == '__main__':
    main()
