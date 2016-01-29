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

#define SRVPORT "5000"
#define BUFFSIZE 100
#define LINESIZE 50
#define VLANREQSIZE 30

struct addrinfo hints,*servinfo, *p;
struct sockaddr addr2;
int retVal,dgramSockFd,bytesSent,bytesRecv;
char hostname[20]="localhost";
int s,optval=1;
char recvBuf[BUFFSIZE];
FILE *fp;
char fpline[LINESIZE];
char vlanreq[VLANREQSIZE];

int createClientSocket()
{
	memset(&hints, 0, sizeof hints);
        hints.ai_family = AF_UNSPEC;
        hints.ai_socktype = SOCK_DGRAM;
	
	if ((retVal = getaddrinfo(hostname,SRVPORT, &hints, &servinfo)) != 0)
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
void command_parser()
{
	/* 
	Perform the following in loop
	- Open the files from h1 to h16.tr one by one
	- read the input file and extract destination host, port and message size 
	*/
	int i,j,k,n,msgLenInt,Npackets,Ndemands,tmpLen;
	long long msgLenLong;
	char fileName[100],assignedVlan[100];
	char temp[3],dest[3],destPort[10],msgLen[10];
	char *ptr;
	for(i=1;i<16;i++)
	{	
		memset(fileName,0,sizeof(fileName));
		/*Generate the filename including the path*/
		strcpy(fileName,"traffic/h");
		if(i<10) {
			temp[0]=(char)i+'0';
			temp[1]='\0';
		}
		else {
			temp[0]='1';
			temp[1]=(char)i%10 + '0';
			temp[2]='\0';
		}
		strcat(fileName,temp);
		strcat(fileName,".tr\0");
		/*fileName has the name of the file. Open the file and read the lines*/
		fp=fopen(fileName,"r");
		if(fp==NULL) {
			printf("file Opening failed\n");
			break;
		}
		while(fgets(fpline,sizeof(fpline),fp)!=NULL)
		{	
			memset(vlanreq,0,sizeof(vlanreq));
			//set the source host
			if(i<10) {
				vlanreq[0]='0';
				vlanreq[1]=(char)i+'0';
			}
			else {
				strcpy(vlanreq,temp);
			}

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

			msgLenLong = msgLenInt*1000000;
			Npackets = (msgLenLong/1500)+(!(!(msgLenLong%1500)));		
			Ndemands = (Npackets/200)+(!(!(Npackets%200)));
			for(n=0;n<Ndemands;n++)
			{
				//the request is ready. Send the request to arbiter
				send_demands(vlanreq);
				//receive the assigned vlan id for the request
				receive_demands(assignedVlan);
				printf("vlan=%s\n",assignedVlan);
			}
		}
		fclose(fp);	
	}
	
}
int main()
{
	
	createClientSocket();
	
	/*
	strcpy(buf,"1234");
	send_demands(buf);

	memset(recvBuf,0,sizeof(recvBuf));
	receive_demands(recvBuf);
	
 	*/
	command_parser();	
//	close(dgramSockFd);	
   	return 0;
}
