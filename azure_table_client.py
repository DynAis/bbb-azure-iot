from azure.data.tables.aio import TableClient
from azure.core.exceptions import HttpResponseError
import asyncio


item_list = ['bertieb_Hand', 'bertieb_Auto',  'start', 'stop', 'Quit','inductive_counter', 
            'total_inductive_counter','capactive_counter','total_capactive_counter',
            'zu_hoch','total_zu_hoch' ,'optisch_counter','total_optisch_counter',
            'Hoehe_messung','Alarm']



async def query_entities(query_filter,connection_string, table_name):
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
            try:
                async for entity in queried_entities:
                    if (await queried_entities.__anext__()):    #the latest table if->while the first table
                        pass
            except:
                return dict(entity)
            # print("Key: {}, Value: {}".format(key, entity[key]))
            # print(queried_entities)
        except Exception as e:
            print(e)

            

async def line_processing(query_filter,connection_string, table_name)->dict:
    dic = await query_entities(query_filter,connection_string, table_name)
    client_dict = {}
    for names in dic:
        if names in item_list:
            if isinstance(dic[names],bool) :
                client_dict[names] = dic[names]
            else:
                client_dict[names] = dic[names].value   
    print("list from Storage Table:"+ str(client_dict))    # print the dict 
    return client_dict

# async def get_last_line():
#     try:
#         client_dict =  await line_processing(query_filter,connection_string, table_name)
#     except Exception as e:
#         print(e)
#     finally:
#         await asyncio.sleep(5)

# if __name__ =="__main__":
#     while True:
#         loop = asyncio.get_event_loop()
#         loop.run_until_complete(get_last_line())
        