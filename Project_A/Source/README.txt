README:

NOTE: PLEASE OPEN README IN NOTEPAD++ OR SUBLIME EDITOR. THE TOPOLOGY DIAGRAM WILL BE DISTORTED OTHERWISE.

a) I have 240 VLAN Ids in entire network. With the type of implementation I have considered using Strawman's a pproach I need 240 VLAN's as the minimum VLAN ids.
   Reason: I have made the switches as dumb as possible with not much processing power which is one of the key ideas of Ethane. The routing logic implemented 
   is hard coded only for intra pod communication. The packets are sent to core switches only if the destination is in different pod.
   At the core switches, controller will extract the destination host number from the vlanid and based on the destination host number the packet will be routed to
   corresponding pod only. 
   Ex: host h1 is in pod1 and host h5 is in pod2. The packet will be forwarded to core switch from pod1 and that core switch will check and learn that the host 
   h5 is in pod2 and will forward the packet to only pod2. Inside pods also the packet is forwarded downwards by checking where the host belongs and every time 
   this check is done by extracting the destination host number from the vlan id. 
   I have used strawman's approach to generate VLAN ids. And at the switches I extract the destination host number by (vlanId&15) and hosts have names from h1
   to h16. The above logic of getting destination number wont work when host is h16 so for this case I make a check for the possible vlan ids that involve h16
   as the destination. Since the destination host number is embedded in the vlan id I have used 240 identical VLAN ids.
   
b) FIB table

*** s1 ------------------------------------------------------------------------
NXST_FLOW reply (xid=0x4):
 cookie=0x0, duration=11.379s, table=0, n_packets=0, n_bytes=0, idle_age=11, in_port=4,dl_vlan=245 actions=output:1
 cookie=0x0, duration=11.437s, table=0, n_packets=0, n_bytes=0, idle_age=11, in_port=3,dl_vlan=193 actions=output:1
 cookie=0x0, duration=11.34s, table=0, n_packets=0, n_bytes=0, idle_age=11, in_port=2,dl_vlan=244 actions=output:3
 cookie=0x0, duration=11.34s, table=0, n_packets=0, n_bytes=0, idle_age=11, in_port=2,dl_vlan=242 actions=output:4
 cookie=0x0, duration=11.97s, table=0, n_packets=1, n_bytes=38, idle_age=8, in_port=3,dl_vlan=49 actions=output:4
 
*** s2 ------------------------------------------------------------------------
NXST_FLOW reply (xid=0x4):
 cookie=0x0, duration=11.357s, table=0, n_packets=0, n_bytes=0, idle_age=11, in_port=4,dl_vlan=20 actions=output:3
 cookie=0x0, duration=11.322s, table=0, n_packets=0, n_bytes=0, idle_age=11, in_port=2,dl_vlan=260 actions=output:3
 cookie=0x0, duration=11.322s, table=0, n_packets=0, n_bytes=0, idle_age=11, in_port=1,dl_vlan=226 actions=output:4
 cookie=0x0, duration=11.322s, table=0, n_packets=0, n_bytes=0, idle_age=11, in_port=2,dl_vlan=242 actions=output:4
 cookie=0x0, duration=11.357s, table=0, n_packets=0, n_bytes=0, idle_age=11, in_port=1,dl_vlan=116 actions=output:3

*** s3 ------------------------------------------------------------------------
NXST_FLOW reply (xid=0x4):
 cookie=0x0, duration=11.107s, table=0, n_packets=0, n_bytes=0, idle_age=11, in_port=4,dl_vlan=245 actions=output:1
 cookie=0x0, duration=11.139s, table=0, n_packets=0, n_bytes=0, idle_age=11, in_port=3,dl_vlan=193 actions=output:1
 cookie=0x0, duration=11.052s, table=0, n_packets=0, n_bytes=0, idle_age=11, in_port=2,dl_vlan=244 actions=output:3
 cookie=0x0, duration=11.052s, table=0, n_packets=0, n_bytes=0, idle_age=11, in_port=2,dl_vlan=195 actions=output:4
 cookie=0x0, duration=11.052s, table=0, n_packets=0, n_bytes=0, idle_age=11, in_port=1,dl_vlan=195 actions=output:4
 cookie=0x0, duration=10.691s, table=0, n_packets=0, n_bytes=0, idle_age=10, in_port=1,dl_vlan=196 actions=output:3
 
