import sys
sys.path.insert(0, "..")
import logging
import time

# try:
#     from IPython import embed
# except ImportError:
#     import code

#     def embed():
#         vars = globals()
#         vars.update(locals())
#         shell = code.InteractiveConsole(vars)
#         shell.interact()

from opcua import Client
from opcua import ua

# define server IP address
server_url = "opc.tcp://opcua.demo-this.com:51210/UA/SampleServer"

class SubHandler(object):
    """
    Subscription Handler. To receive events from server for a subscription
    data_change and event methods are called directly from receiving thread.
    Do not do expensive, slow or network operation there. Create another 
    thread if you need to do such a thing
    """
    def datachange_notification(self, node, val, data):
        print("Server: New data change event, val: ", val)

    def event_notification(self, event):
        print("SErver: New event", event)


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARN)
    #logger = logging.getLogger("KeepAlive")
    #logger.setLevel(logging.DEBUG)

    client = Client(server_url)

    try:
        print('start to connect opcua server: opc.tcp://opcua.demo-this.com:51210/UA/SampleServer')
        client.connect()
        print('connect established\n')
        # client.load_type_definitions()  # load definition of server specific structures/extension objects

        # get root node as well as objects node
        print('----get root and objects node----')
        root = client.get_root_node()
        print("Root node is: ", root)
        objects = client.get_objects_node()
        print("Objects node is: ", objects)
        print('-------------------------------\n')

        # get a specific node and print its value
        static_node = client.get_node("ns=2;i=10218")
        var = static_node.get_data_value()  # get a static node as a DataValue object
        print('----get static node value showcase----')
        print('Timestamp: ' + str(var.SourceTimestamp))
        print('Value: ' + str(var.Value.Value))
        print('Type: ' + str(var.Value.VariantType))
        print('--------------------------------------\n')

        # set a value of a static node
        print('----set static node value showcase----')
        print('read current value: ' + str(var.Value.Value))
        print('increce value by 1')
        # static_node.set_value(249,node.get_data_type_as_variant_type()) # same effect as below, but automaticly detect the datatype
        static_node.set_value(ua.Variant(var.Value.Value + 1, ua.VariantType.Byte))
        # static_node = client.get_node("ns=2;i=10218")
        var = static_node.get_data_value()
        print('read current value after increcement: '+ str(var.Value.Value))
        print('--------------------------------------\n')

        # subscribing to a variable node for 5s
        print('----subscribe dynamic node value showcase (5s)----')
        dynamic_node = client.get_node("ns=2;i=11014")
        handler = SubHandler()
        sub = client.create_subscription(1000, handler)
        handle = sub.subscribe_data_change(dynamic_node)
        time.sleep(5)
        sub.unsubscribe(handle)
        print('--------------------------------------\n')

        # subscribe to events from server
        # sub.subscribe_events()
        # sub.unsubscribe(handle)
        # sub.delete()

        # calling a method on server
        # res = obj.call_method("{}:multiply".format(idx), 3, "klk")
        # print("method result is: ", res)

        # embed()
    finally:
        client.disconnect()
        print('server disconnected')