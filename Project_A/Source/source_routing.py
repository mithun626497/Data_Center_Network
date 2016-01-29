from ryu.base import app_manager
from ryu.controller import ofp_event, dpset
from ryu.controller.handler import MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls

allVlans=[18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,120,121,122,123,124,125,126,127,128,129,130,131,132,133,134,135,137,138,139,140,141,142,143,144,145,146,147,148,149,150,151,152,154,155,156,157,158,159,160,161,162,163,164,165,166,167,168,169,171,172,173,174,175,176,177,178,179,180,181,182,183,184,185,186,188,189,190,191,192,193,194,195,196,197,198,199,200,201,202,203,205,206,207,208,209,210,211,212,213,214,215,216,217,218,219,220,222,223,224,225,226,227,228,229,230,231,232,233,234,235,236,237,239,240,241,242,243,244,245,246,247,248,249,250,251,252,253,254,256,257,258,259,260,261,262,263,264,265,266,267,268,269,270,271]
#allVlans =[21]
pod1Vlans=[18,19,20,33,35,36,49,50,52,65,66,67]
pod2Vlans=[86,87,88,101,103,104,117,118,120,133,134,135]
pod3Vlans=[154,155,156,169,171,172,185,186,188,201,202,203]
pod4Vlans=[222,223,224,237,239,240,253,254,256,269,270,271]
#podx means pod number is x and it has hosts say 1,2,3,4
pod1 = [1,2,3,4]
pod2 = [5,6,7,8]
pod3 = [9,10,11,12]
pod4 = [13,14,15,16]
#spq = [x,y] means switches p and q have the hosts x and y 
s14 =[1,2]
s13 =[3,4]
s58 =[5,6]
s57 =[7,8]
s912=[9,10]
s911=[11,12]
s1316=[13,14]
s1315=[15,16]
s24=[1,2]
s23=[3,4]
s68=[5,6]
s67=[7,8]
s1012=[9,10]
s1011=[11,12]
s1416=[13,14]
s1415=[15,16]

