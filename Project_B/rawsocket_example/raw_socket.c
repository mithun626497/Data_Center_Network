/***
 *
 * Generate/Receive Ethernet Packet
 *
 * Coded by Yasusi Kanada
 * Ver 1.0  2012-5-20	Initial version
 *
 ***/

#define VLAN		1
#define DEBUG		0

#include "Ether.h"
#include <fcntl.h>

#define MAX_PACKET_SIZE	2048
	// Sufficiently larger than the MTU

#define Period		1

enum commMode {SendAndReceive = 0, ReceiveThenSend = 1};

#define ETH_P_Exp	0x88b5
	// Ethernet type = IEEE 802.1 Local Experimental Ethertype 1

#define NTerminals	4
uint16_t MAC1[NTerminals] = {0xd636, 0x224e, 0x0200, 0x0200};
uint32_t MAC2[NTerminals] = {0x3cc450a0, 0xe8cd9100, 0x00000003, 0x00000004};

#define InitialReplyDelay	40
#define MaxCommCount		3

#define IFNAME	"h1-ethX"
	// or "gretapX"


extern void _exit(int32_t);


/**
 * Open a socket for the network interface
 */
int32_t open_socket(int32_t index, int32_t *rifindex) {
  unsigned char buf[MAX_PACKET_SIZE];
  int32_t i;
  int32_t ifindex;
  struct ifreq ifr;
  struct sockaddr_ll sll;
  unsigned char ifname[IFNAMSIZ];
  strncpy(ifname, IFNAME, IFNAMSIZ);
  ifname[strlen(ifname) - 1] = '0' + index;

  int32_t fd = socket(PF_PACKET, SOCK_RAW, htons(ETH_P_ALL));
  if (fd == -1) {
    printf("%s - ", ifname);
    perror("socket");
    _exit(1);
  };

  // get interface index
  memset(&ifr, 0, sizeof(ifr));
  strncpy(ifr.ifr_name, ifname, IFNAMSIZ);
  if (ioctl(fd, SIOCGIFINDEX, &ifr) == -1) {
    printf("%s - ", ifname);
    perror("SIOCGIFINDEX");
    _exit(1);
  };
  ifindex = ifr.ifr_ifindex;
  *rifindex = ifindex;

  // set promiscuous mode
  memset(&ifr, 0, sizeof(ifr));
  strncpy(ifr.ifr_name, ifname, IFNAMSIZ);
  printf("ifname = %s\n", ifname);
  
  ioctl(fd, SIOCGIFFLAGS, &ifr);
  ifr.ifr_flags |= IFF_PROMISC;
  ioctl(fd, SIOCSIFFLAGS, &ifr);

  memset(&sll, 0xff, sizeof(sll));
  sll.sll_family = AF_PACKET;
  sll.sll_protocol = htons(ETH_P_ALL);
  sll.sll_ifindex = ifindex;
  if (bind(fd, (struct sockaddr *)&sll, sizeof(sll)) == -1) {
    printf("%s - ", ifname);
    perror("bind");
    _exit(1);
  };

  /* flush all received packets. 
   *
   * raw-socket receives packets from all interfaces
   * when the socket is not bound to an interface
   */
  do {
    fd_set fds;
    struct timeval t;
    FD_ZERO(&fds);	
    FD_SET(fd, &fds);
    memset(&t, 0, sizeof(t));
    i = select(FD_SETSIZE, &fds, NULL, NULL, &t);
    if (i > 0) {
      recv(fd, buf, i, 0);
    };
    if (DEBUG) printf("interface %d flushed\n", ifindex);
  } while (i);

  if (DEBUG) printf("%s opened (fd=%d interface=%d)\n", ifname, fd, ifindex);

  return fd;
}


/**
 * Create an IPEC packet
 */
ssize_t createPacket(EtherPacket *packet, uint16_t destMAC1, uint32_t destMAC2,
		     uint16_t srcMAC1, uint32_t srcMAC2, uint16_t type, uint32_t vlanTag,
		     int32_t payload) {
  ssize_t packetSize = sizeof(EtherPacket);
  // ssize_t packetSize = payloadLength + sizeof(EtherPacket);
  packet->destMAC1 = htons(destMAC1);
  packet->destMAC2 = htonl(destMAC2);
  packet->srcMAC1 = htons(srcMAC1);
  packet->srcMAC2 = htonl(srcMAC2);
#ifdef VLAN
  packet->VLANTag = htonl(vlanTag);
#endif
  packet->type = htons(type);
  packet->payload = htonl(payload);
  // strncpy(packet->payload, payload, packetSize);
  return packetSize;
}


int32_t lastPayload = -1;

/**
 * Print IPEC packet content
 */
