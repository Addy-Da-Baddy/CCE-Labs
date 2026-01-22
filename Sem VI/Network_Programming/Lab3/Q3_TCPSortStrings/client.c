#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

#define BUFFER_SIZE 1024
#define PORT 6868

int main() {
    int sockfd;
    struct sockaddr_in server_addr;
    char buff[BUFFER_SIZE];
    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd == -1) exit(1);
    printf("Socket created\n");
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(PORT);
    server_addr.sin_addr.s_addr = inet_addr("127.0.0.1");
    if (connect(sockfd, (struct sockaddr*)&server_addr, sizeof(server_addr)) == -1) exit(1);
    printf("Connected to server\n");
    while (1) {
        printf("Enter an alphanumeric string: ");
        fgets(buff, BUFFER_SIZE, stdin);
        buff[strcspn(buff, "\n")] = '\0';
        send(sockfd, buff, strlen(buff), 0);
        if (strcmp(buff, "CLOSE_MAGIC_X32") == 0) {
            printf("Closing connection\n");
            close(sockfd);
            break;
        }
        memset(buff, 0, sizeof(buff));
        recv(sockfd, buff, sizeof(buff), 0);
        printf("%s\n", buff);
        memset(buff, 0, sizeof(buff));
        recv(sockfd, buff, sizeof(buff), 0);
        printf("%s\n", buff);
    }
    return 0;
}
