from ryu.base import app_manager
from ryu.controller import ofp_event, dpset
from ryu.controller.handler import MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
import itertools
#hosts
a=['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16']
commonArray=[]
dictionary={}
#pods
one=['01','02','03','04']
two=['05','06','07','08']
three=['09','10','11','12']
four=['13','14','15','16']

oneone=['01','05']
#packets coming into the pods
#pod_Numb_HostNum_in: pod1, hosts 1 to 4
pod11in=[]
pod12in=[]
pod13in=[]
pod14in=[]
#pod_Numb_HostNum_in: pod2, hosts 5 to 8
pod25in=[]
pod26in=[]
pod27in=[]
pod28in=[]
#pod_Numb_HostNum_in: pod3, hosts 9 to 12
pod39in=[]
pod310in=[]
pod311in=[]
pod312in=[]
#pod_Numb_HostNum_in: pod4, hosts 13 to 16
pod413in=[]
pod414in=[]
pod415in=[]
pod416in=[]

#packets going out of the pods
#pod 1 hosts 1 to 4
pod11out=[]
pod12out=[]
pod13out=[]
pod14out=[]
#pod 2 hosts 5 to 8
pod25out=[]
pod26out=[]
pod27out=[]
pod28out=[]
#pod 3 hosts 9 to 12
pod39out=[]
pod310out=[]
pod311out=[]
pod312out=[]
#pod 4 hosts 13 to 16
pod413out=[]
pod414out=[]
pod415out=[]
pod416out=[]

#pod 1 hosts 1-4
pod11=[]
pod12=[]
pod13=[]
pod14=[]
#pod 2 hosts 5-8
pod25=[]
pod26=[]
pod27=[]
pod28=[]
#pod 3 hosts 9-12
pod39=[]
pod310=[]
pod311=[]
pod312=[]
#pod 4 hosts 13-16
pod413=[]
pod414=[]
pod415=[]
pod416=[]