*** s4 ------------------------------------------------------------------------
NXST_FLOW reply (xid=0x4):
 cookie=0x0, duration=10.798s, table=0, n_packets=0, n_bytes=0, idle_age=10, in_port=4,dl_vlan=245 actions=output:1
 cookie=0x0, duration=10.846s, table=0, n_packets=0, n_bytes=0, idle_age=10, in_port=3,dl_vlan=193 actions=output:1
 cookie=0x0, duration=10.75s, table=0, n_packets=0, n_bytes=0, idle_age=10, in_port=2,dl_vlan=242 actions=output:3
 cookie=0x0, duration=10.715s, table=0, n_packets=0, n_bytes=0, idle_age=10, in_port=3,dl_vlan=35 actions=output:2
 cookie=0x0, duration=10.671s, table=0, n_packets=0, n_bytes=0, idle_age=10, in_port=1,dl_vlan=129 actions=output:4
 cookie=0x0, duration=10.671s, table=0, n_packets=0, n_bytes=0, idle_age=10, in_port=1,dl_vlan=114 actions=output:3
 cookie=0x0, duration=10.671s, table=0, n_packets=0, n_bytes=0, idle_age=10, in_port=2,dl_vlan=81 actions=output:4
 cookie=0x0, duration=10.715s, table=0, n_packets=0, n_bytes=0, idle_age=10, in_port=4,dl_vlan=20 actions=output:2
 
*** s5 ------------------------------------------------------------------------
NXST_FLOW reply (xid=0x4):
 cookie=0x0, duration=10.556s, table=0, n_packets=0, n_bytes=0, idle_age=10, in_port=4,dl_vlan=245 actions=output:2
 cookie=0x0, duration=10.604s, table=0, n_packets=0, n_bytes=0, idle_age=10, in_port=3,dl_vlan=193 actions=output:2
 cookie=0x0, duration=10.517s, table=0, n_packets=0, n_bytes=0, idle_age=10, in_port=1,dl_vlan=166 actions=output:4
 cookie=0x0, duration=10.895s, table=0, n_packets=0, n_bytes=0, idle_age=10, in_port=1,dl_vlan=248 actions=output:3
 cookie=0x0, duration=19.212s, table=0, n_packets=1, n_bytes=38, idle_age=2, in_port=3,dl_vlan=117 actions=output:4
  
*** s6 ------------------------------------------------------------------------
NXST_FLOW reply (xid=0x4):
 cookie=0x0, duration=9.291s, table=0, n_packets=0, n_bytes=0, idle_age=9, in_port=2,dl_vlan=53 actions=output:4
 cookie=0x0, duration=9.291s, table=0, n_packets=0, n_bytes=0, idle_age=9, in_port=2,dl_vlan=39 actions=output:3
 cookie=0x0, duration=9.255s, table=0, n_packets=0, n_bytes=0, idle_age=9, in_port=1,dl_vlan=264 actions=output:3
 cookie=0x0, duration=9.279s, table=0, n_packets=0, n_bytes=0, idle_age=9, in_port=1,dl_vlan=69 actions=output:4
 cookie=0x0, duration=9.291s, table=0, n_packets=0, n_bytes=0, idle_age=9, in_port=4,dl_vlan=103 actions=output:3
 
*** s7 ------------------------------------------------------------------------
NXST_FLOW reply (xid=0x4):
 cookie=0x0, duration=9.349s, table=0, n_packets=0, n_bytes=0, idle_age=9, in_port=4,dl_vlan=245 actions=output:1
 cookie=0x0, duration=9.359s, table=0, n_packets=0, n_bytes=0, idle_age=9, in_port=3,dl_vlan=193 actions=output:1
 cookie=0x0, duration=9.436s, table=0, n_packets=0, n_bytes=0, idle_age=9, in_port=2,dl_vlan=104 actions=output:3
 cookie=0x0, duration=9.443s, table=0, n_packets=0, n_bytes=0, idle_age=9, in_port=4,dl_vlan=120 actions=output:3
 cookie=0x0, duration=9.341s, table=0, n_packets=0, n_bytes=0, idle_age=9, in_port=2,dl_vlan=263 actions=output:4
 cookie=0x0, duration=9.341s, table=0, n_packets=0, n_bytes=0, idle_age=9, in_port=1,dl_vlan=248 actions=output:3
 cookie=0x0, duration=18.681s, table=0, n_packets=0, n_bytes=0, idle_age=18, in_port=1,dl_vlan=151 actions=output:4
 cookie=0x0, duration=359.756s, table=0, n_packets=1, n_bytes=38, idle_age=31, in_port=3,dl_vlan=135 actions=output:4
 
