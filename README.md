# vagrant-inventory
Ansible dynamic inventory for vagrant

## usage
Just use this script as inventory

```bash
cd vagrant

ansible-playbook -i vagrant-inventory.py all -m ping
```
