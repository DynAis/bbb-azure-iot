import azure_table_client as table_client
import bb_control_sim as sim

connection_string = "DefaultEndpointsProtocol=https;AccountName=cldmstblstrg1;AccountKey=5Ez6g49uym1gUA/YIZnJWtS/DGwO0IwcpFnvp/R/hHHtVkXq5hgozsk0M72wkbbYNIHty7QvZbwZ/aW9VBehHA==;EndpointSuffix=core.windows.net"

table_name = "OutputTable1"
query_filter = "PartitionKey eq '1'"#主键


async def main():

    # loop: get node value every 5s, check if it's changed, if so, send it to Server-Simunlation
    while True:
        try:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(get_last_line())
            # get all node value, output a dict
            table_client.line_processing()

            # send to Azure IoT Hub
            await b2a.azure_send_msg(azure_client, properties)

        except Exception as e:
            print(e)
            return

        finally:
            await asyncio.sleep(10)

if __name__ == "__main__":
    asyncio.run(main())  
