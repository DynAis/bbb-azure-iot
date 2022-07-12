# BBB-Azure-IoT

It's a Teamproject in Ostfalia SS2022

Aim to use a BeagleBone-Black as a IoT device connector between local machine and Azure cloud server.
Temporary using simulated OPC-UA server as alternative to test out the workflow.

# Usage:

1. run `pip install -r requirement.txt` to install all requierments.
2. run `opc_server_simulation` to start opcua server
3. run `main.py`
4. check out the message in Azure

[update]:  
change the values in Azure Table storage and check the changes in simulated OPC-UA server

