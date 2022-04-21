import json

from azure.iot.device.aio import IoTHubDeviceClient
from azure.iot.device import Message

model_id = "beaglebone-black"

# Connect to Azure IoT hub, return a device_client
async def azure_connect(conn_str: str) -> IoTHubDeviceClient:
    print("Connecting using Connection String " + conn_str)
    device_client = IoTHubDeviceClient.create_from_connection_string(
        conn_str, product_info=model_id
    )
    # Connect the client. if not successful, throw an exception.
    try:
        await device_client.connect()
    except Exception as e:
        print("Error connecting to Azure IoT Hub: " + str(e))
        return
    return device_client



# Addapt a message dict, change to JSON and send to Azure IoT hub, print message
async def azure_send_msg(device_client: IoTHubDeviceClient, msg_dict: dict, component_name=None):
    # if device_client is void, throw an exception
    assert device_client is not None, "device_client is None"
    # if msg_dict is not a dict or include nothing, throw an exception
    assert isinstance(msg_dict, dict) and msg_dict, "msg_dict is not a dict or is empty"

    # make massage
    msg = Message(json.dumps(msg_dict))
    msg.content_encoding = "utf-8"
    msg.content_type = "application/json"
    if component_name:
        msg.custom_properties["$.sub"] = component_name
    # send massage
    await device_client.send_message(msg)

    # print massage
    print(msg_dict)



# close the connection
async def azure_disconnect(device_client: IoTHubDeviceClient):
    # if device_client is void, throw an exception
    assert device_client is not None, "device_client is None"
    await device_client.disconnect()