#!/usr/bin/python

"Project A ping connectivity test script"

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.log import setLogLevel
from mininet.node import RemoteController
from fat import FatTopo # TODO: change class name
from time import sleep


# get the VLAN for sending a packet from src to dst
def getVLAN(src, dst):
    return ((((src << 4 | dst)+272)+272)+272) # TODO: your logic here

# test connectivity between src and dst
def pingPairPartA(src, dst, net):
    s, d = net.hosts[src-1], net.hosts[dst-1]

    # start tcpdump on the destination host
    cmd = 'tcpdump -en -i {0}-eth1 1>{1}_tcpdump.txt 2> /dev/null &'.format(d.name, d.name)
    d.cmd(cmd)
    
    # send packet from the source host
    cmd = 'python vlan.py -i {0}-eth1 -d {1} -v {2}'.format(s.name, d.IP(), getVLAN(src, dst))
    s.sendCmd(cmd)
    s.waitOutput()

def pingPairPartB(src, dst, net):
    s, d = net.hosts[src-1], net.hosts[dst-1]

    # stop tcpdump in the destination host
    cmd = 'kill %tcpdump'
    d.sendCmd(cmd)
    d.waitOutput()

    # check if the tcpdump output contains a packet destined to the destination host
    cmd = "grep {0} {1}_tcpdump.txt".format(d.IP(), d.name)
    grepResult = d.cmd(cmd)

    # remove temporary files
    d.cmd('rm {0}_tcpdump.txt'.format(d.name))

    if (grepResult.find(d.IP()) > 0) :
        # return True if the destination received the packet i.e. ping successful
        return True
        
    return False

# driver that creates the network and tests connectivity
def pingTest():
    "Create network and run ping test"
    topo = FatTopo() # TODO: change class name
    net = Mininet(topo = topo, controller = RemoteController, autoSetMacs = True, autoStaticArp = True)

    net.start()
    print "Started mininet. Wait for 5 sec."

    # wait for the controller to install rules into the switches
    sleep(5)

    print "Testing network connectivity..."

    fail_cases = []

    for src in xrange(1, 17):
        print "{0}: ".format(net.hosts[src-1].name),
        for dst in xrange(1, 17):
            if src == dst:
                continue
            pingPairPartA(src, dst, net)

        sleep(2)

        for dst in xrange(1, 17):
            if src == dst:
                continue

            ok = pingPairPartB(src, dst, net)
            if ok:
                print "{0} ".format(net.hosts[dst-1].name),
            else:
                fail_cases.append((net.hosts[src-1].name, net.hosts[dst-1].name))
                print "X ",
        print("")

    # stop the network
    net.stop()

    # print summary
    if len(fail_cases) == 0:
        print("Passed")
    else:
        print("Failed {0} cases".format(len(fail_cases)))
        for pair in fail_cases:
            print("\t{0} -> {1}".format(pair[0], pair[1]))


if __name__ == '__main__':
    setLogLevel('output')
    pingTest()
