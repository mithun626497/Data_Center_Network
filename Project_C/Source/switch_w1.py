from ryu.base import app_manager
import array
from ryu.controller import ofp_event, dpset
from ryu.controller.handler import MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.lib.packet import packet
class Controller(app_manager.RyuApp):
    vlan_id_store =0
    #bottom switches
    s1=[1,2]
    s2=[3,4]
    s5=[5,6]
    s6=[7,8]
    s9=[9,10]
    s10=[11,12]
    s13=[13,14]
    s14=[15,16]
    #middle switches
    s3=[s1,s2]
    s4=[s1,s2]
    s7=[s5,s6]
    s8=[s5,s6]
    s11=[s9,s10]
    s12=[s9,s10]
    s15=[s13,s14]
    s16=[s13,s14]
    #core switches      
    s17=[s3,s7,s11,s15]
    s18=[s3,s7,s11,s15]
    s19=[s4,s8,s12,s16]
    s20=[s4,s8,s12,s16]
    vlan_id_store=0

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
                                print p.vid
                                vlan_id_store=p.vid
        #entered = ev.enter
        #if ev.enter:
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

	if dp.id == 1:
	   destination =0
	   vlan_id_store =500
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



