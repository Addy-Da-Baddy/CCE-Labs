#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>

#define BUFFER_SIZE 1024
#define PORT 8080

// Function to swap characters
void swap(char *x, char *y) {
    char temp = *x;
    *x = *y;
    *y = temp;
}

// Recursive function to generate permutations
void permute(char *str, int l, int r, char *result) {
    if (l == r) {
        strcat(result, str);
        strcat(result, "\n");
    } else {
        for (int i = l; i <= r; i++) {
            swap((str + l), (str + i));
            permute(str, l + 1, r, result);
            swap((str + l), (str + i)); // backtrack
        }
    }
}

int main() {
    int sockfd;
    struct sockaddr_in server_addr, client_addr;
    socklen_t addr_len;
    char buff[BUFFER_SIZE];

    // Create UDP socket
    sockfd = socket(AF_INET, SOCK_DGRAM, 0);
    if (sockfd == -1) {
        perror("Socket creation failed");
        exit(1);
    }

    printf("UDP Server Socket Created\n");

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

        printf("\nClient sent: %s\n", buff);

        if (strcmp(buff, "CLOSE") == 0)
            break;

        // Compute permutations
        char result[BUFFER_SIZE * 10]; // buffer for permutations
        memset(result, 0, sizeof(result));
        permute(buff, 0, strlen(buff) - 1, result);

        printf("Permutations:\n%s", result);

        // Send permutations back to client
        sendto(sockfd, result, strlen(result), 0,
               (struct sockaddr*)&client_addr, addr_len);
    }

    close(sockfd);
    return 0;
}
