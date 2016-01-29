1) Some part of the code were used from online sources. Rest all were coded from scratch.
	- Creation of raw socket:
		 http://www.kanadas.com/program-e/2012/05/a_test_program_for_sendingrece.html
	- Creation of IP header, UDP header and calculating checksum
		https://austinmarton.wordpress.com/2011/09/14/sending-raw-ethernet-packets-from-a-specific-interface-in-c-on-linux/
	
2) FastPass agent:
   Create a UDP socket between Fastpass agent and arbiter. Arbiter listening on 20.0.0.100:5000
   Read the traffic file hXX.tr where XX stands for host number and parse the contents of the file. 
   For each line in the file extract the destination host, destination port number and file size to send. 
   Convert the file size into long long int Ex: 50M into 50000000.
   Decide the size of each packet data. I have considered 1000bytes of data per packet. 
   Determine number of packets to be sent by dividing the total size/size per packet.  Ex: 50000000/1000 = 50000 packets per flow
   Consider one vlan for every 500 packets. So make 50000/500 number of demand requests to the arbiter.
   Construct the demand request and send it to the arbiter. This sendto is happening on the UDP socket created between fastpass and arbiter.
   This does not involve any hosts in the topology.
   For every response received from the arbiter start sending 500 packets in the assigned vlan and then continue the same.
   
   Sending Packets:
		- Open a raw socket. 
		- create a ethernet packet, VlanTag
		- Add IP header, UDP header
		- send the packet over the raw socket created to host 16
   
3) Arbiter
	Listening on port 5000 at 20.0.0.100 ip address.
	UDP socket is used to communicate with the fastpass agent
	Arbiter receives vlan request from the FastPass agent. Arbiter will distribute the load on all of the vlans by using round robin logic.
	The request message will have source host and destination host. 
	Arbiter uses strawmans approach and calculates vlandid. 
	The vlans are tracked in a 2D array where if the value indexed by vlanid is 1 then next path is taken.
	If all the vlans indexes are 1 then reset it to 0 and allocate the vlans again in round robin fashion.
	once a vland id is available then send it to the fastpass agent.
    
Parameter settings:
    - Request to the arbiter will be of the form "XXYY" where XX stand for source host number and YY stand for destination host number
	- Vland ids are calculated like below:
		vlanid1 = src<<4 + dest;
		vlanid2 = vland1 +272;
		vlanid3 = vlanid2 +272;
		vlanid4 = vlanid3 +272;
	
	- Fastpass: The parameters parsed are stored in separate variables. The following information is stored:
		Source host
		Destination host
		Destination port
		Message length
		Source IP address
		Destination IP address
		vlan id assigned for that particular packet.
		
	



Makefile can be found in the repository with the same name. This makefile will create the binaries arbiter and cperf for arbiter.c and client.c respectively
   For the makefile to work correctly the file Ether.h should be in the same folder where arbiter.c and client.c are present
NOTE: before using "make" command, run "make clean"	so that any existing binaries will be removed.
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Commands used:
1) to delete binaries
cmd:	make clean
2) to build binaries arbiter and cperf
cmd:	make
3) To run the controller
cmd:	sudo ryu-manager source_routing.py
4) To create the mininet
cmd: sudo python arbiter_network.py --custom=fat.py --topo=fattopo
5) To run the program
cmd: sudo python evaluation.py
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
How to run:
1) open a terminal and run command 3
2) open second terminal and run command 4
3) open third terminal and run command 1 followed by command 20
4) run command 5
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
PLEASE NOTE: IMPORTANT
My virtual machine has some problem in sending packets on eth0. I have done my projectA on eth1 itself.
Please change the one line in evaluation.py file which has eth0 to eth1
Existing line in evaluation.py:
Line 312: cmd = '~/mininet/util/m ' + host + ' sudo tcpdump -i ' + host +'-eth0' + ' -n -s 64 -B 8192 -w dump/' + host + '.pcap >/dev/null 2>&1 &'

Modified line:
Line 312: cmd = '~/mininet/util/m ' + host + ' sudo tcpdump -i ' + host +'-eth1' + ' -n -s 64 -B 8192 -w dump/' + host + '.pcap >/dev/null 2>&1 &'
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++                