void printPacket(EtherPacket *packet, ssize_t packetSize, char *message) {
#ifdef VLAN
  printf("%s #%d (VLAN %d) from %08x%04x to %08x%04x\n",
	 message, ntohl(packet->payload), ntohl(packet->VLANTag) & 0xFFF,
#else
  printf("%s #%d from %08x%04x to %08x%04x\n",
	 message, ntohl(packet->payload),
#endif
	 ntohs(packet->srcMAC1), ntohl(packet->srcMAC2),
	 ntohs(packet->destMAC1), ntohl(packet->destMAC2));
  lastPayload = ntohl(packet->payload);
}


/**
 * Send packets to terminals
 */
void sendPackets(int32_t fd, int32_t ifindex, uint16_t SrcMAC1, uint32_t SrcMAC2,
		 uint16_t DestMAC1, uint32_t DestMAC2, uint16_t type, uint32_t vlanTag,
		 int32_t *count) {
  int32_t i;
  unsigned char packet[MAX_PACKET_SIZE];
  // unsigned char *payload = "Hello!";

  struct sockaddr_ll sll;
  memset(&sll, 0, sizeof(sll));
  sll.sll_family = AF_PACKET;
  sll.sll_protocol = htons(ETH_P_ALL);	// Ethernet type = Trans. Ether Bridging
  sll.sll_ifindex = ifindex;

  ssize_t packetSize = createPacket((EtherPacket*)packet, DestMAC1, DestMAC2,
				    SrcMAC1, SrcMAC2, type, vlanTag, (*count)++);
  ssize_t sizeout = sendto(fd, packet, packetSize, 0,
			   (struct sockaddr *)&sll, sizeof(sll));
  printPacket((EtherPacket*)packet, packetSize, "Sent:    ");
  if (sizeout < 0) {
    perror("sendto");
  } else {
    if (DEBUG) {
      printf("%d bytes sent through interface (ifindex) %d\n",
	     (int32_t)sizeout, (int32_t)ifindex);
    }
  }
}


void sendReceive(int32_t fd, int32_t ifindex, uint16_t SrcMAC1, uint32_t SrcMAC2,
		 uint16_t DestMAC1, uint32_t DestMAC2, uint16_t type, uint16_t vlanID) {
  unsigned char buf[MAX_PACKET_SIZE];
  int32_t sendCount = 0;
  int32_t receiveCount = 0;
  time_t lastTime = time(NULL);
  int32_t replyDelay = 0;
  int32_t i;
  uint32_t vlanTag = 0x81000000 | vlanID;

  // Sending and receiving packets:
  for (; sendCount < MaxCommCount && receiveCount < MaxCommCount;) {
    if (DestMAC2 != 0 && replyDelay <= 0) {
      int32_t currTime = time(NULL);
      if (currTime - lastTime >= Period) {
	if (DEBUG) printf("currTime=%d lastTime=%d\n", currTime, (int32_t)lastTime);
	sendPackets(fd, ifindex, SrcMAC1, SrcMAC2, DestMAC1, DestMAC2, type, vlanTag,
		    &sendCount);
	lastTime = currTime;
      }
    }
    ssize_t sizein = recv(fd, buf, MAX_PACKET_SIZE, 0);
    if (sizein >= 0) {
      EtherPacket *packet = (EtherPacket*) buf;
      if (DestMAC2 == 0) {
	DestMAC1 = ntohs(packet->srcMAC1);
	DestMAC2 = ntohl(packet->srcMAC2);
	replyDelay = InitialReplyDelay;
      } else if (replyDelay > 0) {
	replyDelay--;
      }
      printPacket(packet, sizein, "Received:");
      receiveCount++;
    } else {
      usleep(10000); // sleep for 10 ms
    }
  }
}


/**
 * Main program
 */
int32_t main(int32_t argc, char **argv) {
  int32_t ifindex;
  int32_t myTermNum = 0;
  int32_t destTermNum = 0;
  int32_t ifnum = 0;
  uint16_t vlanID = 1;
  int32_t i;

  // Get terminal and interface numbers from the command line:
  int32_t count = 0;
  if (++count < argc) {
    myTermNum = atoi(argv[count]);	// My terminal number
  }
  if (myTermNum >= NTerminals || myTermNum < 0) {
    printf("My terminal number (%d) too large\n", myTermNum);
    myTermNum = 0;
  }

  if (++count < argc) {
    destTermNum = atoi(argv[count]);	// Destination terminal number
  }
  if (destTermNum >= NTerminals || destTermNum < 0) {
    printf("Destination terminal number (%d) too large\n", destTermNum);
    destTermNum = 1;
  }

  if (++count < argc) {
    ifnum = atoi(argv[count]);		// Interface number
  }

  if (++count < argc) {
    vlanID = atoi(argv[count]);		// VLAN ID
  }
  if (vlanID < 1 || 4095 < vlanID) {
    printf("VLAN ID %d out of range (1..4095)\n", vlanID);
    vlanID = 1;
  }

  // Set locators and IDs using terminal number:
  uint16_t SrcMAC1  = MAC1[myTermNum];
  uint32_t SrcMAC2  = MAC2[myTermNum];
  uint16_t DestMAC1 = MAC1[destTermNum];
  uint32_t DestMAC2 = MAC2[destTermNum];
  printf("eth%d terminal#=%d VLAN:%d srcMAC:%08x%04x destMAC:%08x%04x\n",
	 ifnum, myTermNum, vlanID,
	 (int32_t)SrcMAC1, (int32_t)SrcMAC2, (int32_t)DestMAC1, (int32_t)DestMAC2);

  
  int32_t fd = open_socket(ifnum, &ifindex);

  // Set non-blocking mode:
  int32_t flags = fcntl(fd, F_GETFL, 0);
  fcntl(fd, F_SETFL, O_NONBLOCK | flags);

  sendReceive(fd, ifindex, SrcMAC1, SrcMAC2, DestMAC1, DestMAC2, ETH_P_Exp, vlanID);
}
