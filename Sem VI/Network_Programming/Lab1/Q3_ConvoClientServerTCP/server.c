#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <sys/types.h>
#include <string.h>
#include<unistd.h>

#define BUFFER_SIZE 1024
#define PORT 8080

int main(){
    int sockfd, newsockfd, retval;
    struct sockaddr_in server_addr, client_addr;
    socklen_t addr_len;
    char buff[BUFFER_SIZE];
    //order is socket(), bind(), listen(), accept(), recv(), send(), close()

    sockfd = socket(AF_INET,SOCK_STREAM,0);

    if (sockfd==-1){
        printf("Socket Connection failed");
        exit(0);
    }

    printf("\n Socket Connected \n ");

    server_addr.sin_family=AF_INET;
    server_addr.sin_port = htons(PORT);
    server_addr.sin_addr.s_addr=htonl(INADDR_ANY);

    retval = bind(sockfd,(struct sockaddr*)&server_addr,sizeof(server_addr));

    if (retval==-1){
        printf("Binding Error!");
        close(sockfd);
        exit(0);
    }

    printf("\n Socket Binded on AF_INET \n");

    retval = listen(sockfd,1);
    

    if (retval==-1){
        printf("Listening Error!");
        close(sockfd);
        exit(0);
    }

    printf("\n Listening on port %d \n", PORT);

    addr_len = sizeof(client_addr);
    newsockfd = accept(sockfd, (struct sockaddr*)&client_addr,&addr_len);

    if (newsockfd==-1){
        printf("Connection failed");
        close(sockfd);
        exit(0);
    }
    printf("\n Connection Established with Client\n");

    for(int i=0;;i++){

        printf("\n Server: ");
        fgets(buff,BUFFER_SIZE,stdin);
        buff[strcspn(buff, "\n")] = '\0';
        int sendbytes = send(newsockfd,buff,strlen(buff),0);

        memset(buff,0,sizeof(buff));
        int recdbytes = recv(newsockfd,buff,sizeof(buff),0);
        printf("\n Client:");
        puts(buff);

        if (sendbytes == -1){
            printf("Error in sending. Forcing connection to close");
            close(sockfd);
            close(newsockfd);
            exit(0);
        }

        if (strcmp(buff,"CLOSE")==0){
            break;
        }
    }

    printf("\n Connection Closing");
    close(sockfd);
    close(newsockfd);
    return 0;
}