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
    struct sockaddr_in server_addr, client_addr;
    socklen_t addr_len;
    char buff[BUFFER_SIZE];

    sockfd = socket(AF_INET, SOCK_DGRAM, 0);
    if (sockfd == -1) {
        perror("Socket creation failed");
        exit(1);
    }

    printf("UDP Socket Created\n");

    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(PORT);
    server_addr.sin_addr.s_addr = htonl(INADDR_ANY);

    if (bind(sockfd, (struct sockaddr*)&server_addr, sizeof(server_addr)) == -1) {
        perror("Bind failed");
        close(sockfd);
        exit(1);
    }

    printf("Server listening on port %d\n", PORT);

    addr_len = sizeof(client_addr);

    while (1) {
        memset(buff, 0, sizeof(buff));
        recvfrom(sockfd, buff, BUFFER_SIZE, 0,
                 (struct sockaddr*)&client_addr, &addr_len);

        printf("\n Client: %s\n", buff);

        if (strcmp(buff, "CLOSE") == 0)
            break;

        printf(" Server: ");
        fgets(buff, BUFFER_SIZE, stdin);
        buff[strcspn(buff, "\n")] = '\0';

        sendto(sockfd, buff, strlen(buff), 0,
               (struct sockaddr*)&client_addr, addr_len);
    }

    close(sockfd);
    return 0;
}
