#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>
#include <netdb.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <sys/wait.h>
#include <sys/ioctl.h>
#include <net/if.h> 
#define VLAN            yes
#include "Ether.h"
#include <fcntl.h>
#include <netinet/in.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <net/if.h>
#include <netinet/ip.h>
#include <netinet/udp.h>
#include <netinet/ether.h>
#include <linux/if_packet.h>

#define SRVPORT "5000"
#define BUFFSIZE 100
#define LINESIZE 50
#define VLANREQSIZE 30
#define DEBUG 0
#define MAX_PACKET_SIZE 2048
#define Period          1
enum commMode {SendAndReceive = 0, ReceiveThenSend = 1};
#define ETH_P_Exp       0x0800
#define NTerminals      4
uint16_t MAC1[NTerminals] = {0xffff, 0x0000, 0x0200, 0x0200};
uint32_t MAC2[NTerminals] = {0xffffffff, 0x00000000, 0x00000003, 0x00000004};
#define InitialReplyDelay       40
#define MaxCommCount            3
//#define IFNAME  "h1-ethX"
#define IFNAME "h1-ethX"

extern void _exit(int32_t);

struct addrinfo hints,*servinfo, *p;
struct sockaddr addr2;
int retVal,dgramSockFd,bytesSent,bytesRecv;
char hostname[20]="localhost";
int s,optval=1;
char recvBuf[BUFFSIZE];
FILE *fp;
char fpline[LINESIZE];
char vlanreq[VLANREQSIZE];
char srcIp[32],destIp[32];

int32_t ifindex;
int32_t myTermNum = 0;
int32_t destTermNum = 0;
int32_t ifnum = 0;
uint16_t vlanID = 1;
int32_t i;
int32_t count = 0;
long globalPktCount=0;
// Get terminal and interface numbers from the command line:

unsigned short csum(unsigned short *buf, int nwords)
{
    unsigned long sum;
    for(sum=0; nwords>0; nwords--)
        sum += *buf++;
    sum = (sum >> 16) + (sum &0xffff);
    sum += (sum >> 16);
    return (unsigned short)(~sum);
}

/**
 * Open a socket for the network interface
 */
