#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include  <unistd.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>

#define PORT 8080
#define BUFFER_SIZE 1024



int main() {
    int sockserver, sockclient;
    struct sockaddr_in serverAddr, clientAddr;
    socklen_t clientAddrLen;
    char buf[BUFFER_SIZE];

    sockserver = socket(AF_INET, SOCK_STREAM, 0);
    if (sockserver < 0) {
        perror("Socket creation failed");
        exit(EXIT_FAILURE);
    }

    serverAddr.sin_family = AF_INET;
    serverAddr.sin_port = htons(PORT);
    serverAddr.sin_addr.s_addr = htonl(INADDR_ANY);

    if (bind(sockserver, (struct sockaddr*)&serverAddr, sizeof(serverAddr)) < 0) {
        perror("Bind failed");
        close(sockserver);
        exit(EXIT_FAILURE);
    }

    if (listen(sockserver, 1) < 0) {
        perror("Listen failed");
        close(sockserver);
        exit(EXIT_FAILURE);
    }

    printf("Server listening on port %d\n", PORT);


    clientAddrLen = sizeof(clientAddr);
    sockclient = accept(sockserver, (struct sockaddr*)&clientAddr, &clientAddrLen);
    if (sockclient < 0) {
        perror("Accept failed");
        close(sockserver);
        exit(EXIT_FAILURE);
    }


    int recvbytes = recv(sockclient, buf, BUFFER_SIZE - 1, 0);
    if (recvbytes < 0) {
        perror("Receive failed");
        close(sockclient);
        close(sockserver);
        exit(EXIT_FAILURE);
    }

    buf[recvbytes] = '\0';  // IMPORTANT
    puts("Message received from client:");
    puts(buf);

    printf("Enter response message: ");
    scanf("%1023s", buf);

    send(sockclient, buf, strlen(buf) + 1, 0);

    close(sockclient);
    close(sockserver);
    return 0;
}
