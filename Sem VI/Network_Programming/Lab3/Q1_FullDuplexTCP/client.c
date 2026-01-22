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
    int sockfd, retval;
    struct sockaddr_in server_addr;
    char buff[BUFFER_SIZE];

    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd == -1) {
        perror("Socket creation failed");
        exit(0);
    }

    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(PORT);
    server_addr.sin_addr.s_addr = htonl(INADDR_ANY);

    retval = connect(sockfd, (struct sockaddr*)&server_addr, sizeof(server_addr));
    if (retval == -1) {
        perror("Connection failed");
        close(sockfd);
        exit(0);
    }

    pid_t pid = fork();
    if (pid == 0) {
        printf("Child Process PID: %d, PPID: %d\n", getpid(), getppid());
        while (1) {
            memset(buff, 0, sizeof(buff));
            int recdbytes = recv(sockfd, buff, sizeof(buff), 0);
            if (recdbytes <= 0) break;
            printf("\nServer: %s\n", buff);
            if (strcmp(buff, "CLOSE") == 0) break;
        }
    } else {
        printf("Parent Process PID: %d, PPID: %d\n", getpid(), getppid());
        while (1) {
            printf("Client: ");
            fflush(stdout);
            fgets(buff, BUFFER_SIZE, stdin);
            buff[strcspn(buff, "\n")] = '\0';
            send(sockfd, buff, strlen(buff), 0);
            if (strcmp(buff, "CLOSE") == 0) break;
        }
    }

    close(sockfd);
    return 0;
}
