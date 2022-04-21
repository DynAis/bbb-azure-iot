import logging
import asyncio

from opcua import Client
from opcua import ua



# start to connect the opcua server
async def opc_connect(server_url: str) -> Client:
    client = Client(server_url)
    try:
        print('start to connect opcua server: ' + server_url)
        client.connect()
        print('connect established\n')
        # client.load_type_definitions()  # load definition of server specific structures/extension objects
    except:
        print("error occurred")
    finally:
        # client.disconnect()
        # print('server disconnected')
        return client



# get all the needed nodes and return as a dict 
async def opc_get_all_node_value(client: Client) -> dict:
    objects = client.get_objects_node() 
    global_object = objects.get_children()[-1]
    
    dic = {}
    for obj in global_object.get_children(): # traverse all the needed nodes
        # static_node = client.get_node(node)

        var = obj.get_data_value() # get the node as a DataValue object
        name = str(obj.get_browse_name())[16:len(str(obj.get_browse_name()))-1] # get the node's name
        value = var.Value.Value # get the node's value

        dic[name] = value 

    return dic 
    


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARN)
    server_url = "opc.tcp://localhost:12345"
    c=asyncio.run(opc_connect(server_url))

    print(asyncio.run(opc_get_all_node_value(c)))
