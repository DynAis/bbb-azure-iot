import sys
sys.path.insert(0, "..")

import logging
import asyncio
import time

import opc_2_bbb_bridge as o2b
import azure_table_client as table_client

from opcua import Client


async def opc_set_node_value(client: Client,dit:dict) :
    objects = client.get_objects_node() 
    global_object = objects.get_children()[-1]
    
    try:
        for obj in global_object.get_children(): # traverse all the nodes
            var = obj.get_data_value() # get the original node
            name = str(obj.get_browse_name())[16:len(str(obj.get_browse_name()))-1] # get the node's name
            value = var.Value.Value # get the node's value
            if name in dit:
                if (dit[name] != int(value)): #if the value changed
                    if (1 in obj.get_access_level()):
                    # if (name in if_writeable and if_writeable[name]) :
                    # # check the node wheather is writable
                        # print(obj.get_access_level())
                        print("the value of node "+str(name) +" has changed to: "+ str(dit[name]))
                        obj.set_value(dit[name])
                    else:
                        print("the node "+str(name)+" is not writable")
            
            # obj.set_value(dit[name])
    except Exception as e:
        print(e)
                
    # finally:
    #     client.disconnect()


# if __name__ == "__main__":
#     logging.basicConfig(level=logging.WARN)
#     server_url = "opc.tcp://localhost:12345"
#     loop = asyncio.get_event_loop()
#     client=loop.run_until_complete(o2b.opc_connect(server_url))
#     while True:
#         dic = loop.run_until_complete(table_client.line_processing(query_filter,connection_string, table_name))
#         asyncio.run(opc_set_node_value(client,dic))
#         loop.run_until_complete(opc_set_node_value(client, dic) )
#         time.sleep(5)

    # 
    