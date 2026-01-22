#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>

#define BUFFER_SIZE 1024
#define PORT 8080

int main() {
    int sockfd;
    struct sockaddr_in server_addr;
    socklen_t addr_len;
    char buff[BUFFER_SIZE];

    // Create UDP socket
    sockfd = socket(AF_INET, SOCK_DGRAM, 0);
    if (sockfd == -1) {
        perror("Socket creation failed");
        exit(1);
    }

    printf("UDP Client Socket Created\n");

    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(PORT);
    server_addr.sin_addr.s_addr = htonl(INADDR_LOOPBACK);

    addr_len = sizeof(server_addr);

    while (1) {
        printf("\nEnter string (or CLOSE to exit): ");
        fgets(buff, BUFFER_SIZE, stdin);
        buff[strcspn(buff, "\n")] = '\0';

        // Send string to server
        sendto(sockfd, buff, strlen(buff), 0,
               (struct sockaddr*)&server_addr, addr_len);

        if (strcmp(buff, "CLOSE") == 0)
            break;

        // Receive response from server
        memset(buff, 0, sizeof(buff));
        recvfrom(sockfd, buff, BUFFER_SIZE, 0,
                 (struct sockaddr*)&server_addr, &addr_len);

        printf("Server Response:\n%s\n", buff);
    }

    close(sockfd);
    return 0;
}
