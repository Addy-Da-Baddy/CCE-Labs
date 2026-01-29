#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <sys/types.h>
#include <string.h>
#include <unistd.h>

#define BUFFER_SIZE 1024
#define PORT 8080
#define MAX_RECORDS 10

struct DNSRecord {
    char hostname[50];
    char ip[20];
};

struct DNSRecord dnsDB[MAX_RECORDS] = {
    {"example.com", "93.184.216.34"},
    {"google.com", "142.250.190.14"},
    {"microsoft.com", "40.113.200.201"}
};

int record_count = 3;

void create_record(char *hostname, char *ip) {
    if (record_count < MAX_RECORDS) {
        strcpy(dnsDB[record_count].hostname, hostname);
        strcpy(dnsDB[record_count].ip, ip);
        record_count++;
    }
}

void delete_record(char *hostname) {
    for (int i = 0; i < record_count; i++) {
        if (strcmp(dnsDB[i].hostname, hostname) == 0) {
            for (int j = i; j < record_count - 1; j++) {
                dnsDB[j] = dnsDB[j + 1];
            }
            record_count--;
            break;
        }
    }
}

char* resolve_hostname(char *hostname) {
    for (int i = 0; i < record_count; i++) {
        if (strcmp(dnsDB[i].hostname, hostname) == 0) {
            return dnsDB[i].ip;
        }
    }
    return NULL;
}

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

    while (1) {
        memset(buff, 0, sizeof(buff));
        int recdbytes = recv(newsockfd, buff, sizeof(buff), 0);
        if (recdbytes <= 0) break;

        printf("Client Request: %s\n", buff);

        if (strncmp(buff, "RESOLVE", 7) == 0) {
            char hostname[50];
            sscanf(buff, "RESOLVE %s", hostname);
            char *ip = resolve_hostname(hostname);
            if (ip)
                snprintf(buff, sizeof(buff), "IP Address: %s", ip);
            else
                snprintf(buff, sizeof(buff), "Domain not found");
        } else if (strncmp(buff, "CREATE", 6) == 0) {
            char hostname[50], ip[20];
            sscanf(buff, "CREATE %s %s", hostname, ip);
            create_record(hostname, ip);
            snprintf(buff, sizeof(buff), "Record created for %s -> %s", hostname, ip);
        } else if (strncmp(buff, "DELETE", 6) == 0) {
            char hostname[50];
            sscanf(buff, "DELETE %s", hostname);
            delete_record(hostname);
            snprintf(buff, sizeof(buff), "Record deleted for %s", hostname);
        } else if (strcmp(buff, "CLOSE") == 0) {
            break;
        } else {
            snprintf(buff, sizeof(buff), "Invalid command");
        }

        send(newsockfd, buff, strlen(buff), 0);
    }

    close(newsockfd);
    close(sockfd);
    return 0;
}
