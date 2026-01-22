#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <sys/types.h>
#include <string.h>
#include <unistd.h>

#define BUFFER_SIZE 1024
#define PORT 8080

int main() {
    int sockfd, newsockfd, retval;
    struct sockaddr_in server_addr, client_addr;
    socklen_t addr_len;
    char buff[BUFFER_SIZE];

    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd == -1) {
        perror("Socket creation failed");
        exit(0);
    }

    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(PORT);
    server_addr.sin_addr.s_addr = htonl(INADDR_ANY);

    retval = bind(sockfd, (struct sockaddr*)&server_addr, sizeof(server_addr));
    if (retval == -1) {
        perror("Bind failed");
        close(sockfd);
        exit(0);
    }

    retval = listen(sockfd, 1);
    if (retval == -1) {
        perror("Listen failed");
        close(sockfd);
        exit(0);
    }

    addr_len = sizeof(client_addr);
    newsockfd = accept(sockfd, (struct sockaddr*)&client_addr, &addr_len);
    if (newsockfd == -1) {
        perror("Accept failed");
        close(sockfd);
        exit(0);
    }

    pid_t pid = fork();
    if (pid == 0) {
        printf("Child Process PID: %d, PPID: %d\n", getpid(), getppid());
        while (1) {
            memset(buff, 0, sizeof(buff));
            int recdbytes = recv(newsockfd, buff, sizeof(buff), 0);
            if (recdbytes <= 0) break;
            printf("\nClient: %s\n", buff);
            if (strcmp(buff, "CLOSE") == 0) break;
        }
    } else {
        printf("Parent Process PID: %d, PPID: %d\n", getpid(), getppid());
        while (1) {
            printf("Server: ");
            fflush(stdout);
            fgets(buff, BUFFER_SIZE, stdin);
            buff[strcspn(buff, "\n")] = '\0';
            send(newsockfd, buff, strlen(buff), 0);
            if (strcmp(buff, "CLOSE") == 0) break;
        }
    }

    close(newsockfd);
    close(sockfd);
    return 0;
}