h16routing=[32,48,64,80,96,112,128,144,160,176,192,208,224,240,256]

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
	
	def from_port_to_port(inport, outport,vlanid):
            match   = ofp_parser.OFPMatch(in_port=inport,dl_vlan=vlanid)
            actions = [ofp_parser.OFPActionOutput(outport)]
            out     = ofp_parser.OFPFlowMod(
                    datapath=dp, cookie=0,
                    command=ofp.OFPFC_ADD,
                    match=match,
                    actions=actions)
            dp.send_msg(out)

        # Rules for different switches
        if dp.id == 4:
           from_port_to_port(4, 3,18) #h1 to h2
           from_port_to_port(3, 4,33) #h2 to h1
	   
	   from_port_to_port(4, 2,19) #h1 to h3
	   from_port_to_port(3, 2,35) #h2 to h3
	   from_port_to_port(4, 2,20) #h1 to h4
	   from_port_to_port(3, 2,36) #h2 to h4
	
	   from_port_to_port(1, 4,49) #to h1
           from_port_to_port(1, 3,50) #to h2
           from_port_to_port(1, 4,65) #to h1
           from_port_to_port(1, 3,66) #to h2
	
	   # for all other hosts send it to the core switch via switch 1
	   for n in allVlans:
		if n not in pod1Vlans and n not in pod2Vlans and n not in pod3Vlans and n not in pod4Vlans:
			from_port_to_port(4,1,n)
			from_port_to_port(3,1,n)

	   for n in allVlans:
		if n not in pod1Vlans and n not in pod2Vlans and n not in pod3Vlans and n not in pod4Vlans:
			temp=n&15
			if temp==1:
                        	from_port_to_port(1,4,n)
                	        from_port_to_port(2,4,n)
			elif temp==2:
                      		from_port_to_port(1,3,n)
                        	from_port_to_port(2,3,n)

	if dp.id == 2:
	   from_port_to_port(4,3,19)
	   from_port_to_port(4,3,35)
	   from_port_to_port(4,3,20)
	   from_port_to_port(4,3,36)

	   for n in allVlans:
		if n not in pod1Vlans and n not in pod2Vlans and n not in pod3Vlans and n not in pod4Vlans:
			temp=n&15
			if temp in s24:
	                        from_port_to_port(1,4,n)
        	                from_port_to_port(2,4,n)
			elif temp in s23:
				from_port_to_port(1,3,n)
				from_port_to_port(2,3,n)

        if dp.id == 3:
	   from_port_to_port(4, 3,52) #h3 to h4
           from_port_to_port(3, 4,67) #h4 to h3
           from_port_to_port(2, 4,19) #to h3
           from_port_to_port(2, 3,20) #to h4
	   from_port_to_port(2, 4,35) #to h3
	   from_port_to_port(2, 3,36) #to h4
	   
	   from_port_to_port(4, 1,49) #h3 to h1
           from_port_to_port(4, 1,50) #h3 to h2
           from_port_to_port(3, 1,65) #h4 to h1
           from_port_to_port(3, 1,66) #h4 to h2
	 
	   #routing to core switches
           for n in allVlans:
		if n not in pod1Vlans and n not in pod2Vlans and n not in pod3Vlans and n not in pod4Vlans:
			from_port_to_port(4,1,n)
			from_port_to_port(3,1,n)

	   for n in allVlans:
		if n not in pod1Vlans and n not in pod2Vlans and n not in pod3Vlans and n not in pod4Vlans:
			temp=n&15
			if temp==3:
	                        from_port_to_port(1,4,n)
        	                from_port_to_port(2,4,n)
			elif temp==4:
                        	from_port_to_port(1,3,n)
                        	from_port_to_port(2,3,n)
	
	if dp.id == 1:
	   from_port_to_port(3, 4,49)
           from_port_to_port(3, 4,50)
           from_port_to_port(3, 4,65)
           from_port_to_port(3, 4,66)
	   
	   #routing to core switches
	   for n in allVlans:
		if n not in pod1Vlans and n not in pod2Vlans and n not in pod3Vlans and n not in pod4Vlans:
                        from_port_to_port(4,1,n)
                        from_port_to_port(3,1,n)

	   for n in allVlans:
		if n not in pod1Vlans and n not in pod2Vlans and n not in pod3Vlans and n not in pod4Vlans:
			temp=n&15
			if temp in s14:
	                        from_port_to_port(2,4,n)
			elif temp in s13:
	                        from_port_to_port(2,3,n)
	   
	#pod 2 internal routing
	if dp.id == 8:
           from_port_to_port(4, 3,86) #h5 to h6
           from_port_to_port(3, 4,101) #h6 to h5
           from_port_to_port(4, 2,87) #h5 to h7
           from_port_to_port(3, 2,103) #h6 to h7
           from_port_to_port(4, 2,88) #h5 to h8
           from_port_to_port(3, 2,104) #h6 to h8

           from_port_to_port(1, 4,117) #to h5
           from_port_to_port(1, 3,118) #to h6
           from_port_to_port(1, 4,133) #to h5
           from_port_to_port(1, 3,134) #to h6
	
	   #routing to core switches
           for n in allVlans:
		if n not in pod1Vlans and n not in pod2Vlans and n not in pod3Vlans and n not in pod4Vlans:
                        from_port_to_port(4,1,n)
	  		from_port_to_port(3,1,n)
 
	   for n in allVlans:
		if n not in pod1Vlans and n not in pod2Vlans and n not in pod3Vlans and n not in pod4Vlans:
			temp=n&15
			if temp==5:
                        	from_port_to_port(1,4,n)
                         	from_port_to_port(2,4,n)
			elif temp==6:
                        	from_port_to_port(1,3,n)
		               	from_port_to_port(2,3,n)

        if dp.id == 6:
           from_port_to_port(4,3,87)
           from_port_to_port(4,3,103)
           from_port_to_port(4,3,88)
           from_port_to_port(4,3,104)
	   
	   for n in allVlans:
		if n not in pod1Vlans and n not in pod2Vlans and n not in pod3Vlans and n not in pod4Vlans:
			temp=n&15
                        if temp in s68:
                                from_port_to_port(1,4,n)
				from_port_to_port(2,4,n)
                        elif temp in s67:
                                from_port_to_port(1,3,n)
				from_port_to_port(2,3,n)

        if dp.id == 7:
           from_port_to_port(4, 3,120) #h7 to h8
           from_port_to_port(3, 4,135) #h8 to h7
           from_port_to_port(2, 4,87) #to h7
           from_port_to_port(2, 3,88) #to h8
           from_port_to_port(2, 4,103) #to h7
           from_port_to_port(2, 3,104) #to h8

           from_port_to_port(4, 1,117) #h7 to h5
           from_port_to_port(4, 1,118) #h7 to h6
           from_port_to_port(3, 1,133) #h8 to h5
           from_port_to_port(3, 1,134) #h8 to h6

	   #routing to core switches
           for n in allVlans:
		if n not in pod1Vlans and n not in pod2Vlans and n not in pod3Vlans and n not in pod4Vlans:
                        from_port_to_port(4,1,n)
			from_port_to_port(3,1,n)
	
	   for n in allVlans:
		if n not in pod1Vlans and n not in pod2Vlans and n not in pod3Vlans and n not in pod4Vlans:
			temp=n&15
			if temp==7:
                        	from_port_to_port(1,4,n)
                        	from_port_to_port(2,4,n)
			elif temp==8:
                        	from_port_to_port(1,3,n)
                        	from_port_to_port(2,3,n)

        if dp.id == 5:
           from_port_to_port(3, 4,117)
	   from_port_to_port(3, 4,118)
           from_port_to_port(3, 4,133)
           from_port_to_port(3, 4,134)

	   #routing to core switches
           for n in allVlans:
		if n not in pod1Vlans and n not in pod2Vlans and n not in pod3Vlans and n not in pod4Vlans:
                        from_port_to_port(4,2,n)
                        from_port_to_port(3,2,n)	

	   for n in allVlans:
		if n not in pod1Vlans and n not in pod2Vlans and n not in pod3Vlans and n not in pod4Vlans:
			temp=n&15
                        if temp in s58:
                                from_port_to_port(1,4,n)
                        elif temp in s57:
                                from_port_to_port(1,3,n)
	
	#pod 3 internal routing
        if dp.id == 12:
           from_port_to_port(4, 3,154) #h9 to h10
           from_port_to_port(3, 4,169) #h10 to h9
           
	   from_port_to_port(4, 2,155) #h9 to h11
           from_port_to_port(3, 2,171) #h10 to h11
           from_port_to_port(4, 2,156) #h9 to h12
           from_port_to_port(3, 2,172) #h10 to h12

           from_port_to_port(1, 4,185) #to h9
           from_port_to_port(1, 3,186) #to h10
           from_port_to_port(1, 4,201) #to h9
           from_port_to_port(1, 3,202) #to h10
	  
	   #routing to core switches
           for n in allVlans:
		if n not in pod1Vlans and n not in pod2Vlans and n not in pod3Vlans and n not in pod4Vlans:
                        from_port_to_port(4,2,n)
			from_port_to_port(3,2,n)

	   for n in allVlans:
		if n not in pod1Vlans and n not in pod2Vlans and n not in pod3Vlans and n not in pod4Vlans:
			temp=n&15
			if temp==9:
	                        from_port_to_port(1,4,n)
        	                from_port_to_port(2,4,n)
			elif temp==10:
                        	from_port_to_port(1,3,n)
                        	from_port_to_port(2,3,n)

        if dp.id == 10:
           from_port_to_port(4,3,155)
           from_port_to_port(4,3,171)
           from_port_to_port(4,3,156)
           from_port_to_port(4,3,172)
	
	   #routing to core switches
           for n in allVlans:
		if n not in pod1Vlans and n not in pod2Vlans and n not in pod3Vlans and n not in pod4Vlans:
                        from_port_to_port(4,1,n)
                        from_port_to_port(3,1,n)

	   for n in allVlans:
		if n not in pod1Vlans and n not in pod2Vlans and n not in pod3Vlans and n not in pod4Vlans:
			temp=n&15
                        if temp in s1012:
                                from_port_to_port(2,4,n)
                        elif temp in s1011:
                                from_port_to_port(2,3,n)

        if dp.id == 11:
           from_port_to_port(4, 3,188) #h11 to h12
           from_port_to_port(3, 4,203) #h12 to h11
           from_port_to_port(2, 4,155) #to h11
           from_port_to_port(2, 3,156) #to h12
           from_port_to_port(2, 4,171) #to h11
           from_port_to_port(2, 3,172) #to h12

           from_port_to_port(4, 1,185) #h11 to h9
           from_port_to_port(4, 1,186) #h11 to h10
           from_port_to_port(3, 1,201) #h12 to h9
           from_port_to_port(3, 1,202) #h12 to h10

	   #routing to core switches
           for n in allVlans:
		if n not in pod1Vlans and n not in pod2Vlans and n not in pod3Vlans and n not in pod4Vlans:
			from_port_to_port(4,2,n)
                        from_port_to_port(3,2,n)


	   for n in allVlans:
		if n not in pod1Vlans and n not in pod2Vlans and n not in pod3Vlans and n not in pod4Vlans:
			temp=n&15
			if temp==11:
	                        from_port_to_port(1,4,n)
        	                from_port_to_port(2,4,n)
			elif temp==12:
	                        from_port_to_port(1,3,n)
        	                from_port_to_port(2,3,n)

        if dp.id == 9:
	   from_port_to_port(3, 4,185)
           from_port_to_port(3, 4,186)
           from_port_to_port(3, 4,201)
           from_port_to_port(3, 4,202)
	   
	   #routing to core switches
	   for n in allVlans:
		if n not in pod1Vlans and n not in pod2Vlans and n not in pod3Vlans and n not in pod4Vlans:
			temp=n&15
                        if temp in s912:
                                from_port_to_port(1,4,n)
				from_port_to_port(2,4,n)
                        elif temp in s911:
                                from_port_to_port(1,3,n)
				from_port_to_port(2,3,n)

	#pod 4 internal routing
        if dp.id == 16:
           from_port_to_port(4, 3,222) #h13 to h14
           from_port_to_port(3, 4,237) #h14 to h13
           from_port_to_port(4, 2,223) #h13 to h15
           from_port_to_port(3, 2,239) #h14 to h15
           from_port_to_port(4, 2,224) #h13 to h16
           from_port_to_port(3, 2,240) #h14 to h16

           from_port_to_port(1, 4,253) #to h13
           from_port_to_port(1, 3,254) #to h14
           from_port_to_port(1, 4,269) #to h13
           from_port_to_port(1, 3,270) #to h14

	   #routing to core switches
           for n in allVlans:
		if n not in pod1Vlans and n not in pod2Vlans and n not in pod3Vlans and n not in pod4Vlans:
			from_port_to_port(4,2,n)
                        from_port_to_port(3,2,n)

	   for n in allVlans:
		if n not in pod1Vlans and n not in pod2Vlans and n not in pod3Vlans and n not in pod4Vlans:
			temp=n&15
			if temp==13:
                       		from_port_to_port(1,4,n)
                        	from_port_to_port(2,4,n)
			elif temp==14:
	                        from_port_to_port(1,3,n)
        	                from_port_to_port(2,3,n)

        if dp.id == 14:
           from_port_to_port(4,3,223)
           from_port_to_port(4,3,239)
           from_port_to_port(4,3,224)
           from_port_to_port(4,3,240)

	   #routing to core switches
           for n in allVlans:
		if n not in pod1Vlans and n not in pod2Vlans and n not in pod3Vlans and n not in pod4Vlans:
                        from_port_to_port(4,2,n)
                        from_port_to_port(3,2,n)
	   
	   for n in allVlans:
		if n not in pod1Vlans and n not in pod2Vlans and n not in pod3Vlans and n not in pod4Vlans:
			if n in h16routing:
                                temp=16
                        else:
                                temp = n&15
                        if temp in s1416:
                                from_port_to_port(1,4,n)
                        elif temp in s1415:
                                from_port_to_port(1,3,n)

        if dp.id == 15:
           from_port_to_port(4, 3,256) #h15 to h16
           from_port_to_port(3, 4,271) #h16 to h15
           from_port_to_port(2, 4,223) #to h15
           from_port_to_port(2, 3,224) #to h16
           from_port_to_port(2, 4,239) #to h15
           from_port_to_port(2, 3,240) #to h16

           from_port_to_port(4, 1,253) #h15 to h13
           from_port_to_port(4, 1,254) #h15 to h14
           from_port_to_port(3, 1,269) #h16 to h13
           from_port_to_port(3, 1,270) #h16 to h14

	   #routing to core switches
           for n in allVlans:
		if n not in pod1Vlans and n not in pod2Vlans and n not in pod3Vlans and n not in pod4Vlans:
                        from_port_to_port(4,2,n)
                        from_port_to_port(3,2,n)

	   for n in allVlans:
		if n not in pod1Vlans and n not in pod2Vlans and n not in pod3Vlans and n not in pod4Vlans:
			if n in h16routing:
                                temp=16
                        else:
                                temp = n&15
			if temp==15:
	                        from_port_to_port(1,4,n)
        	                from_port_to_port(2,4,n)
			elif temp==16:
                       		from_port_to_port(1,3,n)
                        	from_port_to_port(2,3,n)

        if dp.id == 13:
           from_port_to_port(3, 4,253)
           from_port_to_port(3, 4,254)
           from_port_to_port(3, 4,269)
	   from_port_to_port(3, 4,270)

	   #routing to core switches
	   for n in allVlans:
		if n not in pod1Vlans and n not in pod2Vlans and n not in pod3Vlans and n not in pod4Vlans:
			if n in h16routing:
                                temp=16
                        else:
                                temp = n&15
                        if temp in s1316:
                                from_port_to_port(1,4,n)
				from_port_to_port(2,4,n)
                        elif temp in s1315:
                                from_port_to_port(1,3,n)
				from_port_to_port(2,3,n)

	#core switches routing
	if dp.id == 17:
           for n in allVlans:
		if n not in pod1Vlans and n not in pod2Vlans and n not in pod3Vlans and n not in pod4Vlans:
			#get the destination host
			if n in h16routing:
				temp=16
			else:
				temp = n&15

			if temp in pod2:	
				from_port_to_port(1,2,n)
			elif temp in pod3:
				from_port_to_port(1,3,n)
			elif temp in pod4:
				from_port_to_port(1,4,n)

	if dp.id == 18:
           for n in allVlans:
		if n not in pod1Vlans and n not in pod2Vlans and n not in pod3Vlans and n not in pod4Vlans:
			if n in h16routing:
                                temp=16
                        else:
                                temp = n&15
			if temp in pod1:
                                from_port_to_port(2,1,n)
                        elif temp in pod3:
                                from_port_to_port(2,3,n)
                        elif temp in pod4:
                                from_port_to_port(2,4,n)

	if dp.id == 19:
           for n in allVlans:
		if n not in pod1Vlans and n not in pod2Vlans and n not in pod3Vlans and n not in pod4Vlans:
			if n in h16routing:
                                temp=16
                        else:
                                temp = n&15
                        if temp in pod1:
                                from_port_to_port(3,1,n)
                        elif temp in pod2:
                                from_port_to_port(3,2,n)
                        elif temp in pod4:
                                from_port_to_port(3,4,n)

	if dp.id == 20:
           for n in allVlans:
		if n not in pod1Vlans and n not in pod2Vlans and n not in pod3Vlans and n not in pod4Vlans:
			if n in h16routing:
                                temp=16
                        else:
                                temp = n&15
                        if temp in pod1:
                                from_port_to_port(4,1,n)
                        elif temp in pod2:
                                from_port_to_port(4,2,n)
                        elif temp in pod3:
                                from_port_to_port(4,3,n)