*** s8 ------------------------------------------------------------------------
NXST_FLOW reply (xid=0x4):
 cookie=0x0, duration=10.343s, table=0, n_packets=0, n_bytes=0, idle_age=10, in_port=2,dl_vlan=53 actions=output:4
 cookie=0x0, duration=10.365s, table=0, n_packets=0, n_bytes=0, idle_age=10, in_port=4,dl_vlan=245 actions=output:1
 cookie=0x0, duration=10.415s, table=0, n_packets=0, n_bytes=0, idle_age=10, in_port=3,dl_vlan=193 actions=output:1
 cookie=0x0, duration=10.343s, table=0, n_packets=0, n_bytes=0, idle_age=10, in_port=1,dl_vlan=166 actions=output:3
 cookie=0x0, duration=10.542s, table=0, n_packets=0, n_bytes=0, idle_age=10, in_port=3,dl_vlan=104 actions=output:2
 cookie=0x0, duration=10.343s, table=0, n_packets=0, n_bytes=0, idle_age=10, in_port=2,dl_vlan=166 actions=output:3
 cookie=0x0, duration=359.49s, table=0, n_packets=1, n_bytes=38, idle_age=343, in_port=1,dl_vlan=117 actions=output:4
 cookie=0x0, duration=359.49s, table=0, n_packets=1, n_bytes=38, idle_age=2, in_port=3,dl_vlan=101 actions=output:4
 cookie=0x0, duration=359.492s, table=0, n_packets=1, n_bytes=38, idle_age=15, in_port=4,dl_vlan=86 actions=output:3
  
*** s9 ------------------------------------------------------------------------
NXST_FLOW reply (xid=0x4):
 cookie=0x0, duration=9.969s, table=0, n_packets=0, n_bytes=0, idle_age=9, in_port=2,dl_vlan=234 actions=output:4
 cookie=0x0, duration=10.027s, table=0, n_packets=0, n_bytes=0, idle_age=10, in_port=1,dl_vlan=57 actions=output:4
 cookie=0x0, duration=10.027s, table=0, n_packets=0, n_bytes=0, idle_age=10, in_port=2,dl_vlan=43 actions=output:3
 cookie=0x0, duration=10.027s, table=0, n_packets=0, n_bytes=0, idle_age=10, in_port=3,dl_vlan=202 actions=output:4
 cookie=0x0, duration=9.976s, table=0, n_packets=0, n_bytes=0, idle_age=9, in_port=1,dl_vlan=108 actions=output:3
 
*** s10 ------------------------------------------------------------------------
NXST_FLOW reply (xid=0x4):
 cookie=0x0, duration=10.048s, table=0, n_packets=0, n_bytes=0, idle_age=10, in_port=4,dl_vlan=245 actions=output:1
 cookie=0x0, duration=10.126s, table=0, n_packets=0, n_bytes=0, idle_age=10, in_port=3,dl_vlan=193 actions=output:1
 cookie=0x0, duration=10.037s, table=0, n_packets=0, n_bytes=0, idle_age=10, in_port=2,dl_vlan=92 actions=output:3
 cookie=0x0, duration=10.037s, table=0, n_packets=0, n_bytes=0, idle_age=10, in_port=2,dl_vlan=220 actions=output:3
 cookie=0x0, duration=704.916s, table=0, n_packets=1, n_bytes=38, idle_age=1, in_port=4,dl_vlan=155 actions=output:3
  
