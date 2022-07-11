from azure.data.tables.aio import TableClient
from azure.core.exceptions import HttpResponseError
import asyncio

connection_string = "DefaultEndpointsProtocol=https;AccountName=cldmstblstrg1;AccountKey=5Ez6g49uym1gUA/YIZnJWtS/DGwO0IwcpFnvp/R/hHHtVkXq5hgozsk0M72wkbbYNIHty7QvZbwZ/aW9VBehHA==;EndpointSuffix=core.windows.net"
# service = TableServiceClient.from_connection_string(conn_str=connection_string)
table_name = "OutputTable1"
query_filter = "PartitionKey eq '1'"#主键

async def query_entities(query_filter):
    table_client = TableClient.from_connection_string(connection_string, table_name)
    # [START query_entities]
    async with table_client:
        try:
            queried_entities = table_client.query_entities(query_filter)
            # parameters = {u"name": u"marker"}
            # name_filter = u"Name eq @name"
            # queried_entities = table_client.query_entities(
            #   query_filter=name_filter, select=[u"Brand", u"Color"], parameters=parameters
            # )
            async for entity in queried_entities:
                
                while (await queried_entities.__anext__()):
                    pass
                
            # print("Key: {}, Value: {}".format(key, entity[key]))
            # print(queried_entities)
        except HttpResponseError as e:
            pass
        except :
            print(entity)
            return entity

async def main():
    try:
        await query_entities(query_filter)
    except Exception as e:
        print(e)
    finally:
        await asyncio.sleep(10)

if __name__ =="__main__":
    while True:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
        