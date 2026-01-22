#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <sys/types.h>
#include <arpa/inet.h>
#include <ctype.h>

#define BUFFER_SIZE 1024
#define PORT 6868

void sort_numbers(char *input, char *output) {
    char nums[BUFFER_SIZE];
    int n = 0;
    for (int i = 0; input[i]; i++) {
        if (isdigit(input[i])) nums[n++] = input[i];
    }
    nums[n] = '\0';
    for (int i = 0; i < n-1; i++) {
        for (int j = i+1; j < n; j++) {
            if (nums[i] > nums[j]) {
                char temp = nums[i];
                nums[i] = nums[j];
                nums[j] = temp;
            }
        }
    }
    strcpy(output, nums);
}

void sort_chars(char *input, char *output) {
    char chars[BUFFER_SIZE];
    int n = 0;
    for (int i = 0; input[i]; i++) {
        if (isalpha(input[i])) chars[n++] = input[i];
    }
    chars[n] = '\0';
    for (int i = 0; i < n-1; i++) {
        for (int j = i+1; j < n; j++) {
            if (chars[i] < chars[j]) {
                char temp = chars[i];
                chars[i] = chars[j];
                chars[j] = temp;
            }
        }
    }
    strcpy(output, chars);
}

int main() {
    int sockfd, newsockfd;
    struct sockaddr_in server_addr, client_addr;
    socklen_t addr_len;
    char buff[BUFFER_SIZE];
    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd == -1) exit(1);
    printf("Socket created\n");
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(PORT);
    server_addr.sin_addr.s_addr = htonl(INADDR_ANY);
    if (bind(sockfd, (struct sockaddr*)&server_addr, sizeof(server_addr)) == -1) exit(1);
    printf("Socket binded\n");
    if (listen(sockfd, 1) == -1) exit(1);
    printf("Listening on port %d\n", PORT);
    addr_len = sizeof(client_addr);
    newsockfd = accept(sockfd, (struct sockaddr*)&client_addr, &addr_len);
    if (newsockfd == -1) exit(1);
    printf("Client connected\n");
    while (1) {
        memset(buff, 0, sizeof(buff));
        int recdbytes = recv(newsockfd, buff, sizeof(buff), 0);
        if (recdbytes <= 0) continue;
        if (strcmp(buff, "CLOSE_MAGIC_X32") == 0) {
            printf("Closing connection\n");
            close(newsockfd);
            close(sockfd);
            break;
        }
        pid_t pid = fork();
        if (pid == 0) {
            char num_result[BUFFER_SIZE];
            sort_numbers(buff, num_result);
            char msg[BUFFER_SIZE];
            sprintf(msg, "Child (PID %d): %s", getpid(), num_result);
            send(newsockfd, msg, strlen(msg), 0);
            exit(0);
        } else {
            char char_result[BUFFER_SIZE];
            sort_chars(buff, char_result);
            char msg[BUFFER_SIZE];
            sprintf(msg, "Parent (PID %d): %s", getpid(), char_result);
            send(newsockfd, msg, strlen(msg), 0);
        }
    }
    return 0;
}
