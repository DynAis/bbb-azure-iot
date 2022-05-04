import asyncio
import bbb_2_azure_bridge as b2a
import opc_2_bbb_bridge as o2b

# We use the connect string now direcktly on scripy, but it's not secure, we will change it wenn we finished everything.
# conn_str = os.getenv("IOTHUB_DEVICE_CONNECTION_STRING")
azure_conn_str = "HostName=CloudMES.azure-devices.net;DeviceId=BeagleBoneBlack;SharedAccessKey=QaV8v3YkB8girsnc1dgzE21BPRhG0SP5rnRgloXl6p4="
opc_server_url = "opc.tcp://192.168.123.238:12345"

async def main():
    # Connect to Azure IoT Hub and OPC UA Server
    [azure_client, opc_client] = await asyncio.gather(
        b2a.azure_connect(azure_conn_str),
        o2b.opc_connect(opc_server_url)
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

if __name__ == "__main__":
    asyncio.run(main())  
