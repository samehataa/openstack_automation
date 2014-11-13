openstack
=========

Open stack automated installation

The repo contains 3 scripts to Configure the basic setup of the openstack as follow:

1- controller_node.py : to configure the controller node

2- compute_node.py: to configure the compute node

3- network_node.py: to configure the network node

Steps:

1- add the controller ip & user & password to the controller_node.py and run it

2- make sure that the network node and the compute node have another network interface

3- add the compute ip & user & password to the compute_node.py script and run it

4- add the network ip & user & password to the network_node.py script and run it

5- Test the setup with the test image

