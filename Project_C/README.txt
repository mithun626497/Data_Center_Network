README

1) No new code has been used from any outside source. All modifications are done to the existing project B code on my own.
2) Changes made from Project B to Project C:
    -> Retransmission logic is added
	-> Since the bandwidth of the link is reduced and also the queue of the switches is reduced there were more packet drops
	-> Based on multiple run analysis and observing the pattern of the drops, suitable delay is added between every send of the packet.
	-> To reduce the traffic flow between client and arbiter, the request for vlanId from arbiter is reduced greatly to one request per flow.
	-> Retransmission helped in filling the lost packets. Since packets were dropped, more number of packets were sent than what is mentioned in the traffic files.

	
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
3) open third terminal and run command 1 followed by command 2
4) run command 5
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


