#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <netinet/in.h>

#define PORT 8080

int main() {
    int sockfd;
    struct sockaddr_in server_addr;
    socklen_t len = sizeof(server_addr);

    sockfd = socket(AF_INET, SOCK_DGRAM, 0);

    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(PORT);
    server_addr.sin_addr.s_addr = INADDR_ANY;

    char filename[256];
    printf("Enter filename: ");
    scanf("%s", filename);
    sendto(sockfd, filename, strlen(filename) + 1, 0, (struct sockaddr*)&server_addr, len);

    char reply[128];
    recvfrom(sockfd, reply, sizeof(reply), 0, NULL, NULL);

    if (strcmp(reply, "OK") != 0) {
        printf("%s\n", reply);
        close(sockfd);
        return 0;
    }

    while (1) {
        int ch;
        printf("\n1.Search 2.Replace 3.Reorder 4.Exit\n");
        scanf("%d", &ch);
        sendto(sockfd, &ch, sizeof(ch), 0, (struct sockaddr*)&server_addr, len);

        if (ch == 1) {
            char key[128];
            printf("Enter string: ");
            scanf("%s", key);
            sendto(sockfd, key, strlen(key) + 1, 0, (struct sockaddr*)&server_addr, len);

            recvfrom(sockfd, reply, sizeof(reply), 0, NULL, NULL);
            printf("%s\n", reply);
        }

        else if (ch == 2) {
            char s1[128], s2[128];
            printf("str1: ");
            scanf("%s", s1);
            printf("str2: ");
            scanf("%s", s2);
            sendto(sockfd, s1, strlen(s1) + 1, 0, (struct sockaddr*)&server_addr, len);
            sendto(sockfd, s2, strlen(s2) + 1, 0, (struct sockaddr*)&server_addr, len);

            recvfrom(sockfd, reply, sizeof(reply), 0, NULL, NULL);
            printf("%s\n", reply);
        }

        else if (ch == 3) {
            recvfrom(sockfd, reply, sizeof(reply), 0, NULL, NULL);
            printf("%s\n", reply);
        }

        else if (ch == 4)
            break;
    }

    close(sockfd);
    return 0;
}