*** s11 ------------------------------------------------------------------------
NXST_FLOW reply (xid=0x4):
 cookie=0x0, duration=9.717s, table=0, n_packets=0, n_bytes=0, idle_age=9, in_port=4,dl_vlan=245 actions=output:2
 cookie=0x0, duration=9.789s, table=0, n_packets=0, n_bytes=0, idle_age=9, in_port=3,dl_vlan=193 actions=output:2
 cookie=0x0, duration=9.712s, table=0, n_packets=0, n_bytes=0, idle_age=9, in_port=1,dl_vlan=251 actions=output:4
 cookie=0x0, duration=9.712s, table=0, n_packets=0, n_bytes=0, idle_age=9, in_port=1,dl_vlan=60 actions=output:3
 cookie=0x0, duration=9.712s, table=0, n_packets=0, n_bytes=0, idle_age=9, in_port=2,dl_vlan=92 actions=output:3
 cookie=0x0, duration=703.869s, table=0, n_packets=1, n_bytes=38, idle_age=1, in_port=2,dl_vlan=155 actions=output:4
 cookie=0x0, duration=89.825s, table=0, n_packets=1, n_bytes=38, idle_age=49, in_port=4,dl_vlan=188 actions=output:3
 cookie=0x0, duration=89.825s, table=0, n_packets=1, n_bytes=38, idle_age=66, in_port=3,dl_vlan=203 actions=output:4
  
*** s12 ------------------------------------------------------------------------
NXST_FLOW reply (xid=0x4):
 cookie=0x0, duration=9.631s, table=0, n_packets=0, n_bytes=0, idle_age=9, in_port=4,dl_vlan=245 actions=output:2
 cookie=0x0, duration=9.638s, table=0, n_packets=0, n_bytes=0, idle_age=9, in_port=3,dl_vlan=193 actions=output:2
 cookie=0x0, duration=9.628s, table=0, n_packets=0, n_bytes=0, idle_age=9, in_port=1,dl_vlan=57 actions=output:4
 cookie=0x0, duration=90.742s, table=0, n_packets=1, n_bytes=38, idle_age=22, in_port=4,dl_vlan=154 actions=output:3
 cookie=0x0, duration=90.742s, table=0, n_packets=1, n_bytes=38, idle_age=8, in_port=3,dl_vlan=169 actions=output:4
 cookie=0x0, duration=90.612s, table=0, n_packets=0, n_bytes=0, idle_age=90, in_port=1,dl_vlan=122 actions=output:3
 cookie=0x0, duration=90.612s, table=0, n_packets=0, n_bytes=0, idle_age=90, in_port=2,dl_vlan=106 actions=output:3
 cookie=0x0, duration=90.619s, table=0, n_packets=0, n_bytes=0, idle_age=90, in_port=2,dl_vlan=89 actions=output:4
 
*** s13 ------------------------------------------------------------------------
NXST_FLOW reply (xid=0x4):
 cookie=0x0, duration=9.304s, table=0, n_packets=0, n_bytes=0, idle_age=9, in_port=2,dl_vlan=157 actions=output:4
 cookie=0x0, duration=9.305s, table=0, n_packets=0, n_bytes=0, idle_age=9, in_port=1,dl_vlan=96 actions=output:3
 cookie=0x0, duration=9.304s, table=0, n_packets=0, n_bytes=0, idle_age=9, in_port=1,dl_vlan=174 actions=output:4
 cookie=0x0, duration=9.313s, table=0, n_packets=0, n_bytes=0, idle_age=9, in_port=3,dl_vlan=254 actions=output:4
 cookie=0x0, duration=9.305s, table=0, n_packets=0, n_bytes=0, idle_age=9, in_port=2,dl_vlan=112 actions=output:3
 
*** s14 ------------------------------------------------------------------------
NXST_FLOW reply (xid=0x4):
 cookie=0x0, duration=9.401s, table=0, n_packets=0, n_bytes=0, idle_age=9, in_port=4,dl_vlan=245 actions=output:2
 cookie=0x0, duration=9.402s, table=0, n_packets=0, n_bytes=0, idle_age=9, in_port=3,dl_vlan=193 actions=output:2
 cookie=0x0, duration=90.47s, table=0, n_packets=0, n_bytes=0, idle_age=90, in_port=1,dl_vlan=48 actions=output:3
 cookie=0x0, duration=90.47s, table=0, n_packets=0, n_bytes=0, idle_age=90, in_port=1,dl_vlan=109 actions=output:4
 cookie=0x0, duration=478.638s, table=0, n_packets=1, n_bytes=38, idle_age=2, in_port=4,dl_vlan=223 actions=output:3
 
