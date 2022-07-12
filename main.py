import asyncio
import bbb_2_azure_bridge as b2a
import opc_2_bbb_bridge as o2b

import time
import azure_table_client as table_client
import bb_control_sim as sim


# We use the connect string now direcktly on scripy, but it's not secure, we will change it wenn we finished everything.
# conn_str = os.getenv("IOTHUB_DEVICE_CONNECTION_STRING")
# azure_conn_str = "HostName=CloudMES.azure-devices.net;DeviceId=BeagleBoneBlack;SharedAccessKey=QaV8v3YkB8girsnc1dgzE21BPRhG0SP5rnRgloXl6p4="
azure_conn_str = "HostName=CloudMES.azure-devices.net;DeviceId=EdgePython_1;SharedAccessKey=PCeKLE6l5WPoRv3I7NAnmfIWtUmzAS5gNQ23l5jGQik="
# opc_server_url = "opc.tcp://10.136.4.101:4840"
opc_server_url = "opc.tcp://localhost:4048"

connection_string = "DefaultEndpointsProtocol=https;AccountName=cldmstblstrg1;AccountKey=5Ez6g49uym1gUA/YIZnJWtS/DGwO0IwcpFnvp/R/hHHtVkXq5hgozsk0M72wkbbYNIHty7QvZbwZ/aW9VBehHA==;EndpointSuffix=core.windows.net"
table_name = "OutputTable1"
query_filter = "PartitionKey eq '1'"  # select PartitionKey


async def main():
    # Connect to Azure IoT Hub and OPC UA Server
    [azure_client, opc_client] = await asyncio.gather(
        b2a.azure_connect(azure_conn_str), o2b.opc_connect(opc_server_url)
    )

    # loop: get node value every 10s, send it to Azure IoT Hub

    while True:
        try:
            # get all node value, output a dict
            properties = {}
            properties = await o2b.opc_get_all_node_value(opc_client)

            # send to Azure IoT Hub
            await b2a.azure_send_msg(azure_client, properties)

        except Exception as e:
            print(e)
            return

        finally:
            await asyncio.sleep(10)


async def main_back():
    try:
        # loop = asyncio.get_event_loop()
        client = await o2b.opc_connect(opc_server_url)
        while True:
            dic = await table_client.line_processing(
                query_filter, connection_string, table_name
            )
            await sim.opc_set_node_value(client, dic)
            await asyncio.sleep(5)  # every 5s, check the changes
    except Exception as e:
        print(e)
        return


async def run():
    # define task
    task = asyncio.create_task(main())
    task_back = asyncio.create_task(main_back())
    # wait for task to finish
    await task
    await task_back


if __name__ == "__main__":
    # start event loop
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
    # asyncio.run(main())
    # asyncio.run(main_back())
