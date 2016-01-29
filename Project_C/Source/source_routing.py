from ryu.base import app_manager
from ryu.controller import ofp_event, dpset
from ryu.controller.handler import MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls

#allVlans=[18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,120,121,122,123,124,125,126,127,128,129,130,131,132,133,134,135,137,138,139,140,141,142,143,144,145,146,147,148,149,150,151,152,154,155,156,157,158,159,160,161,162,163,164,165,166,167,168,169,171,172,173,174,175,176,177,178,179,180,181,182,183,184,185,186,188,189,190,191,192,193,194,195,196,197,198,199,200,201,202,203,205,206,207,208,209,210,211,212,213,214,215,216,217,218,219,220,222,223,224,225,226,227,228,229,230,231,232,233,234,235,236,237,239,240,241,242,243,244,245,246,247,248,249,250,251,252,253,254,256,257,258,259,260,261,262,263,264,265,266,267,268,269,270,271]

allVlans=[18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,120,121,122,123,124,125,126,127,128,129,130,131,132,133,134,135,137,138,139,140,141,142,143,144,145,146,147,148,149,150,151,152,154,155,156,157,158,159,160,161,162,163,164,165,166,167,168,169,171,172,173,174,175,176,177,178,179,180,181,182,183,184,185,186,188,189,190,191,192,193,194,195,196,197,198,199,200,201,202,203,205,206,207,208,209,210,211,212,213,214,215,216,217,218,219,220,222,223,224,225,226,227,228,229,230,231,232,233,234,235,236,237,239,240,241,242,243,244,245,246,247,248,249,250,251,252,253,254,256,257,258,259,260,261,262,263,264,265,266,267,268,269,270,271]

path2Vlans=[291,292,293,294,295,296,297,298,299,300,301,302,303,304,307,308,309,310,311,312,313,314,315,316,317,318,319,320,321,322,325,326,327,328,329,330,331,332,333,334,335,336,337,338,341,342,343,344,345,346,347,348,349,350,351,352,353,354,355,356,359,360,361,362,363,364,365,366,367,368,369,370,371,372,375,376,377,378,379,380,381,382,383,384,385,386,387,388,389,390,393,394,395,396,397,398,399,400,401,402,403,404,405,406,409,410,411,412,413,414,415,416,417,418,419,420,421,422,423,424,427,428,429,430,431,432,433,434,435,436,437,438,439,440,443,444,445,446,447,448,449,450,451,452,453,454,455,456,457,458,461,462,463,464,465,466,467,468,469,470,471,472,473,474,477,478,479,480,481,482,483,484,485,486,487,488,489,490,491,492,495,496,497,498,499,500,501,502,503,504,505,506,507,508,511,512,513,514,515,516,517,518,519,520,521,522,523,524,525,526,529,530,531,532,533,534,535,536,537,538,539,540,541,542]

path3Vlans=[565,566,567,568,569,570,571,572,573,574,575,576,581,582,583,584,585,586,587,588,589,590,591,592,597,598,599,600,601,602,603,604,605,606,607,608,613,614,615,616,617,618,619,620,621,622,623,624,625,626,627,628,633,634,635,636,637,638,639,640,641,642,643,644,649,650,651,652,653,654,655,656,657,658,659,660,665,666,667,668,669,670,671,672,673,674,675,676,681,682,683,684,685,686,687,688,689,690,691,692,693,694,695,696,701,702,703,704,705,706,707,708,709,710,711,712,717,718,719,720,721,722,723,724,725,726,727,728,733,734,735,736,737,738,739,740,741,742,743,744,749,750,751,752,753,754,755,756,757,758,759,760,761,762,763,764,769,770,771,772,773,774,775,776,777,778,779,780,785,786,787,788,789,790,791,792,793,794,795,796,801,802,803,804,805,806,807,808,809,810,811,812]

path4Vlans=[837,838,839,840,841,842,843,844,845,846,847,848,853,854,855,856,857,858,859,860,861,862,863,864,869,870,871,872,873,874,875,876,877,878,879,880,885,886,887,888,889,890,891,892,893,894,895,896,897,898,899,900,905,906,907,908,909,910,911,912,913,914,915,916,921,922,923,924,925,926,927,928,929,930,931,932,937,938,939,940,941,942,943,944,945,946,947,948,953,954,955,956,957,958,959,960,961,962,963,964,965,966,967,968,973,974,975,976,977,978,979,980,981,982,983,984,989,990,991,992,993,994,995,996,997,998,999,1000,1005,1006,1007,1008,1009,1010,1011,1012,1013,1014,1015,1016,1021,1022,1023,1024,1025,1026,1027,1028,1029,1030,1031,1032,1033,1034,1035,1036,1041,1042,1043,1044,1045,1046,1047,1048,1049,1050,1051,1052,1057,1058,1059,1060,1061,1062,1063,1064,1065,1066,1067,1068,1073,1074,1075,1076,1077,1078,1079,1080,1081,1082,1083,1084]

