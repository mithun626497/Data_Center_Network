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

#define MYPORT "5000"
#define MAXBUFLEN 100

struct addrinfo hints,*servinfo, *p;
char buf[MAXBUFLEN];
int retVal,dgramSockFd,bytesRecv,bytesSent;
char hostname[20]="localhost";
//char hostname[20]="20.0.0.100";
socklen_t addr_len;
struct sockaddr_storage their_addr;

void *get_in_addr(struct sockaddr *sa)
{
	if (sa->sa_family == AF_INET) 
	{
		return &(((struct sockaddr_in*)sa)->sin_addr);
	}
	return &(((struct sockaddr_in6*)sa)->sin6_addr);
}

int createArbiterSocket()
{
	memset(&hints, 0, sizeof hints);
        hints.ai_family = AF_UNSPEC;
        hints.ai_socktype = SOCK_DGRAM;
        hints.ai_flags = AI_PASSIVE;

        if((retVal = getaddrinfo("20.0.0.100",MYPORT, &hints, &servinfo)) != 0)
        {
                fprintf(stderr, "getaddrinfo: %s\n", gai_strerror(retVal));
                return 1;
        }

        for(p = servinfo; p != NULL; p = p->ai_next)
        {
                //create a UDP socket to the doctor program
                if ((dgramSockFd = socket(p->ai_family, p->ai_socktype,p->ai_protocol)) == -1)
                {
                        perror("UDP socket() failed");
                        continue;
                }
                if (bind(dgramSockFd,p->ai_addr, p->ai_addrlen) == -1)
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
        addr_len = sizeof their_addr;
        
}
void receive_demand()
{
	if ((bytesRecv = recvfrom(dgramSockFd, buf, MAXBUFLEN-1 , 0,(struct sockaddr *)&their_addr, &addr_len)) == -1)
        {
        	perror("recvfrom failed");
                freeaddrinfo(servinfo);
                close(dgramSockFd);
                exit(1);
        }
	else {
	        buf[bytesRecv] = '\0';
                printf("Received %s\n",buf);
	}
}

void send_response(char *response)
{
	if ((bytesSent = sendto(dgramSockFd, response, strlen(response), 0,(struct sockaddr *)&their_addr, addr_len)) == -1)
        {
	        perror("UDP sendto failed");
                freeaddrinfo(servinfo);
                close(dgramSockFd);
                exit(1);
        }
        else
        {
                 printf("replied %s\n",response);
        }
}

int main()
{
	createArbiterSocket();
	//to keep track of the vlans issued 
	int vlans[1200][4]={0};
	int src,dest,vlan,newVlan;
	char response[MAXBUFLEN];
 	while(1)
	{
		memset(buf,0,sizeof(buf));
		receive_demand();
		//strcpy(response,"5678");
		src=(int)buf[0]-'0';
    		src*=10;
    		src+=(int)buf[1]-'0';
    		
		dest=(int)buf[2]-'0';
    		dest*=10;
    		dest+=(int)buf[3]-'0';
    		
		vlan = (src<<4)+dest;
		memset(response,0,sizeof(response));
		if(src == 13 || src == 14 || src==15)
		{
			vlans[vlan][0]=0;
		}
	loop:	if(vlans[vlan][0]==0)
		{
			vlans[vlan][0]++;
			snprintf(response, MAXBUFLEN,"%d",vlan);
			send_response(response);
		}
		else if(vlans[vlan][1]==0)
		{
			vlans[vlan][1]++;
			newVlan = vlan + 272;
			snprintf(response, MAXBUFLEN,"%d",newVlan);
			send_response(response);		
		}
		else if(vlans[vlan][2]==0)
                {
                        vlans[vlan][2]++;
			newVlan = vlan + (272*2);
			snprintf(response, MAXBUFLEN,"%d",newVlan);
                        send_response(response);
                }
		else if(vlans[vlan][3]==0)
                {
                        vlans[vlan][3]++;
			newVlan = vlan + (272*3);
			snprintf(response, MAXBUFLEN,"%d",newVlan);
                        send_response(response);
                }
		else
		{
			vlans[vlan][0]=0;
			vlans[vlan][1]=0;
			vlans[vlan][2]=0;
			vlans[vlan][3]=0;
			goto loop;
		}

    	}
	return 0;
}