int32_t open_socket(int32_t index, int32_t *rifindex,int hostNum) {
  unsigned char buf[MAX_PACKET_SIZE];
  int32_t i;
  int32_t ifindex;
  struct ifreq ifr;
  struct sockaddr_ll sll;
  
  /*unsigned */char ifname[IFNAMSIZ];
  memset(ifname,0,sizeof(ifname));
  strcpy(ifname,"h");
  if(hostNum<10){
  	ifname[1]='0'+hostNum;
  //	ifname[me)]='\0';
  	strcat(ifname,"-ethX");
  }
  else 
  {
	ifname[1]='0'+(hostNum/10);
	ifname[2]='0'+(hostNum%10);
      //ifname[strlen(ifname)]='\0';
	strcat(ifname,"-ethX");
	
  }
  ifname[strlen(ifname) - 1] = '1' + index;
  int32_t fd = socket(PF_PACKET, SOCK_RAW, htons(ETH_P_ALL));
  if (fd == -1) {
    printf("%s - ", ifname);
    perror("socket");
    _exit(1);
  };


  // get interface index
  memset(&ifr, 0, sizeof(ifr));
  strncpy(ifr.ifr_name, ifname, IFNAMSIZ);
  //strncpy(ifr.ifr_name, "h1-eth1", IFNAMSIZ);
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
ssize_t createPacket( char *packet, uint16_t destMAC1, uint32_t destMAC2,
                     uint16_t srcMAC1, uint32_t srcMAC2, uint16_t type, uint32_t vlanTag,
                     int32_t payload,char *srcIp, char *destIp,short srcPortShort,short destPortShort) {
  ssize_t packetSize = sizeof(EtherPacket);
  int tx_len = sizeof(EtherPacket);
  int i;

  EtherPacket *p = (EtherPacket *) (packet);
  // ssize_t packetSize = payloadLength + sizeof(EtherPacket);
  p->destMAC1 = htons(destMAC1);
  p->destMAC2 = htonl(destMAC2);
  p->srcMAC1 = htons(srcMAC1);
  p->srcMAC2 = htonl(srcMAC2);
//#ifdef VLAN
  p->VLANTag = htonl(vlanTag);
//#endif
  p->type = htons(type);
 // packet->payload = htonl(payload);
  // strncpy(packet->payload, payload, packetSize);
  struct iphdr *iph = (struct iphdr *) (packet + sizeof(EtherPacket));
  iph->ihl = 5;
  iph->version = 4;
  iph->tos = 16; // Low delay
  iph->id = htons(54321);
  iph->ttl = 255; // hops
  iph->protocol = 17; // UDP
  /* Source IP address, can be spoofed */
  iph->saddr = inet_addr(srcIp);
  // iph->saddr = inet_addr("192.168.0.112");
  /* Destination IP address */
  iph->daddr = inet_addr(destIp);
  iph->tot_len = htons(tx_len - sizeof(EtherPacket));
  iph->check = csum((unsigned short *)(packet+sizeof(EtherPacket)),sizeof(struct iphdr)/2);
  tx_len += sizeof(struct iphdr);
  
  struct udphdr *udph = (struct udphdr *) (packet + sizeof(struct iphdr) + sizeof(EtherPacket));
  udph->source = htons(srcPortShort);
  udph->dest = htons(destPortShort);
  udph->check = 0; // skip
  tx_len += sizeof(struct udphdr);
  udph->len = htons(tx_len - sizeof(EtherPacket)-sizeof(struct iphdr));

  for(i=tx_len;i<tx_len+1000;i++) {
 	 packet[i] = 'a';
  }
  tx_len = tx_len+1000;
 // packet[tx_len++] = 0xbe;
 // packet[tx_len++] = 0xae;
  //}
 // printf("mithun packetSize %zu\n",packetSize);  
 // printf("packet %zu\n",sizeof(packet));
  return 1046;
}


int32_t lastPayload = -1;

/**
 * Print IPEC packet content
 */
/*
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

*/
/**
 * Send packets to terminals
 */
void sendPackets(int32_t fd, int32_t ifindex, uint16_t SrcMAC1, uint32_t SrcMAC2,
                 uint16_t DestMAC1, uint32_t DestMAC2, uint16_t type, uint32_t vlanTag,
                 int32_t *count,char *srcIp,char *destIp,short srcPortShort,short destPortShort) {
  int32_t i;
  char packet[1046];
  // unsigned char *payload = "Hello!";

  struct sockaddr_ll sll;
  memset(&sll, 0, sizeof(sll));
  sll.sll_family = AF_PACKET;
  sll.sll_protocol = htons(ETH_P_ALL);  // Ethernet type = Trans. Ether Bridging
  sll.sll_ifindex = ifindex;

  ssize_t packetSize = createPacket(packet, DestMAC1, DestMAC2,
                                    SrcMAC1, SrcMAC2, type, vlanTag, (*count)++,srcIp,destIp,srcPortShort,destPortShort);
  ssize_t sizeout = sendto(fd, packet, packetSize, 0,
                           (struct sockaddr *)&sll, sizeof(sll));
  /*
  printPacket((EtherPacket*)packet, packetSize, "Sent:    ");
  */
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
                 uint16_t DestMAC1, uint32_t DestMAC2, uint16_t type, uint16_t vlanID,char *srcIp,char *destIp,short srcPortShort,short destPortShort) {
  unsigned char buf[MAX_PACKET_SIZE];
  int32_t sendCount = 0;
  int32_t receiveCount = 0;
  time_t lastTime = time(NULL);
  int32_t replyDelay = 0;
  int32_t i;
  uint32_t vlanTag = 0x81000000 | vlanID;

   /*
  // Sending and receiving packets:
  for (; sendCount < MaxCommCount && receiveCount < MaxCommCount;) {
    if (DestMAC2 != 0 && replyDelay <= 0) {
      int32_t currTime = time(NULL);
      if (currTime - lastTime >= Period) {
        if (DEBUG) printf("currTime=%d lastTime=%d\n", currTime, (int32_t)lastTime);
	*/
        sendPackets(fd, ifindex, SrcMAC1, SrcMAC2, DestMAC1, DestMAC2, type, vlanTag,
                    &sendCount,srcIp,destIp,srcPortShort,destPortShort);
	/*
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
  }*/
}


int createClientSocket()
{
	memset(&hints, 0, sizeof hints);
        hints.ai_family = AF_UNSPEC;
        hints.ai_socktype = SOCK_DGRAM;
	
	if ((retVal = getaddrinfo("20.0.0.100",SRVPORT, &hints, &servinfo)) != 0)
        {
                fprintf(stderr, "getaddrinfo: %s\n", gai_strerror(retVal));
                return 1;
        }
	memset(&addr2, 0, sizeof addr2);
	
	setsockopt(s, SOL_SOCKET, SO_REUSEADDR, &optval, sizeof optval);

        for(p = servinfo; p != NULL; p = p->ai_next)
        {
                if ((dgramSockFd = socket(p->ai_family, p->ai_socktype,p->ai_protocol)) == -1)
                {
                        perror("UDP socket() failed");
                        continue;
                }
                if (bind(dgramSockFd,(struct sockaddr *)&addr2, sizeof addr2) == -1)
                {
                        close(dgramSockFd);
                        perror("UDP bind() Failed");
                        continue;
                }
                break;
        }
	if (p == NULL)
        {
                fprintf(stderr, "failed to bind socket\n");
                freeaddrinfo(servinfo);
                return 2;
        }

}

void send_demands(char *buf)
{
	if ((bytesSent = sendto(dgramSockFd, buf, strlen(buf), 0,p->ai_addr, p->ai_addrlen)) == -1)
        {
                perror("send demand failed");
                freeaddrinfo(servinfo);
                close(dgramSockFd);
                exit(1);
        }
        else
                printf("Sent %s\n",buf);

}
void receive_demands(char *recvBuf)
{
	if ((bytesRecv = recvfrom(dgramSockFd, recvBuf, BUFFSIZE-1 , 0,(struct sockaddr *)p->ai_addr, &(p->ai_addrlen))) == -1)
        {
                perror("recv demand failed");
                freeaddrinfo(servinfo);
                close(dgramSockFd);
                exit(1);
        }
        else
        {
                recvBuf[bytesRecv] = '\0';
                printf("Received %s\n",recvBuf);
        }

}

void command_parser(char *argv)
{
	/* 
	Perform the following in loop
	- Open the files from h1 to h16.tr one by one
	- read the input file and extract destination host, port and message size 
	*/
	int i,j,k,n,p,q,z,m,msgLenInt,Npackets,Ndemands,tmpLen,vlanIdInt,PktPerFlow;
	long long msgLenLong;
	char fileName[100],assignedVlan[100];
	char temp[3],dest[3],destPort[10],msgLen[10];
	char *ptr;
	pid_t pid1,pid2,wpid,wpid2,children1[1000],children2[1000];
	int count1=0,count2=0,vlans[4],processCount,pathid;
	int status,status2;
	int hostNum;
	short destPortShort,srcPortShort=3000;
  	
	char tempArgv[10],*aptr;
        strcpy(tempArgv,argv);
        aptr = strchr(tempArgv,'h');
        if(*(aptr+2)=='.')
        {
                hostNum= *(aptr+1)-'0';
        }
        else if(*(aptr+3)=='.')
        {
                hostNum = *(aptr+1)-'0';
                hostNum*=10;
                hostNum+=*(aptr+2)-'0';
        }
        printf("hostNum=%d\n",hostNum);
 	
	memset(fileName,0,sizeof(fileName));
	strcpy(fileName,tempArgv);
	printf("filename=%s\n",tempArgv);
	int32_t fd = open_socket(ifnum, &ifindex,hostNum);
	printf("fd=%d\n",fd);
	fp=fopen(fileName,"r");
	if(fp==NULL) {
		printf("file Opening failed\n");
		exit(0);
	}
	while(fgets(fpline,sizeof(fpline),fp)!=NULL)
	{	
		memset(vlanreq,0,sizeof(vlanreq));
		memset(srcIp,0,sizeof(srcIp));
		strcpy(srcIp,"10.0.0.");
		//set the source host
		if(hostNum<10) {
			vlanreq[0]='0';
			vlanreq[1]=hostNum+'0';
			srcIp[strlen(srcIp)]=vlanreq[1];
			srcIp[strlen(srcIp)]='\0';
		}
		else {
			vlanreq[0]=(hostNum/10)+'0';
			vlanreq[1]=(hostNum%10)+'0';
			temp[0]=vlanreq[0];
			temp[1]=vlanreq[1];
			temp[2]='\0';
			strcpy(vlanreq,temp);
			strcat(srcIp,temp);
		}
		memset(destIp,0,sizeof(destIp));
		memset(dest,0,sizeof(dest));
		ptr = strchr(fpline,'h');
		if(ptr!=NULL) {
		        if(*(ptr+3)==' ')
    			{
        			dest[0]=*(ptr+1);
        			dest[1]=*(ptr+2);
        			dest[2]='\0';
    			}
    			else {
        			dest[0]='0';
        			dest[1]=*(ptr+1);
        			dest[2]='\0';
    			}
			//add the destination host to the request
			strcat(vlanreq,dest);
		}
		strcpy(destIp,"10.0.0.");
		strcat(destIp,dest);
		memset(destPort,0,strlen(destPort));
		ptr = strchr(fpline,'p');
		if(ptr!=NULL) {
			destPort[0]=*(ptr+2);
        		destPort[1]=*(ptr+3);
        		destPort[2]=*(ptr+4);
        		destPort[3]=*(ptr+5);
        		destPort[4]='\0';
				//add the destination port number to the request
                        	//strcat(vlanreq,destPort);		
		}
		destPortShort = atoi(destPort);
		memset(msgLen,0,strlen(msgLen));
                ptr = strchr(fpline,'n');
		j=0;k=2;
     		if(ptr!=NULL) {
			while(*(ptr+k) != 'M') 
			{
        			msgLen[j++]=*(ptr+k);
        			k++;
     			}
     			msgLen[j]='\0';

                        //add the message length to the request
                        //strcat(vlanreq,msgLen);
		}
		strcat(vlanreq,"\0");
		tmpLen =strlen(msgLen);
		if(tmpLen==1)
		{
			msgLenInt = (int)msgLen[0]-'0';
		}
		else if (tmpLen==2) {
			msgLenInt=(int)msgLen[0]-'0';
			msgLenInt*=10;
			msgLenInt+=(int)msgLen[1]-'0';
		}
		else if (tmpLen==3) {
                        msgLenInt=(int)msgLen[0]-'0';
                        msgLenInt*=10;
                        msgLenInt+=(int)msgLen[1]-'0';
			msgLenInt*=10;
			msgLenInt+=(int)msgLen[2]-'0';
                }
		printf("Mithun vlanreq %s\n",vlanreq);
		msgLenLong = msgLenInt*1000000;
		//Npackets = (msgLenLong/1500)+(!(!(msgLenLong%1500)));		
		Npackets = (msgLenLong/1000)+(!(!(msgLenLong%1000)));
		//Ndemands = (Npackets/500)+(!(!(Npackets%500)));
		Ndemands = Npackets;
		printf("msgLenLong %lld,Npacket %d,Ndemads %d, vlandreq %s\n",msgLenLong,Npackets,Ndemands,vlanreq);
		//Ndemands = 4;
		//PktPerFlow = Npackets/Ndemands;
		for(n=0;n<Ndemands;n++)
		{
			//the request is ready. Send the request to arbiter
			send_demands(vlanreq);
			//receive the assigned vlan id for the request
			receive_demands(assignedVlan);
			printf("Mithun vlan=%s\n",assignedVlan);
				//code to create raw socket and send the packets on
				//the assigned vlan id.
				// Set locators and IDs using terminal number:
				/*
  				uint16_t SrcMAC1  = MAC1[myTermNum];
  				uint32_t SrcMAC2  = MAC2[myTermNum];
  				uint16_t DestMAC1 = MAC1[destTermNum];
  				uint32_t DestMAC2 = MAC2[destTermNum];
				*/
			vlanIdInt = atoi(assignedVlan);
				//vlans[n]=vlanIdInt;
			
				//printf("vlanIdInt = %d\n",vlanIdInt);
			uint16_t SrcMAC1  = MAC1[1];
                        uint32_t SrcMAC2  = MAC2[1];
                        uint16_t DestMAC1 = MAC1[0];
                        uint32_t DestMAC2 = MAC2[0];
//  				printf("eth%d terminal#=%d VLAN:%d srcMAC:%08x%04x destMAC:%08x%04x\n",
  //       				ifnum, myTermNum, vlanID,
    //     				(int32_t)SrcMAC1, (int32_t)SrcMAC2, (int32_t)DestMAC1, (int32_t)DestMAC2);

				//printf("before open socket\n");
				//printf("after open socket\n");
				//consider sending 50 packets per flow per process
				//processCount = (PktPerFlow/50)+(!(!(PktPerFlow%50)));
  				// Set non-blocking mode:
  			int32_t flags = fcntl(fd, F_GETFL, 0);
  			fcntl(fd, F_SETFL, O_NONBLOCK | flags);
			printf("Mits vlanid=%d\n",vlanIdInt);
			//for(m=0;m<500;m++){
			//	globalPktCount++; 
	  			sendReceive(fd, ifindex, SrcMAC1, SrcMAC2, DestMAC1, DestMAC2, ETH_P_Exp, vlanIdInt,srcIp,destIp,srcPortShort,destPortShort);
			//}
		}
		printf("Npackets %d,globalPktCount %ld\n",Npackets,globalPktCount);
	}
	fclose(fp);		
	
}
test(char *argv)
{
	int x;
	char temp[10];
	char *aptr;
	strcpy(temp,argv);
 	aptr = strchr(temp,'h');
	if(*(aptr+2)=='.')
	{
		x = *(aptr+1)-'0';	
	}
	else if(*(aptr+3)=='.')
	{
		x = *(aptr+1)-'0';
		x*=10;
		x+=*(aptr+2)-'0';
	}
	printf("argv=%d\n",x);

}

int main(int32_t argc, char *argv[])
{
	
	createClientSocket();
	//test(argv[1]);
	command_parser(argv[1]);	
	close(dgramSockFd);	
   	return 0;
}