*** s15 ------------------------------------------------------------------------
NXST_FLOW reply (xid=0x4):
 cookie=0x0, duration=9.266s, table=0, n_packets=0, n_bytes=0, idle_age=9, in_port=4,dl_vlan=245 actions=output:2
 cookie=0x0, duration=9.278s, table=0, n_packets=0, n_bytes=0, idle_age=9, in_port=3,dl_vlan=193 actions=output:2
 cookie=0x0, duration=9.219s, table=0, n_packets=0, n_bytes=0, idle_age=9, in_port=2,dl_vlan=111 actions=output:4
 cookie=0x0, duration=9.224s, table=0, n_packets=0, n_bytes=0, idle_age=9, in_port=1,dl_vlan=48 actions=output:3
 cookie=0x0, duration=650.692s, table=0, n_packets=1, n_bytes=38, idle_age=28, in_port=3,dl_vlan=271 actions=output:4
 cookie=0x0, duration=650.698s, table=0, n_packets=1, n_bytes=38, idle_age=41, in_port=4,dl_vlan=256 actions=output:3
 cookie=0x0, duration=650.579s, table=0, n_packets=0, n_bytes=0, idle_age=650, in_port=1,dl_vlan=207 actions=output:4
 cookie=0x0, duration=650.692s, table=0, n_packets=0, n_bytes=0, idle_age=650, in_port=2,dl_vlan=240 actions=output:3
  
*** s16 ------------------------------------------------------------------------
NXST_FLOW reply (xid=0x4):
 cookie=0x0, duration=9.16s, table=0, n_packets=0, n_bytes=0, idle_age=9, in_port=4,dl_vlan=245 actions=output:2
 cookie=0x0, duration=9.161s, table=0, n_packets=0, n_bytes=0, idle_age=9, in_port=3,dl_vlan=193 actions=output:2
 cookie=0x0, duration=9.121s, table=0, n_packets=0, n_bytes=0, idle_age=9, in_port=2,dl_vlan=46 actions=output:3
 cookie=0x0, duration=9.121s, table=0, n_packets=0, n_bytes=0, idle_age=9, in_port=2,dl_vlan=45 actions=output:4
 cookie=0x0, duration=9.111s, table=0, n_packets=0, n_bytes=0, idle_age=9, in_port=1,dl_vlan=109 actions=output:4
 cookie=0x0, duration=650.593s, table=0, n_packets=1, n_bytes=38, idle_age=3, in_port=3,dl_vlan=237 actions=output:4
 cookie=0x0, duration=650.589s, table=0, n_packets=1, n_bytes=38, idle_age=174, in_port=4,dl_vlan=223 actions=output:2
 cookie=0x0, duration=650.465s, table=0, n_packets=0, n_bytes=0, idle_age=650, in_port=1,dl_vlan=30 actions=output:3
 
*** s17 ------------------------------------------------------------------------
NXST_FLOW reply (xid=0x4):
 cookie=0x0, duration=8.995s, table=0, n_packets=0, n_bytes=0, idle_age=8, in_port=1,dl_vlan=264 actions=output:2
 cookie=0x0, duration=9.01s, table=0, n_packets=0, n_bytes=0, idle_age=9, in_port=1,dl_vlan=57 actions=output:3
 cookie=0x0, duration=8.995s, table=0, n_packets=0, n_bytes=0, idle_age=8, in_port=1,dl_vlan=190 actions=output:4
 
*** s18 ------------------------------------------------------------------------
NXST_FLOW reply (xid=0x4):
 cookie=0x0, duration=8.119s, table=0, n_packets=0, n_bytes=0, idle_age=8, in_port=2,dl_vlan=157 actions=output:4
 cookie=0x0, duration=8.115s, table=0, n_packets=0, n_bytes=0, idle_age=8, in_port=2,dl_vlan=234 actions=output:3
 cookie=0x0, duration=8.111s, table=0, n_packets=0, n_bytes=0, idle_age=8, in_port=2,dl_vlan=260 actions=output:1

