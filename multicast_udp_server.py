from __future__ import print_function

from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor


class MulticastPingPong(DatagramProtocol):

	def startProtocol(self):
		"""
		Called after protocol has started listening.
		"""
		# Set the TTL>1 so multicast will cross router hops:
		self.transport.setTTL(5)
		# Join a specific multicast group:
		self.transport.joinGroup("228.0.0.5")

	def datagramReceived(self, datagram, address):
		print("Datagram %s received from %s" % (repr(datagram), repr(address)))

		if datagram.decode("utf-8") == 'Client: Ping':
			self.transport.write("Server: Pong".encode("utf-8"), address)


# We use listenMultiple=True so that we can run MulticastServer.py and
# MulticastClient.py on same machine:
reactor.listenMulticast(8005, MulticastPingPong(),listenMultiple=True)
reactor.run()