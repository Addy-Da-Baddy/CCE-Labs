#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define MAX 100

int fcfs(int n, int req[], int head){
    int total_movement = 0;
    printf("FCFS ORDER: ");
    for (int i = 0; i < n; i++){
        int move = abs(req[i]-head);
        head = req[i];
        total_movement+=move;
        printf("%d ", req[i]);
    }
    printf("\nTotal Movement: %d " , total_movement);
    printf("\n");
}

int sstf(int n, int req[], int head){
    int total_movement = 0;
    int visited[MAX] = {0};
        printf("SSTF ORDER: ");

    for (int i = 0; i < n; i++){
        int min = 9999;
        int sst = -1;
        for (int j = 0; j < n; j++){
            if (!visited[j] && abs(head-req[j]) < min){
                sst = j;
                min = abs(head-req[j]);
            }
        }
        total_movement += min;
        visited[sst] = 1;
        head = req[sst];
        printf("%d ", req[sst]);
    }
    printf("\nTotal Movement: %d " , total_movement);
    printf("\n");
}

int SCAN(int n, int req[], int head){
    int MAX_CYL = 100;
        int visited[MAX] = {0};

    int total_movement = 0;
        printf("SCAN ORDER: ");

    for (int i = head; i < MAX_CYL; i++){
        for (int j = 0; j < n; j++){
            if (!visited[j] && req[j]==i){
                visited[j] = 1;
                total_movement += abs(head - req[j]);
                head = req[j];
                printf("%d " , head);
            }
        }
    }
    
    if (head!=MAX_CYL){
        total_movement += abs(MAX_CYL-head);
        head = MAX_CYL;
    }
    
        for (int i = MAX_CYL; i > 0; i--){
            for (int j = 0; j < n; j++){
            if (!visited[j] && req[j]==i){
                visited[j] = 1;
                total_movement += abs(head - req[j]);
                head = req[j];
                printf("%d " , head);
            }
        }
    }
    
    printf("\nTotal Movement: %d " , total_movement);
    printf("\n");
}


int CSCAN(int n, int req[], int head){
    int MAX_CYL = 100;
        int visited[MAX] = {0};

    int total_movement = 0;
        printf("CSCAN ORDER: ");

    for (int i = head; i < MAX_CYL; i++){
        for (int j = 0; j < n; j++){
            if (!visited[j] && req[j]==i){
                visited[j] = 1;
                total_movement += abs(head - req[j]);
                head = req[j];
                printf("%d " , head);
            }
        }
    }
         head = 0;
    
        for (int i = head; i < MAX_CYL; i++){
            for (int j = 0; j < n; j++){
            if (!visited[j] && req[j]==i){
                visited[j] = 1;
                total_movement += abs(head - req[j]);
                head = req[j];
                printf("%d " , head);
            }
        }
    }
    
    printf("\nTotal Movement: %d " , total_movement);
    printf("\n");
}


int LOOK(int n, int req[], int head){
    int MAX_CYL = 100;
        int visited[MAX] = {0};

    int total_movement = 0;
    printf("LOOK ORDER: ");
    int last_done = -1;
    for (int i = head; i < MAX_CYL; i++){
        for (int j = 0; j < n; j++){
            if (!visited[j] && req[j]==i){
                visited[j] = 1;
                total_movement += abs(head - req[j]);
                head = req[j];
                printf("%d " , head);
                last_done = req[j];
            }
        }
    }
    
    head = last_done;
    
        for (int i = head; i > 0; i--){
            for (int j = 0; j < n; j++){
            if (!visited[j] && req[j]==i){
                visited[j] = 1;
                total_movement += abs(head - req[j]);
                head = req[j];
                printf("%d " , head);
            }
        }
    }
    
    printf("\nTotal Movement: %d " , total_movement);
    printf("\n");
}


int CLOOK(int n, int req[], int head){
    int MAX_CYL = 100;
        int visited[MAX] = {0};

    int total_movement = 0;
    printf("CLOOK ORDER: ");
    int last_done = -1;
    for (int i = head; i < MAX_CYL; i++){
        for (int j = 0; j < n; j++){
            if (!visited[j] && req[j]==i){
                visited[j] = 1;
                total_movement += abs(head - req[j]);
                head = req[j];
                printf("%d " , head);
            }
        }
    }
    
        for (int i = 0; i < MAX_CYL; i++){
            for (int j = 0; j < n; j++){
            if (!visited[j] && req[j]==i){
                visited[j] = 1;
                total_movement += abs(head - req[j]);
                head = req[j];
                printf("%d " , head);
            }
        }
    }
    
    printf("\nTotal Movement: %d " , total_movement);
    printf("\n");
}


int main(){
    int n = 5;
    int req[5] = {40,65,32,11,43};
 
    int head = 35;
    fcfs(n,req,head);
    sstf(n,req,head);
    SCAN(n,req,head);
    CSCAN(n,req,head);
    LOOK(n,req,head);
    CLOOK(n,req,head);



}