*** s19 ------------------------------------------------------------------------
NXST_FLOW reply (xid=0x4):
 cookie=0x0, duration=8.127s, table=0, n_packets=0, n_bytes=0, idle_age=8, in_port=3,dl_vlan=110 actions=output:4
 cookie=0x0, duration=8.122s, table=0, n_packets=0, n_bytes=0, idle_age=8, in_port=3,dl_vlan=193 actions=output:1
 cookie=0x0, duration=8.119s, table=0, n_packets=0, n_bytes=0, idle_age=8, in_port=3,dl_vlan=230 actions=output:2
 
*** s20 ------------------------------------------------------------------------
NXST_FLOW reply (xid=0x4):
 cookie=0x0, duration=9.055s, table=0, n_packets=0, n_bytes=0, idle_age=9, in_port=4,dl_vlan=24 actions=output:2
 cookie=0x0, duration=9.055s, table=0, n_packets=0, n_bytes=0, idle_age=9, in_port=4,dl_vlan=41 actions=output:3
 cookie=0x0, duration=9.043s, table=0, n_packets=0, n_bytes=0, idle_age=9, in_port=4,dl_vlan=180 actions=output:1

Routing:

Core Switches are S17, S18, S19 and S20.
S17: This switch receives all the traffic on port 1 only and from pod 1 only. When packets are received on port 1, based on which pod the destination host belongs
     the packet will be forwarded to either pod2, pod3 or pod4 on ports 2,3 and 4 respectively.
S18: This switch receives all the traffic on port 2 only and from pod 2 only. When packets are received on port 2, based on which pod the destination host belongs
     the packet will be forwarded to either pod1, pod3 or pod4 on ports 1,3 and 4 respectively.
S19: This switch receives all the traffic on port 3 only and from pod 3 only. When packets are received on port 3, based on which pod the destination host belongs
     the packet will be forwarded to either pod1, pod2 or pod4 on ports 1,2 and 4 respectively.	 
S20: This switch receives all the traffic on port 4 only and from pod 4 only. When packets are received on port 4, based on which pod the destination host belongs
     the packet will be forwarded to either pod1, pod2 or pod3 on ports 1,2 and 3 respectively. 

NOTE: For each of the core switches, no packets are forwarded to the port on which it receives the packets. Ex S17 receives on port 1 so no forwarding will be done
     on port 1	 
	 
Aggregator Switches:
These are the switches which are connected to core switches and TOR switches: 
	S1 and S2 in pod1
		S1,S2: connected to S4, S3
	S5 and S6 in pod2 
		S5,S6: connected to S8, S7
	S9 and S10 in pod3
		S9,S10: connected to S12, S11
	S13 and S14 in pod4
		S13,S14: connected to S16, S15

S1: This switch is connected to core switch S17 on port 1, core switch S18 on port 2. Also connected to TOR switches S4 and S3 on port 4 and 3 respectively.
	This switch receives packets on port 2,3 and 4 and the switch will decide if the destination is in the same pod or its in different pod. if its in different
	pod then it will forward the packets to core switch S17 on port 1. if its in same pod then it forwards the packet to port 4 or 3.

S2: This switch is connected to core switch S19 on port 1, core switch S20 on port 2. Also connected to TOR switches S4 and S3 on port 4 and 3 respectively.
	This switch receives packets on port 4,1 and 2 only. the switch will forward the received packets to S4 and S3 based on where the destination host reside 
	on ports 4 and 3 respectively.

S5: This switch is connected to core switch S17 on port 1, core switch S18 on port 2. Also connected to TOR switches S8 and S7 on port 4 and 3 respectively.
	This switch receives packets on port 1,4 and 3 and the switch will decide if the destination is in the same pod or its in different pod. if its in different
	pod then it will forward the packets to core switch S18 on port 2. if its in same pod then it forwards the packet to port 4 or 3.

S6: This switch is connected to core switch S19 on port 1, core switch S20 on port 2. Also connected to TOR switches S8 and S7 on port 4 and 3 respectively.
	This switch receives packets on port 4,1 and 2 only. the switch will forward the received packets to S8 and S7 based on where the destination host reside
	on ports 4 and 3 respectively.

S9: This switch is connected to core switch S17 on port 1, core switch S18 on port 2. Also connected to TOR switches S12 and S11 on port 4 and 3 respectively.
	This switch receives packets on port 1,2 and 3. for the packets received on port 1 and 2 the switch will decide if the destination is under switch S12 or S11
	and accordingly forward it to port 4 and 3 respectively. if the packet is received on port 3, it will forward it to port 4 only.

