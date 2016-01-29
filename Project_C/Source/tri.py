from mininet.topo import Topo
class Triangle(Topo):
	def __init__(self):
		Topo.__init__(self)
		# Create the custom topo here by using:
		# self.addHost, self.addSwitch, and self.addLink
		self.addHost("h1")
		self.addHost("h2")

		self.addSwitch("s1")
		self.addSwitch("s2")
		self.addSwitch("s3")

		self.addLink("h1", "s1")
		self.addLink("h2", "s2")

		self.addLink("s1", "s2")
		self.addLink("s2", "s3")
		self.addLink("s3", "s1")

	@classmethod
	def create(cls):
		return cls()

topos = {'tri': Triangle.create}

