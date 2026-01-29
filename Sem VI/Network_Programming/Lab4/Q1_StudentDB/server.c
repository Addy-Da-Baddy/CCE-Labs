#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <sys/types.h>
#include <string.h>
#include <unistd.h>

#define BUFFER_SIZE 1024
#define PORT 8080

struct Student{
    char regno[20];
    char name[50];
    char addr[100];
    char dept[20];
    char sem[10];
    char sec[5];
    char courses[100];
    char subject[20];
    char marks[10];
}typedef Student;

Student studDB[] = {
    {
        "REG101",
        "Aarav Sharma",
        "Indiranagar, Bengaluru, Karnataka",
        "CSE",
        "5",
        "A",
        "Operating Systems, Computer Networks, DBMS",
        "CS501",
        "85"
    },
    {
        "REG102",
        "Rohan Verma",
        "Koramangala, Bengaluru, Karnataka",
        "ECE",
        "6",
        "B",
        "Digital Signal Processing, VLSI Design, Communication Systems",
        "EC601",
        "78"
    },
    {
        "REG103",
        "Ananya Iyer",
        "Adyar, Chennai, Tamil Nadu",
        "IT",
        "4",
        "A",
        "Data Structures, Algorithms, Software Engineering",
        "IT401",
        "88"
    },
    {
        "REG104",
        "Karthik Reddy",
        "Gachibowli, Hyderabad, Telangana",
        "CSE",
        "7",
        "C",
        "Machine Learning, Artificial Intelligence, Big Data",
        "CS701",
        "91"
    },
    {
        "REG105",
        "Priya Nair",
        "Kakkanad, Kochi, Kerala",
        "ECE",
        "5",
        "A",
        "Microprocessors, Embedded Systems, IoT",
        "EC502",
        "83"
    },
    {
        "REG106",
        "Vikram Singh",
        "Vaishali Nagar, Jaipur, Rajasthan",
        "ME",
        "6",
        "B",
        "Thermodynamics, Fluid Mechanics, Heat Transfer",
        "ME601",
        "76"
    },
    {
        "REG107",
        "Sneha Kulkarni",
        "Shivajinagar, Pune, Maharashtra",
        "CSE",
        "4",
        "B",
        "Discrete Mathematics, OOP, Computer Organization",
        "CS401",
        "89"
    },
    {
        "REG108",
        "Amit Patel",
        "Navrangpura, Ahmedabad, Gujarat",
        "CE",
        "7",
        "A",
        "Structural Analysis, RCC, Geotechnical Engineering",
        "CE701",
        "81"
    },
    {
        "REG109",
        "Neha Gupta",
        "Civil Lines, New Delhi",
        "EEE",
        "5",
        "C",
        "Power Systems, Electrical Machines, Control Systems",
        "EE503",
        "84"
    },
    {
        "REG110",
        "Suresh Kumar",
        "Ashok Nagar, Ranchi, Jharkhand",
        "ME",
        "4",
        "A",
        "Engineering Mechanics, Manufacturing Processes, CAD",
        "ME402",
        "79"
    }
};

int studCount = sizeof(studDB) / sizeof(studDB[0]);



void handle_request(char *buff, int sockfd,
                    struct sockaddr_in *client_addr,
                    socklen_t addr_len, int is_udp)
{
    char response[BUFFER_SIZE];
    int found = 0;

    memset(response, 0, sizeof(response));

    for (int i = 0; i < studCount; i++) {

        
        if (strncmp(buff, "REG", 3) == 0 &&
            strstr(buff, studDB[i].regno) != NULL) {

            snprintf(response, sizeof(response),
                     "Name: %s\nAddress: %s\nHandled by PID: %d",
                     studDB[i].name,
                     studDB[i].addr,
                     getpid());

            found = 1;
            break;
        }


        else if (strncmp(buff, "NAME", 4) == 0 &&
                 strstr(buff, studDB[i].name) != NULL) {

            snprintf(response, sizeof(response),
                     "Dept: %s\nSemester: %s\nSection: %s\nCourses: %s\nHandled by PID: %d",
                     studDB[i].dept,
                     studDB[i].sem,
                     studDB[i].sec,
                     studDB[i].courses,
                     getpid());

            found = 1;
            break;
        }

        
        else if (strncmp(buff, "SUB", 3) == 0 &&
                 strstr(buff, studDB[i].subject) != NULL) {

            snprintf(response, sizeof(response),
                     "Marks: %s\nHandled by PID: %d",
                     studDB[i].marks,
                     getpid());

            found = 1;
            break;
        }
    }

    if (!found) {
        snprintf(response, sizeof(response),
                 "Record not found\nHandled by PID: %d",
                 getpid());
    }

    if (is_udp) {
        sendto(sockfd, response, strlen(response), 0,
               (struct sockaddr *)client_addr, addr_len);
    } else {
        send(sockfd, response, strlen(response), 0);
    }
}

int main() {
    int choice;
    printf("Select Protocol:\n1. TCP\n2. UDP\nEnter choice: ");
    scanf("%d", &choice);

    int sockfd, newsockfd = -1, retval;
    struct sockaddr_in server_addr, client_addr;
    socklen_t addr_len = sizeof(client_addr);
    char buff[BUFFER_SIZE];

    sockfd = socket(AF_INET, (choice == 1 ? SOCK_STREAM : SOCK_DGRAM), 0);
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


    if (choice == 1) {
        retval = listen(sockfd, 5);
        if (retval == -1) {
            perror("Listen failed");
            close(sockfd);
            exit(0);
        }

        printf("TCP Server running...\n");

        newsockfd = accept(sockfd,
                           (struct sockaddr*)&client_addr, &addr_len);
        if (newsockfd == -1) {
            perror("Accept failed");
            close(sockfd);
            exit(0);
        }
    }
    else {
        printf("UDP Server running...\n");
    }

    while (1) {
        memset(buff, 0, sizeof(buff));
        int recdbytes;

        if (choice == 1)
            recdbytes = recv(newsockfd, buff, sizeof(buff), 0);
        else
            recdbytes = recvfrom(sockfd, buff, sizeof(buff), 0,
                                 (struct sockaddr*)&client_addr, &addr_len);

        if (recdbytes <= 0)
            break;

        if (strcmp(buff, "CLOSE") == 0)
            break;

        pid_t pid = fork();

        if (pid == 0) {   
            handle_request(buff,
                           (choice == 1 ? newsockfd : sockfd),
                           &client_addr,
                           addr_len,
                           (choice == 2));
            exit(0);
        }
        else {
            wait(NULL);  
        }
    }

    if (choice == 1)
        close(newsockfd);

    close(sockfd);
    return 0;
}
