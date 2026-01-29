#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <sys/types.h>
#include <string.h>
#include <unistd.h>

#define BUFFER_SIZE 1024
#define PORT 8080

void print_prompt() {
    printf("\nChoose Option:\n");
    printf("1. REG <Registration Number>\n");
    printf("2. NAME <Student Name>\n");
    printf("3. SUB <Subject Code>\n");
    printf("Type CLOSE to exit\nClient: ");
    fflush(stdout);
}

int main() {
    int choice;
    printf("Select Protocol:\n1. TCP\n2. UDP\nEnter choice: ");
    scanf("%d", &choice);
    getchar();

    int sockfd, retval;
    struct sockaddr_in server_addr;
    socklen_t addr_len = sizeof(server_addr);
    char buff[BUFFER_SIZE];

    sockfd = socket(AF_INET, (choice == 1 ? SOCK_STREAM : SOCK_DGRAM), 0);
    if (sockfd == -1) {
        perror("Socket creation failed");
        exit(0);
    }

    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(PORT);
    server_addr.sin_addr.s_addr = htonl(INADDR_ANY);

    if (choice == 1) {
        retval = connect(sockfd, (struct sockaddr*)&server_addr, sizeof(server_addr));
        if (retval == -1) {
            perror("Connection failed");
            close(sockfd);
            exit(0);
        }
    }

    pid_t pid = fork();

    if (pid == 0) {
        printf("Client Child PID: %d\n", getpid());
        while (1) {
            memset(buff, 0, sizeof(buff));
            int recdbytes;
            if (choice == 1)
                recdbytes = recv(sockfd, buff, sizeof(buff), 0);
            else
                recdbytes = recvfrom(sockfd, buff, sizeof(buff), 0,
                                     (struct sockaddr*)&server_addr, &addr_len);
            if (recdbytes <= 0) break;
            printf("\nServer Response:\n%s\n", buff);
            if (strcmp(buff, "CLOSE") == 0) break;
            print_prompt();
        }
        exit(0);
    } else {
        printf("Client Parent PID: %d\n", getpid());
        while (1) {
            print_prompt();
            if (fgets(buff, BUFFER_SIZE, stdin) == NULL) continue;
            buff[strcspn(buff, "\n")] = '\0';
            if (choice == 1)
                send(sockfd, buff, strlen(buff), 0);
            else
                sendto(sockfd, buff, strlen(buff), 0,
                       (struct sockaddr*)&server_addr, addr_len);
            if (strcmp(buff, "CLOSE") == 0) break;
        }
    }

    close(sockfd);
    return 0;
}
