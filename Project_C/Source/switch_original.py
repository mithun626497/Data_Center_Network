from ryu.base import app_manager
from ryu.controller import ofp_event, dpset
from ryu.controller.handler import MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls

class Controller(app_manager.RyuApp):
    def __init__(self, *args, **kwargs):
        super(Controller, self).__init__(*args, **kwargs)


    @set_ev_cls(dpset.EventDP, MAIN_DISPATCHER)
    def switch_in(self, ev):
        dp  = ev.dp
        entered = ev.enter
        if ev.enter:
            self.install_rules(dp)


    def install_rules(self, dp):
        ofp        = dp.ofproto
        ofp_parser = dp.ofproto_parser

        # Make sure the switch's forwarding table is empty
        dp.send_delete_all_flows()

        # Creates a rule that sends out packets coming
        # from port: inport to the port: outport
        def from_port_to_port(inport, outport):
            match   = ofp_parser.OFPMatch(in_port=inport)
            actions = [ofp_parser.OFPActionOutput(outport)]
            out     = ofp_parser.OFPFlowMod(
                    datapath=dp, cookie=0,
                    command=ofp.OFPFC_ADD,
                    match=match,
                    actions=actions)
            dp.send_msg(out)

        # Rules for different switches
        if dp.id == 1:
           from_port_to_port(1, 2)
           from_port_to_port(3, 1)

        if dp.id == 2:
           from_port_to_port(2, 1)
           from_port_to_port(1, 3)

        if dp.id == 3:
           from_port_to_port(1, 2)



