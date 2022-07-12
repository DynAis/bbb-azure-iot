import logging
import asyncio

from opcua import Client



# start to connect the opcua server
async def opc_connect(server_url: str) -> Client:
    client = Client(server_url)
    try:
        print('start to connect opcua server: ' + server_url)
        client.connect()
        print('connect established\n')
        # client.load_type_definitions()  # load definition of server specific structures/extension objects
    except Exception as e:
        print(e)
    finally:
        # client.disconnect()
        # print('server disconnected')
        return client



# get all the needed nodes and return as a dict 
async def opc_get_all_node_value(client: Client) -> dict:
    objects = client.get_objects_node() 
    global_object = objects.get_children()[-1]
    # global_object = client.get_node('ns=3,s=Outputs')
    
    dic = {}
    for obj in global_object.get_children(): # traverse all the needed nodes
        # static_node = client.get_node(node)

        var = obj.get_data_value() # get the node as a DataValue object
        name = str(obj.get_browse_name())[16:len(str(obj.get_browse_name()))-1] # get the node's name
        value = var.Value.Value # get the node's value

        dic[name] = value 

    return dic 
    
# disconnect the opcua client
async def opc_disconnect(client: Client):
    assert client is not None, "opcua client is None"
    await client.disconnect()

if __name__ == "__main__":
    logging.basicConfig(level=logging.WARN)
    server_url = "opc.tcp://10.136.4.101:4840"
    c=asyncio.run(opc_connect(server_url))

    print(asyncio.run(opc_get_all_node_value(c)))
