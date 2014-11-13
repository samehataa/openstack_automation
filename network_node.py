#!/usr/bin/env python2.7
from JumpScale import j
import requests
import json
import time
import JumpScale.baselib.remote
publicip="??"
network_user="??"
network_pass="??"
controller_ip="??"
compute1_ip="??"
network_ip="??"
j.remote.fabric.setHost('%s@%s:2223'%(network_user, publicip,))
j.remote.fabric.setDefaultPasswd(network_pass, '%s@%s:2223'%(network_user, publicip))
j.remote.fabric.api.sudo('echo "network" > /etc/hostname')
j.remote.fabric.api.sudo('echo "auto eth1" >> /etc/network/interfaces')
j.remote.fabric.api.sudo('echo "iface eth1 inet static" >> /etc/network/interfaces')
j.remote.fabric.api.sudo('echo "\taddress 192.168.9.2" >> /etc/network/interfaces')
j.remote.fabric.api.sudo('echo "\tnetmask 255.255.255.0" >> /etc/network/interfaces')
j.remote.fabric.api.sudo('echo -e "%s\tcontroller" >> /etc/hosts'%(controller_ip,))
j.remote.fabric.api.sudo('echo -e "%s\tcompute1" >> /etc/hosts'%(compute1_ip,))
j.remote.fabric.api.sudo('echo -e "%s\tnetwork" >> /etc/hosts'%(network_ip,))
j.remote.fabric.api.sudo('apt-get install ntp -y')
j.remote.fabric.api.sudo('sed -i \'s/server/#server/\' /etc/ntp.conf')
j.remote.fabric.api.sudo('sed -i \'/#server ntp.ubuntu.com/a server controller\' /etc/ntp.conf')
j.remote.fabric.api.sudo('echo "net.ipv4.ip_forward=1" >> /etc/sysctl.conf')
j.remote.fabric.api.sudo('echo "net.ipv4.conf.all.rp_filter=0" >> /etc/sysctl.conf')
j.remote.fabric.api.sudo('echo "net.ipv4.conf.default.rp_filter=0" >> /etc/sysctl.conf')
j.remote.fabric.api.sudo('sysctl -p')
j.remote.fabric.api.sudo('apt-get install python-software-properties -y')
j.remote.fabric.api.sudo('echo "deb http://ubuntu-cloud.archive.canonical.com/ubuntu trusty-updates/juno main" > /etc/apt/sources.list.d/ubuntu-cloud-archive-juno-trusty.list')
j.remote.fabric.api.sudo('apt-get install ubuntu-cloud-keyring -y')
j.remote.fabric.api.sudo('apt-get install debconf-utils -y')
j.remote.fabric.api.sudo('echo -e "grub\tgrub/update_grub_changeprompt_threeway\tselect\tinstall_new" | debconf-set-selections')
j.remote.fabric.api.sudo('echo -e "grub-legacy-ec2\tgrub/update_grub_changeprompt_threeway\tselect\tinstall_new" | debconf-set-selections')
j.remote.fabric.api.sudo('apt-get update -y && apt-get dist-upgrade')
j.remote.fabric.api.sudo(' apt-get install neutron-plugin-ml2 neutron-plugin-openvswitch-agent neutron-l3-agent neutron-dhcp-agent -y')
#########/etc/neutron/neutron.conf
j.remote.fabric.api.sudo('sed -i \'/^\[DEFAULT\]/a rabbit_host = controller\' /etc/neutron/neutron.conf')
j.remote.fabric.api.sudo('sed -i \'/^\[DEFAULT\]/a rabbit_password = testpass\' /etc/neutron/neutron.conf')
j.remote.fabric.api.sudo('sed -i \'/^\[DEFAULT\]/a auth_strategy = keystone\' /etc/neutron/neutron.conf')
j.remote.fabric.api.sudo('sed -i \'s/^auth_uri/#auth_uri/\' /etc/neutron/neutron.conf')
j.remote.fabric.api.sudo('sed -i \'s/^admin_password/#admin_password/\' /etc/neutron/neutron.conf')
j.remote.fabric.api.sudo('sed -i \'s/^admin_user/#admin_user/\' /etc/neutron/neutron.conf')
j.remote.fabric.api.sudo('sed -i \'s/^admin_tenant_name/#admin_tenant_name/\' /etc/neutron/neutron.conf')
j.remote.fabric.api.sudo('sed -i \'s/^identity_uri/#identity_uri/\' /etc/neutron/neutron.conf')
j.remote.fabric.api.sudo('sed -i \'/^\[keystone_authtoken\]/a admin_password = testpass\' /etc/neutron/neutron.conf')
j.remote.fabric.api.sudo('sed -i \'/^\[keystone_authtoken\]/a admin_user = neutron\' /etc/neutron/neutron.conf')
j.remote.fabric.api.sudo('sed -i \'/^\[keystone_authtoken\]/a admin_tenant_name = service\' /etc/neutron/neutron.conf')
j.remote.fabric.api.sudo('sed -i \'/^\[keystone_authtoken\]/a identity_uri = http://controller:35357\' /etc/neutron/neutron.conf')
j.remote.fabric.api.sudo('sed -i \'/^\[keystone_authtoken\]/a auth_uri = http://controller:5000/v2.0\' /etc/neutron/neutron.conf')
j.remote.fabric.api.sudo('sed -i \'s/^core_plugin/#core_plugin/\' /etc/neutron/neutron.conf')
j.remote.fabric.api.sudo('sed -i \'/^\[DEFAULT\]/a core_plugin = ml2\' /etc/neutron/neutron.conf')
j.remote.fabric.api.sudo('sed -i \'/^\[DEFAULT\]/a service_plugins = router\' /etc/neutron/neutron.conf')
j.remote.fabric.api.sudo('sed -i \'/^\[DEFAULT\]/a allow_overlapping_ips = True\' /etc/neutron/neutron.conf')
#######another config file : /etc/neutron/plugins/ml2/ml2_conf.ini
j.remote.fabric.api.sudo('sed -i \'/^\[ml2\]/a type_drivers = flat,gre \' /etc/neutron/plugins/ml2/ml2_conf.ini')
j.remote.fabric.api.sudo('sed -i \'/^\[ml2\]/a tenant_network_types = gre \' /etc/neutron/plugins/ml2/ml2_conf.ini')
j.remote.fabric.api.sudo('sed -i \'/^\[ml2\]/a mechanism_drivers = openvswitch \' /etc/neutron/plugins/ml2/ml2_conf.ini')
j.remote.fabric.api.sudo('sed -i \'/^\[ml2_type_gre\]/a tunnel_id_ranges = 1:1000 \' /etc/neutron/plugins/ml2/ml2_conf.ini')
j.remote.fabric.api.sudo('sed -i \'/^\[securitygroup\]/a enable_security_group = True\' /etc/neutron/plugins/ml2/ml2_conf.ini')
j.remote.fabric.api.sudo('sed -i \'/^\[securitygroup\]/a enable_ipset = True \' /etc/neutron/plugins/ml2/ml2_conf.ini')
j.remote.fabric.api.sudo('sed -i \'/^\[securitygroup\]/a firewall_driver = neutron.agent.linux.iptables_firewall.OVSHybridIptablesFirewallDriver\' /etc/neutron/plugins/ml2/ml2_conf.ini')
j.remote.fabric.api.sudo('sed -i \'/^\[ml2_type_flat\]/a flat_networks = external \' /etc/neutron/plugins/ml2/ml2_conf.ini')
j.remote.fabric.api.sudo('sed -i \'/^\[ovs\]/a local_ip = 192.168.9.2 \' /etc/neutron/plugins/ml2/ml2_conf.ini')
j.remote.fabric.api.sudo('sed -i \'/^\[ovs\]/a tunnel_type = gre \' /etc/neutron/plugins/ml2/ml2_conf.ini')
j.remote.fabric.api.sudo('sed -i \'/^\[ovs\]/a enable_tunneling = True \' /etc/neutron/plugins/ml2/ml2_conf.ini')
j.remote.fabric.api.sudo('sed -i \'/^\[ovs\]/a bridge_mappings = external:br-ex \' /etc/neutron/plugins/ml2/ml2_conf.ini')
########another config file : /etc/neutron/l3_agent.ini
j.remote.fabric.api.sudo('sed -i \'/^\[DEFAULT\]/a interface_driver = neutron.agent.linux.interface.OVSInterfaceDriver\' /etc/neutron/l3_agent.ini')
j.remote.fabric.api.sudo('sed -i \'/^\[DEFAULT\]/a use_namespaces = True \' /etc/neutron/l3_agent.ini')
j.remote.fabric.api.sudo('sed -i \'/^\[DEFAULT\]/a external_network_bridge = br-ex \' /etc/neutron/l3_agent.ini')
#######another config file : /etc/neutron/dhcp_agent.ini
j.remote.fabric.api.sudo('sed -i \'/^\[DEFAULT\]/a interface_driver = neutron.agent.linux.interface.OVSInterfaceDriver\' /etc/neutron/dhcp_agent.ini')
j.remote.fabric.api.sudo('sed -i \'/^\[DEFAULT\]/a dhcp_driver = neutron.agent.linux.dhcp.Dnsmasq\' /etc/neutron/dhcp_agent.ini')
j.remote.fabric.api.sudo('sed -i \'/^\[DEFAULT\]/a use_namespaces = True\' /etc/neutron/dhcp_agent.ini')
j.remote.fabric.api.sudo('sed -i \'/^\[DEFAULT\]/a dnsmasq_config_file = /etc/neutron/dnsmasq-neutron.conf\' /etc/neutron/dhcp_agent.ini')
#####another config file /etc/neutron/dnsmasq-neutron.conf
j.remote.fabric.api.sudo(' echo "dhcp-option-force=26,1454" > /etc/neutron/dnsmasq-neutron.conf')
#j.remote.fabric.api.sudo('pkill dnsmasq')
############another config file: /etc/neutron/metadata_agent.ini
j.remote.fabric.api.sudo('sed -i \'/^\[DEFAULT\]/a admin_password = testpass\' /etc/neutron/metadata_agent.ini')
j.remote.fabric.api.sudo('sed -i \'/^\[DEFAULT\]/a admin_user = neutron\' /etc/neutron/metadata_agent.ini')
j.remote.fabric.api.sudo('sed -i \'/^\[DEFAULT\]/a admin_tenant_name = service\' /etc/neutron/metadata_agent.ini')
j.remote.fabric.api.sudo('sed -i \'/^\[DEFAULT\]/a auth_region = regionOne\' /etc/neutron/metadata_agent.ini')
j.remote.fabric.api.sudo('sed -i \'/^\[DEFAULT\]/a auth_url = http://controller:5000/v2.0\' /etc/neutron/metadata_agent.ini')
j.remote.fabric.api.sudo('sed -i \'/^\[DEFAULT\]/a nova_metadata_ip = controller\' /etc/neutron/metadata_agent.ini')
j.remote.fabric.api.sudo('sed -i \'/^\[DEFAULT\]/a metadata_proxy_shared_secret = testpass\' /etc/neutron/metadata_agent.ini')
j.remote.fabric.api.sudo('service openvswitch-switch restart')
j.remote.fabric.api.sudo('ovs-vsctl add-br br-ex')
j.remote.fabric.api.sudo('ovs-vsctl add-port br-ex eth2')
j.remote.fabric.api.sudo('service neutron-plugin-openvswitch-agent restart')
j.remote.fabric.api.sudo('service neutron-l3-agent restart')
j.remote.fabric.api.sudo('service neutron-dhcp-agent restart')
j.remote.fabric.api.sudo('service neutron-metadata-agent restart')
