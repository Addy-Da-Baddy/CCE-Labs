#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <netinet/in.h>

#define PORT 8080

int main() {
    int sockfd;
    struct sockaddr_in server_addr;

    sockfd = socket(AF_INET, SOCK_STREAM, 0);

    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(PORT);
    server_addr.sin_addr.s_addr = INADDR_ANY;

    connect(sockfd, (struct sockaddr*)&server_addr, sizeof(server_addr));

    char filename[256];
    printf("Enter filename: ");
    scanf("%s", filename);
    send(sockfd, filename, strlen(filename) + 1, 0);

    char reply[128];
    recv(sockfd, reply, sizeof(reply), 0);

    if (strcmp(reply, "OK") != 0) {
        printf("%s\n", reply);
        close(sockfd);
        return 0;
    }

    while (1) {
        int ch;
        printf("\n1.Search 2.Replace 3.Reorder 4.Exit\n");
        scanf("%d", &ch);
        send(sockfd, &ch, sizeof(ch), 0);

        if (ch == 1) {
            char key[128];
            printf("Enter string: ");
            scanf("%s", key);
            send(sockfd, key, strlen(key) + 1, 0);

            recv(sockfd, reply, sizeof(reply), 0);
            printf("%s\n", reply);
        }

        else if (ch == 2) {
            char s1[128], s2[128];
            printf("str1: ");
            scanf("%s", s1);
            printf("str2: ");
            scanf("%s", s2);
            send(sockfd, s1, strlen(s1) + 1, 0);
            send(sockfd, s2, strlen(s2) + 1, 0);

            recv(sockfd, reply, sizeof(reply), 0);
            printf("%s\n", reply);
        }

        else if (ch == 3) {
            recv(sockfd, reply, sizeof(reply), 0);
            printf("%s\n", reply);
        }

        else if (ch == 4)
            break;
    }

    close(sockfd);
    return 0;
}
