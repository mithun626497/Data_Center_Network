from ryu.base import app_manager
import array
from ryu.controller import ofp_event, dpset
from ryu.controller.handler import MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.lib.packet import packet
s1=[1,2]
s2=[3,4]
s3=[5,6]
s4=[7,8]
s5=[9,10]
s6=[11,12]
s7=[13,14]
s8=[15,16]

#middle switches
vlan_id_store=0

#vlan_id_store=0
class Controller(app_manager.RyuApp):
    #vlan_id_store=0
    #bottom switches
#    s1=[1,2]
 ##   s2=[3,4]
   # s3=[5,6]
#    s4=[7,8]
#    s5=[9,10]
#    s6=[11,12]
##    s7=[13,14]
#    s8=[15,16]
    
    #middle switches
#    vlan_id_store=0
    def __init__(self, *args, **kwargs):
	super(Controller, self).__init__(*args, **kwargs)
    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)

    def switch_in(self, ev):
        msg=ev.msg
        dp  = msg.datapath
        pkt=packet.Packet(array.array('B',ev.msg.data))
        vlan_id_store=0
        for p in pkt:
                if p.protocol_name=='vlan':
 #                               print p.vid
				#global vlan_id_store
                                vlan_id_store=p.vid
				print vlan_id_store
	#destination = str(vlan_id_store -int(vlan_id_store))[2:]
	#source = str(vlan_id_store -int(vlan_id_store))[-2:]
	self.install_rules(dp)

    def install_rules(self, dp):
        ofp        = dp.ofproto
        ofp_parser = dp.ofproto_parser
        dp.send_delete_all_flows()

        # Creates a rule that sends out packets coming
        # from port: inport to the port: outport
        def from_port_to_port(inport, outport,vlan_id):
            match   = ofp_parser.OFPMatch(in_port=inport,dl_vlan=vlan_id)
            actions = [ofp_parser.OFPActionOutput(outport)]
            out     = ofp_parser.OFPFlowMod(
                    datapath=dp, cookie=0,
                    command=ofp.OFPFC_ADD,
                    match=match,
                    actions=actions)
            dp.send_msg(out)
 	print "mithun",vlan_id_store	
        #global vlan_id_store
	destination = str(vlan_id_store -int(vlan_id_store))[-2:]
	#global vlan_id_store
        source = str(vlan_id_store -int(vlan_id_store))[0:2]
	#global vlan_id_store
	#print vlan_id_store
	print destination
	print source
	
	if dp.id == 1:
           #check if the destination is 2
           if destination==2:
                from_port_to_port(1,2,vlan_id_store)
                from_port_to_port(3,2,vlan_id_store)
                from_port_to_port(4,2,vlan_id_store)
           if destination==1:
                from_port_to_port(2,1,vlan_id_store)
                from_port_to_port(3,1,vlan_id_store)
                from_port_to_port(4,1,vlan_id_store)
           else:
                from_port_to_port(1,3,vlan_id_store)
                from_port_to_port(2,3,vlan_id_store)
                from_port_to_port(4,3,vlan_id_store)

	if dp.id == 2:
           #check if the destination is 2
           if destination==4:
                from_port_to_port(1,2,vlan_id_store)
                from_port_to_port(3,2,vlan_id_store)
                from_port_to_port(4,2,vlan_id_store)
           if destination==3:
                from_port_to_port(2,1,vlan_id_store)
                from_port_to_port(3,1,vlan_id_store)
                from_port_to_port(4,1,vlan_id_store)
           else:
                from_port_to_port(1,3,vlan_id_store)
                from_port_to_port(2,3,vlan_id_store)
                from_port_to_port(4,3,vlan_id_store)
	
	if dp.id == 5:
           #check if the destination is 2
           if destination==6:
                from_port_to_port(1,2,vlan_id_store)
                from_port_to_port(3,2,vlan_id_store)
                from_port_to_port(4,2,vlan_id_store)
           if destination==5:
                from_port_to_port(2,1,vlan_id_store)
                from_port_to_port(3,1,vlan_id_store)
                from_port_to_port(4,1,vlan_id_store)
           else:
                from_port_to_port(1,3,vlan_id_store)
                from_port_to_port(2,3,vlan_id_store)
                from_port_to_port(4,3,vlan_id_store)

	if dp.id == 6:
           #check if the destination is 2
           if destination==8:
                from_port_to_port(1,2,vlan_id_store)
                from_port_to_port(3,2,vlan_id_store)
                from_port_to_port(4,2,vlan_id_store)
           if destination==7:
                from_port_to_port(2,1,vlan_id_store)
                from_port_to_port(3,1,vlan_id_store)
                from_port_to_port(4,1,vlan_id_store)
           else:
                from_port_to_port(1,3,vlan_id_store)
                from_port_to_port(2,3,vlan_id_store)
                from_port_to_port(4,3,vlan_id_store)

	if dp.id == 9:
           #check if the destination is 2
           if destination==10:
                from_port_to_port(1,2,vlan_id_store)
                from_port_to_port(3,2,vlan_id_store)
                from_port_to_port(4,2,vlan_id_store)
           if destination==9:
                from_port_to_port(2,1,vlan_id_store)
                from_port_to_port(3,1,vlan_id_store)
                from_port_to_port(4,1,vlan_id_store)
           else:
                from_port_to_port(1,3,vlan_id_store)
                from_port_to_port(2,3,vlan_id_store)
                from_port_to_port(4,3,vlan_id_store)
	
	if dp.id == 10:
           #check if the destination is 2
           if destination==12:
                from_port_to_port(1,2,vlan_id_store)
                from_port_to_port(3,2,vlan_id_store)
                from_port_to_port(4,2,vlan_id_store)
           if destination==11:
                from_port_to_port(2,1,vlan_id_store)
                from_port_to_port(3,1,vlan_id_store)
                from_port_to_port(4,1,vlan_id_store)
           else:
                from_port_to_port(1,3,vlan_id_store)
                from_port_to_port(2,3,vlan_id_store)
                from_port_to_port(4,3,vlan_id_store)

	if dp.id == 13:
           #check if the destination is 2
           if destination==14:
                from_port_to_port(1,2,vlan_id_store)
                from_port_to_port(3,2,vlan_id_store)
                from_port_to_port(4,2,vlan_id_store)
           if destination==13:
                from_port_to_port(2,1,vlan_id_store)
                from_port_to_port(3,1,vlan_id_store)
                from_port_to_port(4,1,vlan_id_store)
           else:
                from_port_to_port(1,3,vlan_id_store)
                from_port_to_port(2,3,vlan_id_store)
                from_port_to_port(4,3,vlan_id_store)
	
	if dp.id == 14:
           #check if the destination is 2
           if destination==16:
                from_port_to_port(1,2,vlan_id_store)
                from_port_to_port(3,2,vlan_id_store)
                from_port_to_port(4,2,vlan_id_store)
           if destination==15:
                from_port_to_port(2,1,vlan_id_store)
                from_port_to_port(3,1,vlan_id_store)
                from_port_to_port(4,1,vlan_id_store)
           else:
                from_port_to_port(1,3,vlan_id_store)
                from_port_to_port(2,3,vlan_id_store)
                from_port_to_port(4,3,vlan_id_store)
	
	# routing for PODS	
	if dp.id == 3:
	   global s1
	   if destination in s1:
		from_port_to_port(2,1,vlan_id_store)
		from_port_to_port(3,1,vlan_id_store)
		from_port_to_port(4,1,vlan_id_store)
	   global s2
	   if destination in s2:
                from_port_to_port(1,2,vlan_id_store)
                from_port_to_port(3,2,vlan_id_store)
                from_port_to_port(4,2,vlan_id_store)	   
	   else:
                from_port_to_port(1,3,vlan_id_store)
                from_port_to_port(2,3,vlan_id_store)

	if dp.id == 4:
	   #global s1
           if destination in s1:
                from_port_to_port(2,1,vlan_id_store)
                from_port_to_port(3,1,vlan_id_store)
                from_port_to_port(4,1,vlan_id_store)
	   #global s2
           if destination in s2:
                from_port_to_port(1,2,vlan_id_store)
                from_port_to_port(3,2,vlan_id_store)
                from_port_to_port(4,2,vlan_id_store)
           else:
                from_port_to_port(1,3,vlan_id_store)
                from_port_to_port(2,3,vlan_id_store)
		from_port_to_port(1,4,vlan_id_store)
		from_port_to_port(2,4,vlan_id_store)
		
	if dp.id == 7:
	   #global s3
           if destination in s3:
                from_port_to_port(2,1,vlan_id_store)
                from_port_to_port(3,1,vlan_id_store)
                from_port_to_port(4,1,vlan_id_store)
	  # global s4
           if destination in s4:
                from_port_to_port(1,2,vlan_id_store)
                from_port_to_port(3,2,vlan_id_store)
                from_port_to_port(4,2,vlan_id_store)
           else:
                from_port_to_port(1,3,vlan_id_store)
                from_port_to_port(2,3,vlan_id_store)
		from_port_to_port(1,4,vlan_id_store)
                from_port_to_port(2,4,vlan_id_store)

	if dp.id == 8:
	   #global s3
           if destination in s3:
                from_port_to_port(2,1,vlan_id_store)
                from_port_to_port(3,1,vlan_id_store)
                from_port_to_port(4,1,vlan_id_store)
	   #global s4
           if destination in s4:
                from_port_to_port(1,2,vlan_id_store)
                from_port_to_port(3,2,vlan_id_store)
                from_port_to_port(4,2,vlan_id_store)
           else:
                from_port_to_port(1,3,vlan_id_store)
                from_port_to_port(2,3,vlan_id_store)
                from_port_to_port(1,4,vlan_id_store)
                from_port_to_port(2,4,vlan_id_store)

	if dp.id == 11:
	  # global s5
           if destination in s5:
                from_port_to_port(2,1,vlan_id_store)
                from_port_to_port(3,1,vlan_id_store)
                from_port_to_port(4,1,vlan_id_store)
	  # global s6
           if destination in s6:
                from_port_to_port(1,2,vlan_id_store)
                from_port_to_port(3,2,vlan_id_store)
                from_port_to_port(4,2,vlan_id_store)
           else:
                from_port_to_port(1,3,vlan_id_store)
                from_port_to_port(2,3,vlan_id_store)
                from_port_to_port(1,4,vlan_id_store)
                from_port_to_port(2,4,vlan_id_store)

	if dp.id == 12:
	  # global s5
           if destination in s5:
                from_port_to_port(2,1,vlan_id_store)
                from_port_to_port(3,1,vlan_id_store)
                from_port_to_port(4,1,vlan_id_store)
	  # global s6
           if destination in s6:
                from_port_to_port(1,2,vlan_id_store)
                from_port_to_port(3,2,vlan_id_store)
                from_port_to_port(4,2,vlan_id_store)
           else:
                from_port_to_port(1,3,vlan_id_store)
                from_port_to_port(2,3,vlan_id_store)
                from_port_to_port(1,4,vlan_id_store)
                from_port_to_port(2,4,vlan_id_store)

	if dp.id == 15:
	  # global s7
           if destination in s7:
                from_port_to_port(2,1,vlan_id_store)
                from_port_to_port(3,1,vlan_id_store)
                from_port_to_port(4,1,vlan_id_store)
	  # global s8
           if destination in s8:
                from_port_to_port(1,2,vlan_id_store)
                from_port_to_port(3,2,vlan_id_store)
                from_port_to_port(4,2,vlan_id_store)
           else:
                from_port_to_port(1,3,vlan_id_store)
                from_port_to_port(2,3,vlan_id_store)
                from_port_to_port(1,4,vlan_id_store)
                from_port_to_port(2,4,vlan_id_store)

	if dp.id == 16:
	  # global s7
           if destination in s7:
                from_port_to_port(2,1,vlan_id_store)
                from_port_to_port(3,1,vlan_id_store)
                from_port_to_port(4,1,vlan_id_store)
	  # global s8
           if destination in s8:
                from_port_to_port(1,2,vlan_id_store)
                from_port_to_port(3,2,vlan_id_store)
                from_port_to_port(4,2,vlan_id_store)
           else:
                from_port_to_port(1,3,vlan_id_store)
                from_port_to_port(2,3,vlan_id_store)
                from_port_to_port(1,4,vlan_id_store)
                from_port_to_port(2,4,vlan_id_store)


	#routing for Core switches
	if dp.id == 17:
           if source == 1 :
                from_port_to_port(1,2,vlan_id_store)
                from_port_to_port(1,3,vlan_id_store)
                from_port_to_port(1,4,vlan_id_store)
	   if source == 2 :
                from_port_to_port(2,1,vlan_id_store)
                from_port_to_port(2,3,vlan_id_store)
                from_port_to_port(2,4,vlan_id_store)
	   if source == 3 :
                from_port_to_port(3,1,vlan_id_store)
                from_port_to_port(3,2,vlan_id_store)
                from_port_to_port(3,4,vlan_id_store)
	   if source == 4 :
                from_port_to_port(4,1,vlan_id_store)
                from_port_to_port(4,2,vlan_id_store)
                from_port_to_port(4,3,vlan_id_store)
	
	if dp.id == 18:
           if source == 1 :
                from_port_to_port(1,2,vlan_id_store)
                from_port_to_port(1,3,vlan_id_store)
                from_port_to_port(1,4,vlan_id_store)
           if source == 2 :
                from_port_to_port(2,1,vlan_id_store)
                from_port_to_port(2,3,vlan_id_store)
                from_port_to_port(2,4,vlan_id_store)
           if source == 3 :
                from_port_to_port(3,1,vlan_id_store)
                from_port_to_port(3,2,vlan_id_store)
                from_port_to_port(3,4,vlan_id_store)
           if source == 4 :
                from_port_to_port(4,1,vlan_id_store)
                from_port_to_port(4,2,vlan_id_store)
                from_port_to_port(4,3,vlan_id_store)

	if dp.id == 19:
           if source == 1 :
                from_port_to_port(1,2,vlan_id_store)
                from_port_to_port(1,3,vlan_id_store)
                from_port_to_port(1,4,vlan_id_store)
           if source == 2 :
                from_port_to_port(2,1,vlan_id_store)
                from_port_to_port(2,3,vlan_id_store)
                from_port_to_port(2,4,vlan_id_store)
           if source == 3 :
                from_port_to_port(3,1,vlan_id_store)
                from_port_to_port(3,2,vlan_id_store)
                from_port_to_port(3,4,vlan_id_store)
           if source == 4 :
                from_port_to_port(4,1,vlan_id_store)
                from_port_to_port(4,2,vlan_id_store)
                from_port_to_port(4,3,vlan_id_store)

	if dp.id == 20:
           if source == 1 :
                from_port_to_port(1,2,vlan_id_store)
                from_port_to_port(1,3,vlan_id_store)
                from_port_to_port(1,4,vlan_id_store)
           if source == 2 :
                from_port_to_port(2,1,vlan_id_store)
                from_port_to_port(2,3,vlan_id_store)
                from_port_to_port(2,4,vlan_id_store)
           if source == 3 :
                from_port_to_port(3,1,vlan_id_store)
                from_port_to_port(3,2,vlan_id_store)
                from_port_to_port(3,4,vlan_id_store)
           if source == 4 :
                from_port_to_port(4,1,vlan_id_store)
                from_port_to_port(4,2,vlan_id_store)
                from_port_to_port(4,3,vlan_id_store)