S10: This switch is connected to core switch S19 on port 1, core switch S20 on port 2. Also connected to TOR switches S12 and S11 on port 4 and 3 respectively.
	This switch receives packets on port 2,3 and 4 only. if the destination of the packet received is in different pod then s10 will forward the packet to the
	core switch S19 on port 1. if its in the same pod then based on whether the host is under S12 or S11 the switch will forward the packet on port 4 and 3 respectively.

S13: This switch is connected to core switch S17 on port 1, core switch S18 on port 2. Also connected to TOR switches S16 and S15 on port 4 and 3 respectively.
	This switch receives packets on port 1,2 and 3. for the packets received on port 1 and 2 the switch will decide if the destination is under switch S16 or S15
	and accordingly forward it to port 4 and 3 respectively. if the packet is received on port 3, it will forward it to port 4 only.

S14: This switch is connected to core switch S19 on port 1, core switch S20 on port 2. Also connected to TOR switches S16 and S15 on port 4 and 3 respectively.
	This switch receives packets on port 1,3 and 4 only. if the destination of the packet received is in different pod then s14 will forward the packet to the
	core switch S20 on port 2. if its in the same pod then based on whether the host is under S16 or S15 the switch will forward the packet on port 4 and 3 respectively.

NOTE: For every pod only one switch forwards the packets to core switches. S1->S17 on port 1, S5->S18 on port 2, S10->S19 on port 1, S14->S20 on port 2.0

TOR Switches:
These are the switches connected to Aggregator switches and hosts.
	S4 : connected to S1,S2,h1 and h2
	S3: connected to S1,S2, h3 and h4
	S8 : connected to S5,S6,h5 and h6
	S7: connected to S5,S6, h7 and h8
	S12 : connected to S9,S10,h9 and h10
	S11: connected to S9,S10, h11 and h12
	S16 : connected to S13,S14,h13 and h14
	S15: connected to S13,S14, h15 and h16

S4: This switch is connected to S1 on port1, S2 on port 2, h1 on port 4 and h2 on port 3. It receives packets on port 1,2,3,4 from S1, S2, h2, h1 respectively. If the destination
	host is not in the same pod then the switch forwards the packet to S1 on port 1 otherwise it will forward the packet to S2 on port 2. If packets are received on 
	port 1 or 2 then based on if the destination is h1 or h2 it will forward on port 4 or 3 respectively.

S3: This switch is connected to S1 on port1, S2 on port 2, h3 on port 4 and h4 on port 3. It receives packets on port 1,2,3,4 from S1, S2, h4, h3 respectively. If the destination
	host is not in the same pod or if the host is in S4 then the switch forwards the packet to S1 on port 1. If packets are received on	port 1 or 2 then based on 
	whether the destination is h4 or h3 it will forward on port 4 or 3 respectively.

S8: This switch is connected to S5 on port1, S6 on port 2, h5 on port 4 and h6 on port 3. It receives packets on port 1,2,3,4 from S5, S6, h6, h5 respectively. If the destination
	host is not in the same pod then the switch forwards the packet to S5 on port 1 otherwise it will forward the packet to S6 on port 2. If packets are received on 
	port 1 or 2 then based on if the destination is h5 or h6 it will forward on port 4 or 3 respectively.

S7: This switch is connected to S5 on port 1, S6 on port 2, h7 on port 4 and h8 on port 3. It receives packets on port 1,2,3,4 from S5, S6, h8, h7 respectively. If the destination
	host is not in the same pod or if the host is in S8 then the switch forwards the packet to S5 on port 1. If packets are received on	port 1 or 2 then based on 
	whether the destination is h7 or h8 it will forward on port 4 or 3 respectively.

S12: This switch is connected to S9 on port1, S10 on port 2, h9 on port 4 and h10 on port 3. It receives packets on port 1,2,3,4 from S9, S10, h9, h10 respectively. If the destination
	host is not in the same pod or if its in S11 then the switch forwards the packet to S10 on port 2. If packets are received on port 1 or 2 then based on if the destination is 
	h9 or h10 it will forward on port 4 or 3 respectively.