#allVlans =[21]
pod1Vlans=[18,19,20,33,35,36,49,50,52,65,66,67,291,292,307,308,321,322,337,338]
pod2Vlans=[86,87,88,101,103,104,117,118,120,133,134,135,359,360,375,376,389,390,405,406]
pod3Vlans=[154,155,156,169,171,172,185,186,188,201,202,203,427,428,443,444,457,458,473,474]
pod4Vlans=[222,223,224,237,239,240,253,254,256,269,270,271,495,496,511,512,525,526,541,542]

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

#h16routing=[32,48,64,80,96,112,128,144,160,176,192,208,224,240,256]
h16routing=[32,48,64,80,96,112,128,144,160,176,192,208,224,240,256,304,576,848,320,592,864,336,608,880,352,624,896,368,640,912,384,656,928,400,672,944,416,688,960,432,704,976,448,720,992,464,736,1008,480,752,1024,496,512]

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
	   from_port_to_port(4, 1,291) #h1 to h3	
	   from_port_to_port(3, 2,35) #h2 to h3
	   from_port_to_port(3, 1,307) #h2 to h3
	   from_port_to_port(4, 2,20) #h1 to h4
	   from_port_to_port(4, 1,292) #h1 to h4
	   from_port_to_port(3, 2,36) #h2 to h4
	   from_port_to_port(3, 1,308) #h2 to h4
	
	   from_port_to_port(1, 4,49) #to h1
	   from_port_to_port(2, 4,321) #h1 from h3
           from_port_to_port(1, 3,50) #to h2
	   from_port_to_port(2, 3,322) #to h2 from h3
           from_port_to_port(1, 4,65) #to h1
	   from_port_to_port(2, 4,337) #to h1 from h4
           from_port_to_port(1, 3,66) #to h2
	   from_port_to_port(2, 3,338) #to h2 from h4
	
	   # for all other hosts send it to the core switch via switch 1
	   for n in allVlans:
		if n not in pod1Vlans and n not in pod2Vlans and n not in pod3Vlans and n not in pod4Vlans:
			from_port_to_port(4,1,n)
			from_port_to_port(3,1,n)

	   for n in path2Vlans:
                if n not in pod1Vlans and n not in pod2Vlans and n not in pod3Vlans and n not in pod4Vlans:
                        from_port_to_port(4,1,n)
                        from_port_to_port(3,1,n)
	
	   for n in path3Vlans:
                if n not in pod1Vlans and n not in pod2Vlans and n not in pod3Vlans and n not in pod4Vlans:
                        from_port_to_port(4,2,n)
                        from_port_to_port(3,2,n)

	   for n in path4Vlans:
                if n not in pod1Vlans and n not in pod2Vlans and n not in pod3Vlans and n not in pod4Vlans:
                        from_port_to_port(4,2,n)
                        from_port_to_port(3,2,n)

	   for n in allVlans + path2Vlans + path3Vlans + path4Vlans:
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
	   
 	   from_port_to_port(3,4,321) #h3 to h1
	   from_port_to_port(3,4,322) #h3 to h2
	   from_port_to_port(3,4,337) #h4 to h1
	   from_port_to_port(3,4,338) #h4 to h2

	   for n in allVlans + path2Vlans + path3Vlans + path4Vlans:
		if n not in pod1Vlans and n not in pod2Vlans and n not in pod3Vlans and n not in pod4Vlans:
			temp=n&15
			if temp in s24:
	                        from_port_to_port(1,4,n)
        	                from_port_to_port(2,4,n)
			elif temp in s23:
				from_port_to_port(1,3,n)
				from_port_to_port(2,3,n)
	   
	   for n in path3Vlans:
                if n not in pod1Vlans and n not in pod2Vlans and n not in pod3Vlans and n not in pod4Vlans:
 			from_port_to_port(4,1,n)
			from_port_to_port(3,1,n)

	   for n in path4Vlans:
                if n not in pod1Vlans and n not in pod2Vlans and n not in pod3Vlans and n not in pod4Vlans:
                        from_port_to_port(4,2,n)
                        from_port_to_port(3,2,n)

        if dp.id == 3:
	   from_port_to_port(4, 3,52) #h3 to h4
           from_port_to_port(3, 4,67) #h4 to h3

           from_port_to_port(2, 4,19) #to h3
	   from_port_to_port(1, 4,291) #to h3 from h1
           from_port_to_port(2, 3,20) #to h4
	   from_port_to_port(1, 3,292) #to h4 from h1
	   from_port_to_port(2, 4,35) #to h3
	   from_port_to_port(1, 4,307) #to h3 from h2
	   from_port_to_port(2, 3,36) #to h4
	   from_port_to_port(1, 3,308) #to h4 from h2
	   
	   from_port_to_port(4, 1,49) #h3 to h1
	   from_port_to_port(4, 2,321) #h3 to h1
           from_port_to_port(4, 1,50) #h3 to h2
	   from_port_to_port(4, 2,322) #h3 to h2
           from_port_to_port(3, 1,65) #h4 to h1
	   from_port_to_port(3, 2,337) #h4 to h1
           from_port_to_port(3, 1,66) #h4 to h2
	   from_port_to_port(3, 2,338) #h4 to h2
	 
	   #routing to core switches
           for n in allVlans:
		if n not in pod1Vlans and n not in pod2Vlans and n not in pod3Vlans and n not in pod4Vlans:
			from_port_to_port(4,1,n)
			from_port_to_port(3,1,n)

	   for n in path2Vlans:
                if n not in pod1Vlans and n not in pod2Vlans and n not in pod3Vlans and n not in pod4Vlans:
                        from_port_to_port(4,1,n)
                        from_port_to_port(3,1,n)

	   for n in path3Vlans:
                if n not in pod1Vlans and n not in pod2Vlans and n not in pod3Vlans and n not in pod4Vlans:
                        from_port_to_port(4,2,n)
                        from_port_to_port(3,2,n)

	   for n in path4Vlans:
                if n not in pod1Vlans and n not in pod2Vlans and n not in pod3Vlans and n not in pod4Vlans:
                        from_port_to_port(4,2,n)
                        from_port_to_port(3,2,n)

	   for n in allVlans + path2Vlans + path3Vlans + path4Vlans:
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

	   from_port_to_port(4, 3,291) #h1 to h3
	   from_port_to_port(4, 3,292) #h1 to h4
	   from_port_to_port(4, 3,307) #h2 to h3 
	   from_port_to_port(4, 3,308) #h2 to h4

	   #routing to core switches
	   for n in allVlans:
		if n not in pod1Vlans and n not in pod2Vlans and n not in pod3Vlans and n not in pod4Vlans:
                        from_port_to_port(4,1,n)
                        from_port_to_port(3,1,n)

	   for n in path2Vlans:
                if n not in pod1Vlans and n not in pod2Vlans and n not in pod3Vlans and n not in pod4Vlans:
                        from_port_to_port(4,2,n)
                        from_port_to_port(3,2,n)

	   for n in allVlans + path2Vlans + path3Vlans + path4Vlans:
		if n not in pod1Vlans and n not in pod2Vlans and n not in pod3Vlans and n not in pod4Vlans:
			temp=n&15
			if temp in s14:
	                        from_port_to_port(2,4,n)
				from_port_to_port(1,4,n)
			elif temp in s13:
	                        from_port_to_port(2,3,n)
				from_port_to_port(1,3,n)
	   
	#pod 2 internal routing
	if dp.id == 8:
           from_port_to_port(4, 3,86) #h5 to h6
           from_port_to_port(3, 4,101) #h6 to h5

           from_port_to_port(4, 2,87) #h5 to h7
	   from_port_to_port(4, 1,359) #h5 to h7
           from_port_to_port(3, 2,103) #h6 to h7
	   from_port_to_port(3, 1,375) #h6 to h7
           from_port_to_port(4, 2,88) #h5 to h8
	   from_port_to_port(4, 1,360) #h5 to h8
           from_port_to_port(3, 2,104) #h6 to h8
	   from_port_to_port(3, 1,376) #h6 to h8 

           from_port_to_port(1, 4,117) #to h5
	   from_port_to_port(2, 4,389) #to h5 from h7
           from_port_to_port(1, 3,118) #to h6
	   from_port_to_port(2, 3,390) #to h6 from h7
           from_port_to_port(1, 4,133) #to h5
 	   from_port_to_port(2, 4,405) #to h5 from h8
           from_port_to_port(1, 3,134) #to h6
	   from_port_to_port(2, 3,406) #to h6 from h8
	
	   #routing to core switches
           for n in allVlans:
		if n not in pod1Vlans and n not in pod2Vlans and n not in pod3Vlans and n not in pod4Vlans:
                        from_port_to_port(4,1,n)
	  		from_port_to_port(3,1,n)

	   for n in path2Vlans:
                if n not in pod1Vlans and n not in pod2Vlans and n not in pod3Vlans and n not in pod4Vlans:
                        from_port_to_port(4,1,n)
                        from_port_to_port(3,1,n)
 
	   for n in path3Vlans:
                if n not in pod1Vlans and n not in pod2Vlans and n not in pod3Vlans and n not in pod4Vlans:
                        from_port_to_port(4,2,n)
                        from_port_to_port(3,2,n)

	   for n in path4Vlans:
                if n not in pod1Vlans and n not in pod2Vlans and n not in pod3Vlans and n not in pod4Vlans:
                        from_port_to_port(4,2,n)
                        from_port_to_port(3,2,n)

	   for n in allVlans + path2Vlans + path3Vlans + path4Vlans:
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
	
	   from_port_to_port(3,4,389) #h7 to h5	
	   from_port_to_port(3,4,390) #h7 to h6
	   from_port_to_port(3,4,405) #h8 to h5
	   from_port_to_port(3,4,406) #h8 to h6
   
	   for n in allVlans + path2Vlans + path3Vlans + path4Vlans:
		if n not in pod1Vlans and n not in pod2Vlans and n not in pod3Vlans and n not in pod4Vlans:
			temp=n&15
                        if temp in s68:
                                from_port_to_port(1,4,n)
				from_port_to_port(2,4,n)
                        elif temp in s67:
                                from_port_to_port(1,3,n)
				from_port_to_port(2,3,n)
	
	   for n in path3Vlans:
                if n not in pod1Vlans and n not in pod2Vlans and n not in pod3Vlans and n not in pod4Vlans:
			from_port_to_port(4,1,n)
			from_port_to_port(3,1,n)

	   for n in path4Vlans:
                if n not in pod1Vlans and n not in pod2Vlans and n not in pod3Vlans and n not in pod4Vlans:
                        from_port_to_port(4,2,n)
                        from_port_to_port(3,2,n)

        if dp.id == 7:
           from_port_to_port(4, 3,120) #h7 to h8
           from_port_to_port(3, 4,135) #h8 to h7

           from_port_to_port(2, 4,87) #to h7
	   from_port_to_port(1, 4,359) #to h7 from h5
           from_port_to_port(2, 3,88) #to h8
	   from_port_to_port(1, 3,360) #to h8 from h5
           from_port_to_port(2, 4,103) #to h7
	   from_port_to_port(1, 4,375) #to h7 from h6
           from_port_to_port(2, 3,104) #to h8
	   from_port_to_port(1, 3,376) #to h8 from h6

           from_port_to_port(4, 1,117) #h7 to h5
	   from_port_to_port(4, 2,389) #h7 to h5
           from_port_to_port(4, 1,118) #h7 to h6
	   from_port_to_port(4, 2,390) #h7 to h6
           from_port_to_port(3, 1,133) #h8 to h5
	   from_port_to_port(3, 2,405) #h8 to h5
           from_port_to_port(3, 1,134) #h8 to h6
	   from_port_to_port(3, 2,406) #h8 to h6

	   #routing to core switches
           for n in allVlans:
		if n not in pod1Vlans and n not in pod2Vlans and n not in pod3Vlans and n not in pod4Vlans:
                        from_port_to_port(4,1,n)
			from_port_to_port(3,1,n)

	   for n in path2Vlans:
                if n not in pod1Vlans and n not in pod2Vlans and n not in pod3Vlans and n not in pod4Vlans:
                        from_port_to_port(4,1,n)
                        from_port_to_port(3,1,n)
	
	   for n in path3Vlans:
                if n not in pod1Vlans and n not in pod2Vlans and n not in pod3Vlans and n not in pod4Vlans:
                        from_port_to_port(4,2,n)
                        from_port_to_port(3,2,n)

	   for n in path4Vlans:
                if n not in pod1Vlans and n not in pod2Vlans and n not in pod3Vlans and n not in pod4Vlans:
                        from_port_to_port(4,2,n)
                        from_port_to_port(3,2,n)

	
	   for n in allVlans + path2Vlans + path3Vlans + path4Vlans:
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

	   from_port_to_port(4,3,359) #h5 to h7
	   from_port_to_port(4,3,360) #h5 to h8
	   from_port_to_port(4,3,375) #h6 to h7
	   from_port_to_port(4,3,376) #h6 to h8

	   #routing to core switches
           for n in allVlans:
		if n not in pod1Vlans and n not in pod2Vlans and n not in pod3Vlans and n not in pod4Vlans:
                        from_port_to_port(4,2,n)
                        from_port_to_port(3,2,n)

	   for n in path2Vlans:
                if n not in pod1Vlans and n not in pod2Vlans and n not in pod3Vlans and n not in pod4Vlans:
                        from_port_to_port(4,1,n)
                        from_port_to_port(3,1,n)

	   for n in allVlans + path2Vlans + path3Vlans + path4Vlans:
		if n not in pod1Vlans and n not in pod2Vlans and n not in pod3Vlans and n not in pod4Vlans:
			temp=n&15
                        if temp in s58:
                                from_port_to_port(1,4,n)
				from_port_to_port(2,4,n)
                        elif temp in s57:
                                from_port_to_port(1,3,n)
				from_port_to_port(2,3,n)
	
	#pod 3 internal routing
        if dp.id == 12:
           from_port_to_port(4, 3,154) #h9 to h10
           from_port_to_port(3, 4,169) #h10 to h9
           
	   from_port_to_port(4, 2,155) #h9 to h11
	   from_port_to_port(4, 1,427) #h9 to h11
           from_port_to_port(3, 2,171) #h10 to h11
	   from_port_to_port(3, 1,443) #h10 to h11
           from_port_to_port(4, 2,156) #h9 to h12
	   from_port_to_port(4, 1,428) #h9 to h12
           from_port_to_port(3, 2,172) #h10 to h12
	   from_port_to_port(3, 1,444) #h10 to h12

           from_port_to_port(1, 4,185) #to h9
	   from_port_to_port(2, 4,457) #to h9 from h11
           from_port_to_port(1, 3,186) #to h10
 	   from_port_to_port(2, 3,458) #to h10 from h11
           from_port_to_port(1, 4,201) #to h9
	   from_port_to_port(2, 4,473) #to h9 from h12
           from_port_to_port(1, 3,202) #to h10
	   from_port_to_port(2, 3,474) #to h10 from h12
	  
	   #routing to core switches
           for n in allVlans:
		if n not in pod1Vlans and n not in pod2Vlans and n not in pod3Vlans and n not in pod4Vlans:
                        from_port_to_port(4,2,n)
			from_port_to_port(3,2,n)

	   for n in path2Vlans:
                if n not in pod1Vlans and n not in pod2Vlans and n not in pod3Vlans and n not in pod4Vlans:
                        from_port_to_port(4,2,n)
                        from_port_to_port(3,2,n)

	   for n in path3Vlans:
                if n not in pod1Vlans and n not in pod2Vlans and n not in pod3Vlans and n not in pod4Vlans:
                        from_port_to_port(4,1,n)
                        from_port_to_port(3,1,n)

	   for n in path4Vlans:
                if n not in pod1Vlans and n not in pod2Vlans and n not in pod3Vlans and n not in pod4Vlans:
                        from_port_to_port(4,1,n)
                        from_port_to_port(3,1,n)


	   for n in allVlans + path2Vlans + path3Vlans + path4Vlans:
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
	
	   from_port_to_port(3,4,457) #h11 to h9
	   from_port_to_port(3,4,458) #h11 to h10
	   from_port_to_port(3,4,473) #h12 to h9
	   from_port_to_port(3,4,474) #h12 to h10 

	   #routing to core switches
           for n in allVlans:
		if n not in pod1Vlans and n not in pod2Vlans and n not in pod3Vlans and n not in pod4Vlans:
                        from_port_to_port(4,1,n)
                        from_port_to_port(3,1,n)

	   for n in path2Vlans:
                if n not in pod1Vlans and n not in pod2Vlans and n not in pod3Vlans and n not in pod4Vlans:
                        from_port_to_port(4,2,n)
                        from_port_to_port(3,2,n)


	   for n in allVlans + path2Vlans + path3Vlans + path4Vlans:
		if n not in pod1Vlans and n not in pod2Vlans and n not in pod3Vlans and n not in pod4Vlans:
			temp=n&15
                        if temp in s1012:
                                from_port_to_port(2,4,n)
				from_port_to_port(1,4,n)
                        elif temp in s1011:
                                from_port_to_port(2,3,n)
				from_port_to_port(1,3,n)

        if dp.id == 11:
           from_port_to_port(4, 3,188) #h11 to h12
           from_port_to_port(3, 4,203) #h12 to h11

           from_port_to_port(2, 4,155) #to h11
	   from_port_to_port(1, 4,427) #to h11 from h9
           from_port_to_port(2, 3,156) #to h12
	   from_port_to_port(1, 3,428) #to h12 from h9
           from_port_to_port(2, 4,171) #to h11
	   from_port_to_port(1, 4,443) #to h11 from h10
           from_port_to_port(2, 3,172) #to h12
	   from_port_to_port(1, 3,444) #to h12 from h10

           from_port_to_port(4, 1,185) #h11 to h9
	   from_port_to_port(4, 2,457) #h11 to h9
           from_port_to_port(4, 1,186) #h11 to h10
	   from_port_to_port(4, 2,458) #h11 to h10
           from_port_to_port(3, 1,201) #h12 to h9
	   from_port_to_port(3, 2,473) #h12 to h9
           from_port_to_port(3, 1,202) #h12 to h10
	   from_port_to_port(3, 2,474) #h12 to h10 

	   #routing to core switches
           for n in allVlans:
		if n not in pod1Vlans and n not in pod2Vlans and n not in pod3Vlans and n not in pod4Vlans:
			from_port_to_port(4,2,n)
                        from_port_to_port(3,2,n)

	   for n in path2Vlans:
                if n not in pod1Vlans and n not in pod2Vlans and n not in pod3Vlans and n not in pod4Vlans:
                        from_port_to_port(4,2,n)
                        from_port_to_port(3,2,n)

	   for n in path3Vlans:
                if n not in pod1Vlans and n not in pod2Vlans and n not in pod3Vlans and n not in pod4Vlans:
                        from_port_to_port(4,1,n)
                        from_port_to_port(3,1,n)

	   for n in path4Vlans:
                if n not in pod1Vlans and n not in pod2Vlans and n not in pod3Vlans and n not in pod4Vlans:
                        from_port_to_port(4,1,n)
                        from_port_to_port(3,1,n)


	   for n in allVlans + path2Vlans + path3Vlans + path4Vlans:
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
	  
	   from_port_to_port(4,3,427) #h9 to h11
	   from_port_to_port(4,3,428) #h9 to h12 
	   from_port_to_port(4,3,443) #h10 to h11
	   from_port_to_port(4,3,444) #h10 to h12

	   #routing to core switches
	   for n in allVlans + path2Vlans + path3Vlans + path4Vlans:
		if n not in pod1Vlans and n not in pod2Vlans and n not in pod3Vlans and n not in pod4Vlans:
			temp=n&15
                        if temp in s912:
                                from_port_to_port(1,4,n)
				from_port_to_port(2,4,n)
                        elif temp in s911:
                                from_port_to_port(1,3,n)
				from_port_to_port(2,3,n)

	   for n in path3Vlans:
                if n not in pod1Vlans and n not in pod2Vlans and n not in pod3Vlans and n not in pod4Vlans:
			from_port_to_port(4,1,n)
			from_port_to_port(3,1,n)

	   for n in path4Vlans:
                if n not in pod1Vlans and n not in pod2Vlans and n not in pod3Vlans and n not in pod4Vlans:
                        from_port_to_port(4,2,n)
                        from_port_to_port(3,2,n)
	

	#pod 4 internal routing
        if dp.id == 16:
           from_port_to_port(4, 3,222) #h13 to h14
           from_port_to_port(3, 4,237) #h14 to h13

           from_port_to_port(4, 2,223) #h13 to h15
	   from_port_to_port(4, 1,495) #h13 to h15
           from_port_to_port(3, 2,239) #h14 to h15
	   from_port_to_port(3, 1,511) #h14 to h15
           from_port_to_port(4, 2,224) #h13 to h16
	   from_port_to_port(4, 1,496) #h13 to h16
           from_port_to_port(3, 2,240) #h14 to h16
	   from_port_to_port(3, 1,512) #h14 to h16

           from_port_to_port(1, 4,253) #to h13
	   from_port_to_port(2, 4,525) #to h13 from h15
           from_port_to_port(1, 3,254) #to h14
	   from_port_to_port(2, 3,526) #to h14 from h15
           from_port_to_port(1, 4,269) #to h13
	   from_port_to_port(2, 4,541) #to h13 from h16
           from_port_to_port(1, 3,270) #to h14
	   from_port_to_port(2, 3,542) #to h14 from h16

	   #routing to core switches
           for n in allVlans:
		if n not in pod1Vlans and n not in pod2Vlans and n not in pod3Vlans and n not in pod4Vlans:
			from_port_to_port(4,2,n)
                        from_port_to_port(3,2,n)

	   for n in path2Vlans:
                if n not in pod1Vlans and n not in pod2Vlans and n not in pod3Vlans and n not in pod4Vlans:
                        from_port_to_port(4,2,n)
                        from_port_to_port(3,2,n)

	   for n in path3Vlans:
                if n not in pod1Vlans and n not in pod2Vlans and n not in pod3Vlans and n not in pod4Vlans:
                        from_port_to_port(4,1,n)
                        from_port_to_port(3,1,n)

	   for n in path4Vlans:
                if n not in pod1Vlans and n not in pod2Vlans and n not in pod3Vlans and n not in pod4Vlans:
                        from_port_to_port(4,1,n)
                        from_port_to_port(3,1,n)


	   for n in allVlans + path2Vlans + path3Vlans + path4Vlans:
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
	
	   from_port_to_port(3,4,525) #h15 to h13
	   from_port_to_port(3,4,526) #h15 to h14
	   from_port_to_port(3,4,541) #h16 to h13
	   from_port_to_port(3,4,542) #h16 to h14

	   #routing to core switches
           for n in allVlans:
		if n not in pod1Vlans and n not in pod2Vlans and n not in pod3Vlans and n not in pod4Vlans:
                        from_port_to_port(4,2,n)
                        from_port_to_port(3,2,n)
	   
	   for n in path2Vlans:
                if n not in pod1Vlans and n not in pod2Vlans and n not in pod3Vlans and n not in pod4Vlans:
                        from_port_to_port(4,1,n)
                        from_port_to_port(3,1,n)


	   for n in allVlans + path2Vlans + path3Vlans + path4Vlans:
		if n not in pod1Vlans and n not in pod2Vlans and n not in pod3Vlans and n not in pod4Vlans:
			if n in h16routing:
                                temp=16
                        else:
                                temp = n&15
                        if temp in s1416:
                                from_port_to_port(1,4,n)
				from_port_to_port(2,4,n)
                        elif temp in s1415:
                                from_port_to_port(1,3,n)
				from_port_to_port(2,3,n)

        if dp.id == 15:
           from_port_to_port(4, 3,256) #h15 to h16
           from_port_to_port(3, 4,271) #h16 to h15

           from_port_to_port(2, 4,223) #to h15
	   from_port_to_port(1, 4,495) #to h15 from h13
           from_port_to_port(2, 3,224) #to h16
	   from_port_to_port(1, 3,496) #to h16 from h13
           from_port_to_port(2, 4,239) #to h15
	   from_port_to_port(1, 4,511) #to h15 from h14
           from_port_to_port(2, 3,240) #to h16
	   from_port_to_port(1, 3,512) #to h16 from h14

           from_port_to_port(4, 1,253) #h15 to h13
	   from_port_to_port(4, 2,525) #h15 to h13
           from_port_to_port(4, 1,254) #h15 to h14
	   from_port_to_port(4, 2,526) #h15 to h14
           from_port_to_port(3, 1,269) #h16 to h13
	   from_port_to_port(3, 2,541) #h16 to h13
           from_port_to_port(3, 1,270) #h16 to h14
	   from_port_to_port(3, 2,542) #h16 to h14

	   #routing to core switches
           for n in allVlans:
		if n not in pod1Vlans and n not in pod2Vlans and n not in pod3Vlans and n not in pod4Vlans:
                        from_port_to_port(4,2,n)
                        from_port_to_port(3,2,n)

	   for n in path2Vlans:
                if n not in pod1Vlans and n not in pod2Vlans and n not in pod3Vlans and n not in pod4Vlans:
                        from_port_to_port(4,2,n)
                        from_port_to_port(3,2,n)

	   for n in path3Vlans:
                if n not in pod1Vlans and n not in pod2Vlans and n not in pod3Vlans and n not in pod4Vlans:
                        from_port_to_port(4,1,n)
                        from_port_to_port(3,1,n)

	   for n in path4Vlans:
                if n not in pod1Vlans and n not in pod2Vlans and n not in pod3Vlans and n not in pod4Vlans:
                        from_port_to_port(4,1,n)
                        from_port_to_port(3,1,n)


	   for n in allVlans + path2Vlans + path3Vlans + path4Vlans:
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
		
	   from_port_to_port(4,3,495) #h13 to h15
	   from_port_to_port(4,3,496) #h13 to h16
	   from_port_to_port(4,3,511) #h14 to h15
	   from_port_to_port(4,3,512) #h14 to h16

	   #routing to core switches
	   for n in allVlans + path2Vlans + path3Vlans + path4Vlans:
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
	
	   for n in path3Vlans:
           	if n not in pod1Vlans and n not in pod2Vlans and n not in pod3Vlans and n not in pod4Vlans:
			from_port_to_port(4,1,n)
			from_port_to_port(3,1,n)
	
	   for n in path4Vlans:
                if n not in pod1Vlans and n not in pod2Vlans and n not in pod3Vlans and n not in pod4Vlans:
                        from_port_to_port(4,2,n)
                        from_port_to_port(3,2,n)


	#core switches routing
	if dp.id == 17:
           for n in allVlans + path2Vlans + path3Vlans + path4Vlans:
		if n not in pod1Vlans and n not in pod2Vlans and n not in pod3Vlans and n not in pod4Vlans:
			#get the destination host
			if n in h16routing:
				temp=16
			else:
				temp = n&15

			if temp in pod2:	
				from_port_to_port(1,2,n)
				from_port_to_port(3,2,n)
				from_port_to_port(4,2,n)
			elif temp in pod3:
				from_port_to_port(1,3,n)
				from_port_to_port(2,3,n)
				from_port_to_port(4,3,n)
			elif temp in pod4:
				from_port_to_port(1,4,n)
				from_port_to_port(2,4,n)
				from_port_to_port(3,4,n)
			elif temp in pod1:
				from_port_to_port(2,1,n)
				from_port_to_port(3,1,n)
				from_port_to_port(4,1,n)

	if dp.id == 18:
           for n in allVlans + path2Vlans + path3Vlans + path4Vlans:
		if n not in pod1Vlans and n not in pod2Vlans and n not in pod3Vlans and n not in pod4Vlans:
			if n in h16routing:
                                temp=16
                        else:
                                temp = n&15
			if temp in pod1:
                                from_port_to_port(2,1,n)
				from_port_to_port(3,1,n)
				from_port_to_port(4,1,n)
                        elif temp in pod3:
                                from_port_to_port(2,3,n)
				from_port_to_port(1,3,n)
				from_port_to_port(4,3,n)
                        elif temp in pod4:
                                from_port_to_port(2,4,n)
				from_port_to_port(1,4,n)
				from_port_to_port(3,4,n)
			elif temp in pod2:
				from_port_to_port(1,2,n)
				from_port_to_port(3,2,n)
				from_port_to_port(4,2,n)

	if dp.id == 19:
           for n in allVlans + path2Vlans + path3Vlans + path4Vlans:
		if n not in pod1Vlans and n not in pod2Vlans and n not in pod3Vlans and n not in pod4Vlans:
			if n in h16routing:
                                temp=16
                        else:
                                temp = n&15
                        if temp in pod1:
                                from_port_to_port(3,1,n)
				from_port_to_port(2,1,n)
				from_port_to_port(4,1,n)
                        elif temp in pod2:
                                from_port_to_port(3,2,n)
				from_port_to_port(1,2,n)
				from_port_to_port(4,2,n)
                        elif temp in pod4:
                                from_port_to_port(3,4,n)
				from_port_to_port(1,4,n)
				from_port_to_port(2,4,n)
			elif temp in pod3:
				from_port_to_port(1,3,n)
				from_port_to_port(2,3,n)
				from_port_to_port(4,3,n)

	if dp.id == 20:
           for n in allVlans + path2Vlans + path3Vlans + path4Vlans:
		if n not in pod1Vlans and n not in pod2Vlans and n not in pod3Vlans and n not in pod4Vlans:
			if n in h16routing:
                                temp=16
                        else:
                                temp = n&15
                        if temp in pod1:
                                from_port_to_port(4,1,n)
				from_port_to_port(3,1,n)
				from_port_to_port(2,1,n)
                        elif temp in pod2:
                                from_port_to_port(4,2,n)
				from_port_to_port(1,2,n)
				from_port_to_port(3,2,n)
                        elif temp in pod3:
                                from_port_to_port(4,3,n)
				from_port_to_port(1,3,n)
				from_port_to_port(2,3,n)
			elif temp in pod4:
				from_port_to_port(1,4,n)
				from_port_to_port(2,4,n)
				from_port_to_port(3,4,n)


