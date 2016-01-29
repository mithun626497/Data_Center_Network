from mininet.topo import Topo


class FatTopo(Topo):
    def __init__(self):
        
        Topo.__init__(self)
	#adding hosts 1 to 16
        for h in range(1,17):
            self.addHost("h"+str(h))
	#adding switches 1 to 20
        for s in range(1,21):
            self.addSwitch("s"+str(s))
       
	#adding links
	#adding host to switch links
 	self.addLink("h1","s4",0,4)
        self.addLink("h2","s4",0,3)
        self.addLink("h3","s3",0,4)
	self.addLink("h4","s3",0,3)
        self.addLink("h5","s8",0,4)
        self.addLink("h6","s8",0,3)
	self.addLink("h7","s7",0,4)
        self.addLink("h8","s7",0,3)
        self.addLink("h9","s12",0,4)
	self.addLink("h10","s12",0,3)
        self.addLink("h11","s11",0,4)
        self.addLink("h12","s11",0,3)	
	self.addLink("h13","s16",0,4)
        self.addLink("h14","s16",0,3)
        self.addLink("h15","s15",0,4)
        self.addLink("h16","s15",0,3)

	#adding links to pod switches
	#pod1
	self.addLink("s4","s1",1,4)
        self.addLink("s4","s2",2,4)
        self.addLink("s1","s3",3,1)
        self.addLink("s2","s3",3,2)
        #pod2
        self.addLink("s5","s8",4,1)
        self.addLink("s5","s7",3,1)
        self.addLink("s8","s6",2,4)
        self.addLink("s6","s7",3,2)
	#pod3
        self.addLink("s9","s12",4,1)
        self.addLink("s9","s11",3,1)
        self.addLink("s12","s10",2,4)
        self.addLink("s10","s11",3,2)
	#pod4
        self.addLink("s13","s16",4,1)
        self.addLink("s13","s15",3,1)
        self.addLink("s16","s14",2,4)
        self.addLink("s14","s15",3,2)

  	#adding links to core switches      
	#core switch 1
        self.addLink("s17","s1",1,1)
        self.addLink("s17","s5",2,1)
        self.addLink("s17","s9",3,1)
        self.addLink("s17","s13",4,1)
	#core switch 2
        self.addLink("s18","s1",1,2)
        self.addLink("s18","s5",2,2)
        self.addLink("s18","s9",3,2)
        self.addLink("s18","s13",4,2)
	#core switch 3
        self.addLink("s19","s2",1,1)
        self.addLink("s19","s6",2,1)
        self.addLink("s19","s10",3,1)
        self.addLink("s19","s14",4,1)
	#core switch 4
        self.addLink("s20","s2",1,2)
        self.addLink("s20","s6",2,2)
        self.addLink("s20","s10",3,2)
        self.addLink("s20","s14",4,2)
        
    
    @classmethod
    def create(cls):
        return cls()
        
topos = {"fattopo":FatTopo.create}