S11: This switch is connected to S9 on port 1, S10 on port 2, h11 on port 4 and h12 on port 3. It receives packets on port 1,2,3,4 from S9, S10, h12, h11 respectively. If the destination
	host is not in the same pod then the switch forwards the packet to S10 on port 2. if the destination host is in S12 then it forwards to S9 on port 1. If packets are received on port 1 or 2 then based on 
	whether the destination is h11 or h12 it will forward on port 4 or 3 respectively.	

S16: This switch is connected to S13 on port1, S14 on port 2, h13 on port 4 and h14 on port 3. It receives packets on port 1,2,3,4 from S13, S14, h14, h13 respectively. If the destination
	host is not in the same pod or if its in S15 then the switch forwards the packet to S14 on port 2. If packets are received on port 1 or 2 then based on if the destination is 
	h13 or h14 it will forward on port 4 or 3 respectively.

S15: This switch is connected to S3 on port 1, S14 on port 2, h15 on port 4 and h16 on port 3. It receives packets on port 1,2,3,4 from S13, S14, h16, h15 respectively. If the destination
	host is not in the same pod then the switch forwards the packet to S14 on port 2. if the destination host is in S16 then it forwards to S13 on port 1. If packets are received on port 1 or 2 then based on 
	whether the destination is h15 or h16 it will forward on port 4 or 3 respectively.	
	
				:1   :2
				|----|							|----|							|----|							|----|
				| 17 |							| 18 |							| 19 |							| 20 |
			  :4|----|:3						|----|							|----|							|----|
				/	\							/	\							/	\							/	\	
			  /		  \						  /		  \						  /		  \						  /		  \
		|----|			|----|			|----|			|----|			|----|			|----|	 		|----|			|----|
		| 1  |			| 2  |			| 5  |			| 6  |      	| 9  |			| 10 |      	| 13 |			| 14 |
		|----|			|----|			|----|			|----|      	|----|			|----|      	|----|			|----|
		  |	  \		   /   |			  |	  \		   /   |			  |	  \		   /   |	  		  |	  \		   /   |	
		  | 	 \ /	   |  			  | 	 \ /	   |   	 	  	  | 	 \ /	   | 			  | 	 \ /	   | 
		|----| /	 \	|----|			|----| /	 \	|----|			|----| /	 \	|----|			|----| /	 \	|----|
		| 4  |			| 3  |			| 8  |			| 7  |      	| 12 |			| 11 |      	| 16 |			| 15 |
		|----|			|----|			|----|			|----|      	|----|			|----|      	|----|			|----|
		/  \			/  \			/  \			 /  \			 /  \			 /  \			 /  \			 /  \
	   /	\			/	\		   /	\			/	\ 			/	\ 			/	\	  		/	\	 		/	\
	|----|	|----|	|----|	|----|	|----|	|----|	 |----|	|----|  |----| |----|	|----|	|----|	|----|	|----|	 |----|	|----|  
	| h1 |	| h2 |  | h3 |	| h4 |  | h5 |	| h6 |   | h7 |	| h8 |  | h9 | | h10|   | h11|	| h12|  | h13|	| h14|   | h15|	| h16|
	|----|	|----|	|----|	|----|  |----|	|----|   |----|	|----|  |----| |----|	|----|	|----|  |----|	|----|   |----|	|----|
			
NOTE: The ports are assigned as shown to switch S17. The pattern of port assignment is same for all the switches.


c)The general formula for Fat Tree Architecture is: 
  For 'k' ary fat tree number of hosts supported is (k^3)/4:
	In our case k=8. So it supports 128 hosts.
  
  Number of core switches is given by (k/2)^2: 
	In our case k=8, so it has 16 core switches
  
  Number of switches in each layer in each pod is given by k/2 switches	:
	In our case we have 2 layers and so we have 2*(8/2) = 8 switches. Like this we have 8 pods. So totalling 64 switches.
 
  In summary we have 128 hosts and 80 switches for k=8
  Number of VLAN IDs needed in the worst case will be 128*127 = 16256 ids
  Total number of shortest paths k*((k/2)^2) = 128 paths.
  
  
  COMMANDS USED:
  1) sudo mn --custom=fat.py --topo=fattopo --controller=remote
  2) ryu-manager source_routing.py
  3) for sending from h1 to h2: 
	 h1 python vlan.py -i h1-eth1 -d 10.0.0.2 -v 18