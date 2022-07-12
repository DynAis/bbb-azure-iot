from time import sleep
from opcua import Server



##Server config
server = Server()
# server.set_endpoint("opc.tcp://127.0.0.1:4048")
server.set_endpoint("opc.tcp://localhost:12345")
server.register_namespace("server")

##Register 3rd namespace as S71500
PLC = server.register_namespace("PLC")

##retiver server objects as one
Objects = server.get_objects_node()
global_object = Objects.add_object(PLC, "variables")

#variabels

bsHand = global_object.add_variable('ns=3;s="Sort"."hmi"."bsHand"', "bertieb_Hand", False)
bsHand.set_writable()

bsAuto = global_object.add_variable('ns=3;s="Sort"."hmi"."bsAuto"', "bertieb_Auto", True)
bsAuto.set_writable()

start = global_object.add_variable('ns=3;s="Sort"."hmi"."bsStart"', "start", False)
start.set_writable()

stop = global_object.add_variable('ns=3;s="Sort"."hmi"."bsStopp"', "stop", True)
stop.set_writable()

_quit = global_object.add_variable('ns=3;s="Sort"."hmi"."bsQuitt"', "Quit", False)
_quit.set_writable()

ind_counter = global_object.add_variable('ns=3;s="Sort"."zaehl"."zaehlerInd"', "inductive_counter",0)
ind_counter.set_writable()
glob_ind_counter = global_object.add_variable('ns=3;s="Sort"."zaehl"."total_zaehlerInd"', "total_inductive_counter",0)
glob_ind_counter.set_writable()

kap_counter = global_object.add_variable('ns=3;s="Sort"."zaehl"."zaehlerKa"', "capactive_counter", 0)
kap_counter.set_writable()
glob_kap_counter = global_object.add_variable('ns=3;s="Sort"."zaehl"."total_zaehlerKa"', "total_capactive_counter", 0)
glob_kap_counter.set_writable()

h_counter = global_object.add_variable('ns=3;s="Sort"."zaehl"."zaehlerHo"', "zu_hoch", 0)
h_counter.set_writable()
glob_h_counter = global_object.add_variable('ns=3;s="Sort"."zaehl"."total_zaehlerHo"', "total_zu_hoch", 0)
glob_h_counter.set_writable()

opt_counter = global_object.add_variable('ns=3;s="Sort"."zaehl"."zaehlerWs"', "optisch_counter" ,0)
opt_counter.set_writable()
global_opt_counter = global_object.add_variable('ns=3;s="Sort"."zaehl"."total_zaehlerWs"', "total_optisch_counter" ,0)
global_opt_counter.set_writable()

hight_mes = global_object.add_variable('ns=3;s="Sort"."Hoehe_messen"', "Hoehe_messung" ,0)
# opt_counter.set_writable()#
hight_mes.set_writable()

Alarm = global_object.add_variable('ns=3;s="Sort"."Stoerung"', "Alarm" ,False)
Alarm.set_writable()

server.start()
print(server.get_endpoints())
print("")
print(server.get_namespace_array())
print("")
print("------------Server Started--------------")

while True:
    print("########SAMPLE##########")
    for obj in global_object.get_children():
        print(str(obj.get_browse_name())[16:len(str(obj.get_browse_name()))-1])
        print(obj.get_value())
        print("   ")
    print("   ")
    sleep(10)
    