pod2=[]
pod3=[]
pod4=[]
ipod1=[]
ipod2=[]
ipod3=[]
ipod4=[]
class Controller(app_manager.RyuApp):
    def __init__(self, *args, **kwargs):
        super(Controller, self).__init__(*args, **kwargs)
    @set_ev_cls(dpset.EventDP, MAIN_DISPATCHER)
    def switch_in(self, ev):
	global ipod1
	ipod1=[]
	global ipod2
	ipod2=[]
	global ipod3
	ipod3=[]
	global ipod4
	ipod4=[]
	global pod11
	pod11=[]       	
        global pod12
        pod12=[]
        global pod13
        pod13=[]
        global pod14
        pod14=[]
        global pod25
        pod25=[]
        global pod26
        pod26=[]
        global pod27
        pod27=[]
        global pod28
        pod28=[]
        global pod39
        pod39=[]
        global pod310
        pod310=[]
        global pod311
        pod311=[]
        global pod312
        pod312=[]
        global pod413
        pod413=[]
        global pod414
        pod414=[]
        global pod415
        pod415=[]
        global pod416
        pod416=[]

 	global pod11in
        pod11in=[]
        global pod12in
        pod12in=[]
        global pod13in
        pod13in=[]
        global pod14in
        pod14in=[]
        global pod25in
        pod25in=[]
        global pod26in
        pod26in=[]
        global pod27in
        pod27in=[]
        global pod28in
        pod28in=[]
        global pod39in
        pod39in=[]
        global pod310in
        pod310in=[]
        global pod311in
        pod311in=[]
        global pod312in
        pod312in=[]
        global pod413in
        pod413in=[]
        global pod414in
        pod414in=[]
        global pod415in
        pod415in=[]
        global pod416in
        pod416in=[]


 	global pod11out
        pod11out=[]
        global pod12out
        pod12out=[]
        global pod13out
        pod13out=[]
        global pod14out
        pod14out=[]
        global pod25out
        pod25out=[]
        global pod26out
        pod26out=[]
        global pod27out
        pod27out=[]
        global pod28out
        pod28out=[]
        global pod39out
        pod39out=[]
        global pod310out
        pod310out=[]
        global pod311out
        pod311out=[]
        global pod312out
        pod312out=[]
        global pod413out
        pod413out=[]
        global pod414out
        pod414out=[]
        global pod415out
        pod415out=[]
        global pod416out
        pod416out=[]

        #get all the possible source and destinations in pod1
        #output for pod 1 will be like
        #102 103 104 201 203 204 301 302 304 401 402 403
	for p in itertools.permutations(one, 2):
		global ipod1
		#join: between every element in p add a '' and append
		ipod1.append(int(''.join(p)))
	#get the vlan id for pod2.
	for p in itertools.permutations(two, 2):
                global ipod2
	        ipod2.append(int(''.join(p)))
	#get the vlan id for pod3
	for p in itertools.permutations(three, 2):
                global ipod3
 	 	ipod3.append(int(''.join(p)))
 	#get the vlan id for pod4
	for p in itertools.permutations(four, 2):
		global ipod4
                ipod4.append(int(''.join(p)))
	
       	for p in ['05','06','07','08','09','10','11','12','13','14','15','16']:
		global pod11
		global pod11in
		global pod11out
		pod11.append(int('01'+p))
		pod11out.append(int('01'+p))
		pod11.append(int(p+'01'))
		pod11in.append(int(p+'01'))
	for p in ['05','06','07','08','09','10','11','12','13','14','15','16']:
                global pod12
                global pod12in
                global pod12out
                pod12.append(int('02'+p)) 
                pod12out.append(int('02'+p)) 
                pod12.append(int(p+'02')) 
                pod12in.append(int(p+'02')) 
       	for p in ['05','06','07','08','09','10','11','12','13','14','15','16']:
                global pod13
                global pod13in
                global pod13out
                pod13.append(int('03'+p))
                pod13out.append(int('03'+p))
                pod13.append(int(p+'03'))
                pod13in.append(int(p+'03'))
       	for p in ['05','06','07','08','09','10','11','12','13','14','15','16']:
                global pod14
                global pod14in
                global pod14out
                pod14.append(int('04'+p))
                pod14out.append(int('04'+p))
                pod14.append(int(p+'04'))
                pod14in.append(int(p+'04'))
       	for p in ['01','02','03','04','09','10','11','12','13','14','15','16']:
                global pod25
                global pod25in
                global pod25out
                pod25.append(int('05'+p))
                pod25out.append(int('05'+p))
                pod25.append(int(p+'05'))
                pod25in.append(int(p+'05'))
       	for p in ['01','02','03','04','09','10','11','12','13','14','15','16']:
                global pod26
                global pod26in
                global pod26out
                pod26.append(int('06'+p))
                pod26out.append(int('06'+p))
                pod26.append(int(p+'06'))
                pod26in.append(int(p+'06'))
       	for p in ['01','02','03','04','09','10','11','12','13','14','15','16']:
                global pod27
                global pod27in
                global pod27out
                pod27.append(int('07'+p))
                pod27out.append(int('07'+p))
                pod27.append(int(p+'07'))
                pod27in.append(int(p+'07'))
       	for p in ['01','02','03','04','09','10','11','12','13','14','15','16']:
                global pod28
                global pod28in
                global pod28out
                pod28.append(int('08'+p))
                pod28out.append(int('08'+p))
                pod28in.append(int(p+'08'))
                pod28.append(int(p+'08'))
       	for p in ['01','02','03','04','05','06','07','08','13','14','15','16']:
                global pod39
                global pod39in
                global pod39out
                pod39.append(int('09'+p))
                pod39out.append(int('09'+p))
                pod39.append(int(p+'09'))
                pod39in.append(int(p+'09'))
       	for p in ['01','02','03','04','05','06','07','08','13','14','15','16']:
                global pod310
                global pod310in
                global pod310out
                pod310.append(int('10'+p))
                pod310out.append(int('10'+p))
                pod310.append(int(p+'10'))
                pod310in.append(int(p+'10'))
       	for p in ['01','02','03','04','05','06','07','08','13','14','15','16']:
                global pod311
                global pod311in
                global pod311out
                pod311.append(int('11'+p))
                pod311out.append(int('11'+p))
                pod311.append(int(p+'11'))
                pod311in.append(int(p+'11'))
       	for p in ['01','02','03','04','05','06','07','08','13','14','15','16']:
                global pod312
                global pod312in
                global pod312out
                pod312.append(int('12'+p))
                pod312out.append(int('12'+p))
                pod312.append(int(p+'12'))
                pod312in.append(int(p+'12'))
       	for p in ['01','02','03','04','05','06','07','08','09','10','11','12']:
                global pod413
                global pod413in
                global pod413out
                pod413.append(int('13'+p))
                pod413out.append(int('13'+p))
                pod413.append(int(p+'13'))
                pod413in.append(int(p+'13'))
       	for p in ['01','02','03','04','05','06','07','08','09','10','11','12']:
                global pod414
                global pod414in
                global pod414out
                pod414.append(int('14'+p))
                pod414out.append(int('14'+p))
                pod414in.append(int(p+'14'))
                pod414.append(int(p+'14'))
       	for p in ['01','02','03','04','05','06','07','08','09','10','11','12']:
                global pod415
                global pod415in
                global pod415out
                pod415.append(int('15'+p))
                pod415out.append(int('15'+p))
                pod415.append(int(p+'15'))
                pod415in.append(int(p+'15'))
       	for p in ['01','02','03','04','05','06','07','08','09','10','11','12']:
                global pod416
                global pod416in
                global pod416out
                pod416.append(int('16'+p))
                pod416out.append(int('16'+p))
                pod416.append(int(p+'16'))
                pod416in.append(int(p+'16'))

	i=1
	count=0
	while True:
        	if count>=15:
                	break
        	if i==3 or i==4 or i==7 or i==8 or i==11 or i==12:
                	i=i+1
                	continue
        	global temp1
		temp1=[]
		global temp2
        	temp2=[]
		global temp3
        	temp3=[]
		global temp4
        	temp4=[]
		global commonArray
		commonArray=[]
		
        	for p in itertools.permutations(a, 2):
                	str1=''.join(p)
			global commonArray
                	commonArray.append(int(str1))

                	if str1[-2:]==a[count]:
                        	global temp1
				temp1.append(int(str1))
                        	tempstr1='s'+str(i)+'h'+str(1)+'in'
                	if str1[:2]==a[count]:
				global temp2
                        	temp2.append(int(str1))
                        	tempstr2='s'+str(i)+'h'+str(1)+'out'
                	if str1[-2:]==a[count+1]:
				global temp3
                        	temp3.append(int(str1))
                        	tempstr3='s'+str(i)+'h'+str(2)+'in'
                	if str1[:2]==a[count+1]:
				global temp4
                        	temp4.append(int(str1))
                        	tempstr4='s'+str(i)+'h'+str(2)+'out'
        	count=count+2
        	i=i+1
		global dictionary
        	dictionary[tempstr1]=temp1
        	dictionary[tempstr2]=temp2
        	dictionary[tempstr3]=temp3
        	dictionary[tempstr4]=temp4
		

	count=0
	for i in dictionary:
		count=count+1
        dp  = ev.dp
        entered = ev.enter
        if ev.enter:
            self.install_rules(dp)
    def install_rules(self, dp):
        ofp        = dp.ofproto
        ofp_parser = dp.ofproto_parser
        dp.send_delete_all_flows()

        # Creates a rule that sends out packets coming
        # from port: inport to the port: outport
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
	print "pod413out-pod312in",pod413out
	print "pod414out",pod414out
	print "pod415out",pod415out
	print "pod416out",pod416out
	

	if dp.id == 1:
		#s1h1in
		for i in dictionary['s1h1in']:
			from_port_to_port(3,1,i)
			from_port_to_port(4,1,i)
		for i in dictionary['s1h2in']:
			from_port_to_port(3,2,i)
			from_port_to_port(4,2,i)
		for i in dictionary['s1h1out']:
			from_port_to_port(1,3,i)
		for i in dictionary['s1h2out']:
			from_port_to_port(2,3,i)
		from_port_to_port(2,1,201)
		from_port_to_port(1,2,102)		


        if dp.id == 5:
                #s1h1in
                for i in dictionary['s5h1in']:
                        from_port_to_port(3,1,i)
                        from_port_to_port(4,1,i)
                for i in dictionary['s5h2in']:
                        from_port_to_port(3,2,i)
                        from_port_to_port(4,2,i)

                for i in dictionary['s5h1out']:
                        from_port_to_port(1,3,i)
                for i in dictionary['s5h2out']:
                        from_port_to_port(2,3,i)
                from_port_to_port(2,1,605)
                from_port_to_port(1,2,506)


        if dp.id == 9:
                #s1h1in
                for i in dictionary['s9h1in']:
                        from_port_to_port(3,1,i)
                        from_port_to_port(4,1,i)
                for i in dictionary['s9h2in']:
                        from_port_to_port(3,2,i)
                        from_port_to_port(4,2,i)
                for i in dictionary['s9h1out']:
                        from_port_to_port(1,3,i)
                for i in dictionary['s9h2out']:
                        from_port_to_port(2,3,i)
                from_port_to_port(2,1,1009)
                from_port_to_port(1,2,910)


	if dp.id == 13:
                #s1h1in
                for i in dictionary['s13h1in']:
                        from_port_to_port(3,1,i)
                        from_port_to_port(4,1,i)
                for i in dictionary['s13h2in']:
                        from_port_to_port(3,2,i)
                        from_port_to_port(4,2,i)
                print "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%s13h1out",dictionary['s13h1out']
		for i in dictionary['s13h1out']:
                        from_port_to_port(1,3,i)
		print "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%s13h2out",dictionary['s13h2out']
                for i in dictionary['s13h2out']:
                        from_port_to_port(2,3,i)
                from_port_to_port(2,1,1413)
                from_port_to_port(1,2,1314)


	if dp.id==2:
                for i in dictionary['s2h1in']:
                        from_port_to_port(3,1,i)
			from_port_to_port(4,1,i)
                from_port_to_port(2,1,403)
                #s2h2in 
		for i in dictionary['s2h2in']:
                        from_port_to_port(3,2,i)
                        from_port_to_port(4,2,i)
                #s2h1out
		for i in dictionary['s2h1out']:
                        from_port_to_port(1,4,i)
                #s2h2out
                for i in dictionary['s2h2out']:
                        from_port_to_port(2,4,i)
		from_port_to_port(2,1,403)
                from_port_to_port(1,2,304)

	if dp.id==6:
                for i in dictionary['s6h1in']:
                        from_port_to_port(3,1,i)
			from_port_to_port(4,1,i)
                #s2h2in 
                for i in dictionary['s6h2in']:
                        from_port_to_port(3,2,i)
                        from_port_to_port(4,2,i)
                #s2h1out
                for i in dictionary['s6h1out']:
                        from_port_to_port(1,4,i)
                #s2h2out
                for i in dictionary['s6h2out']:
                        from_port_to_port(2,4,i)
                from_port_to_port(2,1,807)
                from_port_to_port(1,2,708)

        if dp.id==10:
                for i in dictionary['s10h1in']:
                        from_port_to_port(3,1,i)
			from_port_to_port(4,1,i)
                #s2h2in 
                for i in dictionary['s10h2in']:
                        from_port_to_port(3,2,i)
                        from_port_to_port(4,2,i)
                #s2h1out
                for i in dictionary['s10h1out']:
                        from_port_to_port(1,4,i)
                #s2h2out
                for i in dictionary['s10h2out']:
                        from_port_to_port(2,4,i)
                from_port_to_port(2,1,1211)
                from_port_to_port(1,2,1112)


        if dp.id==14:
                for i in dictionary['s14h1in']:
                        from_port_to_port(3,1,i)
			from_port_to_port(4,1,i)
                #s2h2in 
                for i in dictionary['s14h2in']:
                        from_port_to_port(3,2,i)
                        from_port_to_port(4,2,i)
                #s2h1out
                for i in dictionary['s14h1out']:
                        from_port_to_port(1,4,i)
                #s2h2out
                for i in dictionary['s14h2out']:
                        from_port_to_port(2,4,i)
                from_port_to_port(2,1,1615)
                from_port_to_port(1,2,1516)


	if dp.id==3:
		global pod11out
		for i in pod11out:
			from_port_to_port(1,3,i)
		global pod11in
		for i in pod11in:	
			from_port_to_port(3,1,i)
			from_port_to_port(4,1,i)
		global pod13in
		for i in pod13in:	
			from_port_to_port(3,2,i)
			from_port_to_port(4,2,i)
		
		global pod12out
		for i in pod12out:
			from_port_to_port(1,4,i)
		global pod12in
		for i in pod12in:
			from_port_to_port(4,1,i)
			from_port_to_port(3,1,i)
		global pod14in
		for i in pod14in:
			from_port_to_port(3,2,i)
			from_port_to_port(4,2,i)
		global ipod1
		for i in ipod1:
			from_port_to_port(1,2,i)

        if dp.id==7:

                global pod25out
                for i in pod25out:
                        from_port_to_port(1,3,i)
                global pod25in
		for i in pod25in:
			from_port_to_port(3,1,i)
			from_port_to_port(4,1,i)
		global pod27in
		for i in pod27in:	
			from_port_to_port(4,2,i)
			from_port_to_port(3,2,i)
                	
			

		global pod26out
                for i in pod26out:
                        from_port_to_port(1,4,i)
                global pod26in
		for i in pod26in:
			 from_port_to_port(4,1,i)
                         from_port_to_port(3,1,i)
                for i in pod28in:
		         from_port_to_port(3,2,i)
                         from_port_to_port(4,2,i)

		


		global ipod2
                for i in ipod2:
                        from_port_to_port(1,2,i)
        if dp.id==11:
                global pod39out
                for i in pod39out:
                        from_port_to_port(1,3,i)
                global pod39in
		for i in pod39in:        
			from_port_to_port(3,1,i)
			from_port_to_port(4,1,i)
		global pod311in
		for i in pod311in:
			from_port_to_port(3,2,i)
			from_port_to_port(4,2,i)
                global pod310out
                for i in pod310out:
                        from_port_to_port(1,4,i)
                global pod310in
		for i in pod310in:
			from_port_to_port(4,1,i)
			from_port_to_port(3,1,i)
		global pod312in
		for i in pod312in:
			from_port_to_port(3,2,i)
			from_port_to_port(4,2,i)
                global ipod3
                for i in ipod3:
                        from_port_to_port(1,2,i)


        if dp.id==15:
                global pod413out
                for i in pod413out:
                        from_port_to_port(1,3,i)
                global pod413in
                for i in pod413in:
                        from_port_to_port(3,1,i)
                        from_port_to_port(4,1,i)
                global pod415in
                for i in pod415in:
                        from_port_to_port(3,2,i)
                        from_port_to_port(4,2,i)
                global pod414out
                for i in pod414out:
                        from_port_to_port(1,4,i)
                global pod414in
                for i in pod414in:
                        from_port_to_port(4,1,i)
                        from_port_to_port(3,1,i)
                global pod416in
                for i in pod416in:
                        from_port_to_port(3,2,i)
                        from_port_to_port(4,2,i)
                global ipod4
                for i in ipod4:
                        from_port_to_port(1,2,i)




	if dp.id==4:
		global pod13out
		print 'pod13out',pod13out
		for i in pod13out:
			from_port_to_port(2,3,i)

		global pod13in
		for i in pod13in:
			from_port_to_port(3,2,i)
			from_port_to_port(4,2,i)
		global pod11in
		for i in pod11in:
			from_port_to_port(4,1,i)
			from_port_to_port(3,1,i)
			
		global pod14out
		for i in pod14out:
			from_port_to_port(2,4,i)
		global pod14in
		for i in pod14in:	
			from_port_to_port(4,2,i)
			from_port_to_port(3,2,i)
		global pod12in
		for i in pod12in:
			from_port_to_port(3,1,i)
			from_port_to_port(4,1,i)
		global ipod1
		for i in ipod1:
			from_port_to_port(2,1,i)



        if dp.id==8:
                global pod27out
                for i in pod27out:
                        from_port_to_port(2,3,i)
		global pod27in
		for i in pod27in:
                        from_port_to_port(3,2,i)
                        from_port_to_port(4,2,i)
                global pod25in
		for i in pod25in:
			from_port_to_port(4,1,i)
                        from_port_to_port(3,1,i)
                global pod28out
                for i in pod28out:
                        from_port_to_port(2,4,i)
                global pod28in
		for i in pod28in:        
			from_port_to_port(4,2,i)
			from_port_to_port(3,2,i)
		global pod26in
		for i in pod26in:
			from_port_to_port(3,1,i)
			from_port_to_port(4,1,i)
                global ipod2
                for i in ipod2:
                        from_port_to_port(2,1,i)
        if dp.id==12:
                global pod311out
                for i in pod311out:
                        from_port_to_port(2,3,i)
                global pod311in
		for i in pod311in:        
			from_port_to_port(3,2,i)
			from_port_to_port(4,2,i)
		global pod39in
		for i in pod39in:
			from_port_to_port(4,1,i)
			from_port_to_port(3,1,i)
                global pod312out
                for i in pod312out:
                        from_port_to_port(2,4,i)
                global pod312in
		for i in pod312in:        
			from_port_to_port(4,2,i)
			from_port_to_port(3,2,i)
		global pod310in	
		for i in pod310in:
			from_port_to_port(3,1,i)
			from_port_to_port(4,1,i)
                global ipod3
                for i in ipod3:
                        from_port_to_port(2,1,i)



	if dp.id==16:
                global pod415out
                for i in pod415out:
                        from_port_to_port(2,3,i)
                global pod415in
                for i in pod415in:
                        from_port_to_port(3,2,i)
                        from_port_to_port(4,2,i)
                global pod413in
                for i in pod413in:
                        from_port_to_port(4,1,i)
                        from_port_to_port(3,1,i)
                global pod416out
                for i in pod416out:
                        from_port_to_port(2,4,i)
                global pod416in
                for i in pod416in:
                        from_port_to_port(4,2,i)
                        from_port_to_port(3,2,i)
                global pod414in
                for i in pod414in:
                        from_port_to_port(3,1,i)
                        from_port_to_port(4,1,i)
                global ipod4
                for i in ipod4:
                        from_port_to_port(2,1,i)






	#CORE BITCHES
	if dp.id==17:
		global pod11out
		pod11out.sort()
		for i in range(0,4):
			
			from_port_to_port(1,2,pod11out[i])
			from_port_to_port(1,3,pod11out[i+4])
			from_port_to_port(1,4,pod11out[i+8])
		
		global pod25out
		pod25out.sort()
		for i in range(0,4):
			from_port_to_port(2,1,pod25out[i])
			from_port_to_port(2,3,pod25out[i+4])
			from_port_to_port(2,4,pod25out[i+8])
		global pod39out
		pod39out.sort()
                for i in range(0,4):
                        from_port_to_port(3,1,pod39out[i])
                        from_port_to_port(3,2,pod39out[i+4])
                        from_port_to_port(3,4,pod39out[i+8])
		global pod413out
		pod413out.sort()
		
                for i in range(0,4):
                        from_port_to_port(4,1,pod413out[i])
                        from_port_to_port(4,2,pod413out[i+4])
                        from_port_to_port(4,3,pod413out[i+8])

        if dp.id==18:
                global pod12out
                pod11out.sort()
                for i in range(0,4):
                        from_port_to_port(1,2,pod12out[i])
                        from_port_to_port(1,3,pod12out[i+4])
                        from_port_to_port(1,4,pod12out[i+8])

                global pod26out
                pod25out.sort()
                for i in range(0,4):
                        from_port_to_port(2,1,pod26out[i])
                        from_port_to_port(2,3,pod26out[i+4])
                        from_port_to_port(2,4,pod26out[i+8])
                global pod310out
                pod310out.sort()
                for i in range(0,4):
                        from_port_to_port(3,1,pod310out[i])
                        from_port_to_port(3,2,pod310out[i+4])
                        from_port_to_port(3,4,pod310out[i+8])
                global pod414out
                pod414out.sort()
                for i in range(0,4):
                        from_port_to_port(4,1,pod414out[i])
                        from_port_to_port(4,2,pod414out[i+4])
                        from_port_to_port(4,3,pod414out[i+8])

        if dp.id==19:
                global pod13out
                pod13out.sort()
                for i in range(0,4):
                        from_port_to_port(1,2,pod13out[i])
                        from_port_to_port(1,3,pod13out[i+4])
                        from_port_to_port(1,4,pod13out[i+8])

                global pod27out
		
                pod27out.sort()
                print 'pod13out',pod13out
		for i in range(0,4):
                        from_port_to_port(2,1,pod27out[i])
                        from_port_to_port(2,3,pod27out[i+4])
                        from_port_to_port(2,4,pod27out[i+8])
                global pod311out
                pod311out.sort()
                for i in range(0,4):
                        from_port_to_port(3,1,pod311out[i])
                        from_port_to_port(3,2,pod311out[i+4])
                        from_port_to_port(3,4,pod311out[i+8])
                global pod415out
                pod415out.sort()
                for i in range(0,4):
                        from_port_to_port(4,1,pod415out[i])
                        from_port_to_port(4,2,pod415out[i+4])
                        from_port_to_port(4,3,pod415out[i+8])

        if dp.id==20:
                global pod14out
                pod14out.sort()
		print 'pod14out',pod14out
                for i in range(0,4):
                        from_port_to_port(1,2,pod14out[i])
                        from_port_to_port(1,3,pod14out[i+4])
                        from_port_to_port(1,4,pod14out[i+8])

                global pod28out
                pod28out.sort()
                for i in range(0,4):
                        from_port_to_port(2,1,pod28out[i])
                        from_port_to_port(2,3,pod28out[i+4])
                        from_port_to_port(2,4,pod28out[i+8])
                global pod312out
                pod312out.sort()
                for i in range(0,4):
                        from_port_to_port(3,1,pod312out[i])
                        from_port_to_port(3,2,pod312out[i+4])
                        from_port_to_port(3,4,pod312out[i+8])
                global pod416out
                pod416out.sort()
                for i in range(0,4):
                        from_port_to_port(4,1,pod416out[i])
                        from_port_to_port(4,2,pod416out[i+4])
                        from_port_to_port(4,3,pod416out[i+8])

