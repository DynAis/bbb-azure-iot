import sys
sys.path.insert(0, "..")

import logging
import asyncio

import opc_2_bbb_bridge as o2b

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
                # obj 生成一个枚举类型的集合 
                # {<AccessLevel.CurrentRead: 0>, <AccessLevel.CurrentWrite: 1>} 可写
                # {<AccessLevel.CurrentRead: 0>}#不可写
                if dit[name] is not value: #if the value changed
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
                
    finally:
        # if dit[name] is not value: #if the value changed
        #             print("the value of node "+str(name) +" has changed to: "+ str(dit[name]))
        client.disconnect()
            


# def set_node(client, var):
#     try:
#         static_node = client.get_node("ns=3;s=\"Sort\".\"hmi\".\"bsHand\"")
#         static_node.set_value(var)
#     except Exception as e:
#         print(e)
#     finally:
#         print("Successfully write the value")


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARN)
    server_url = "opc.tcp://localhost:12345"
    d = {'bertieb_Hand': True,'Hoehe_messung': 555} # !!!
    dit = {'bertieb_Hand': True, 
        'bertieb_Auto': False, 
        'start': True, 
        'stop': False, 
        'Quit': True, 
        'inductive_counter': 1, 
        'total_inductive_counter': 2, 
        'capactive_counter': 233, 
        'total_capactive_counter': 3, 
        'zu_hoch': 123, 
        'total_zu_hoch': 4, 
        'optisch_counter': 5, 
        'total_optisch_counter': 6, 
        'Hoehe_messung': 555, # !!!
        # "User does not have permission to perform the requested operation."(BadUserAccessDenied)
        'Alarm': True}

    c=asyncio.run(o2b.opc_connect(server_url))
    asyncio.run(opc_set_node_value(c,d) )
    # set_node(c,True)