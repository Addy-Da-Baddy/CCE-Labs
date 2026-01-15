#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <netinet/in.h>

#define PORT 8080

void reorder_file(const char *fname) {
    FILE *fp = fopen(fname, "r+");
    char data[4096];
    int i, j;

    int n = fread(data, 1, sizeof(data) - 1, fp);
    data[n] = '\0';

    for (i = 0; i < n; i++) {
        for (j = i + 1; j < n; j++) {
            if (data[i] > data[j]) {
                char t = data[i];
                data[i] = data[j];
                data[j] = t;
            }
        }
    }

    rewind(fp);
    fwrite(data, 1, n, fp);
    ftruncate(fileno(fp), n);
    fclose(fp);
}

int main() {
    int sockfd;
    struct sockaddr_in server_addr, client_addr;
    socklen_t len = sizeof(client_addr);

    sockfd = socket(AF_INET, SOCK_DGRAM, 0);

    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(PORT);
    server_addr.sin_addr.s_addr = INADDR_ANY;

    bind(sockfd, (struct sockaddr*)&server_addr, sizeof(server_addr));

    printf("UDP Server waiting...\n");

    char filename[256];
    recvfrom(sockfd, filename, sizeof(filename), 0, (struct sockaddr*)&client_addr, &len);

    FILE *fp = fopen(filename, "r+");
    if (!fp) {
        char msg[] = "File not present";
        sendto(sockfd, msg, strlen(msg) + 1, 0, (struct sockaddr*)&client_addr, len);
        close(sockfd);
        return 0;
    }

    char ok[] = "OK";
    sendto(sockfd, ok, strlen(ok) + 1, 0, (struct sockaddr*)&client_addr, len);

    while (1) {
        int choice;
        recvfrom(sockfd, &choice, sizeof(choice), 0, (struct sockaddr*)&client_addr, &len);

        if (choice == 1) {
            char key[128], line[512];
            int count = 0;

            recvfrom(sockfd, key, sizeof(key), 0, (struct sockaddr*)&client_addr, &len);
            rewind(fp);

            while (fgets(line, sizeof(line), fp))
                if (strstr(line, key))
                    count++;

            if (count > 0) {
                char result[128];
                sprintf(result, "Found %d times", count);
                sendto(sockfd, result, strlen(result) + 1, 0, (struct sockaddr*)&client_addr, len);
            } else {
                char msg[] = "String not found";
                sendto(sockfd, msg, strlen(msg) + 1, 0, (struct sockaddr*)&client_addr, len);
            }
        }

        else if (choice == 2) {
            char s1[128], s2[128], data[4096];
            recvfrom(sockfd, s1, sizeof(s1), 0, (struct sockaddr*)&client_addr, &len);
            recvfrom(sockfd, s2, sizeof(s2), 0, (struct sockaddr*)&client_addr, &len);

            rewind(fp);
            int n = fread(data, 1, sizeof(data) - 1, fp);
            data[n] = '\0';

            char *pos = strstr(data, s1);
            if (!pos) {
                char msg[] = "String not found";
                sendto(sockfd, msg, strlen(msg) + 1, 0, (struct sockaddr*)&client_addr, len);
                continue;
            }

            char result[4096];
            strncpy(result, data, pos - data);
            result[pos - data] = '\0';
            strcat(result, s2);
            strcat(result, pos + strlen(s1));

            rewind(fp);
            fwrite(result, 1, strlen(result), fp);
            ftruncate(fileno(fp), strlen(result));

            char msg[] = "String replaced";
            sendto(sockfd, msg, strlen(msg) + 1, 0, (struct sockaddr*)&client_addr, len);
        }

        else if (choice == 3) {
            fclose(fp);
            reorder_file(filename);
            fp = fopen(filename, "r+");
            
            char msg[] = "File reordered";
            sendto(sockfd, msg, strlen(msg) + 1, 0, (struct sockaddr*)&client_addr, len);
        }

        else if (choice == 4) {
            break;
        }
    }

    fclose(fp);
    close(sockfd);
    return 0;
}
