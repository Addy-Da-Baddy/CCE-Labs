#include <stdio.h>
#include <stdbool.h>
#include <string.h>
#define MAX 100

typedef struct PatientDetails{
    int hospitalNo;
    char name[MAX];
    char age[MAX];
    char address[MAX];
}PD;

void getDetails(PD* pd){
    printf("Enter hospitalNo, Name,  Age and Address: ");
    scanf("%d",&(pd->hospitalNo));
    gets(pd->name);
    gets(pd->age);
    gets(pd->address);
}

typedef struct PatientQueue{
    int front;
    int rear;
    PD details[MAX];
}PQ;

void initPQ(PQ* pq){
    pq->front = -1;
    pq->rear = -1;
}

bool isFull(PQ *q) {
    return ((q->rear + 1) % MAX == q->front);
}

bool isEmpty(PQ *q) {
    return (q->front == -1);
}

void enq(PQ *q, PD pd) {
    if (isFull(q)) {
        printf("Queue overflow!\n");
    } else {
        if (isEmpty(q)) {
            q->front = 0;
        }
        q->rear = (q->rear + 1) % MAX;
        q->details[q->rear] = pd;
    }
}

PD deq(PQ *q) {
    if (isEmpty(q)) {
        printf("Queue underflow!\n");
        return ;
    } else {
        PD detail = q->details[q->front];
        if (q->front == q->rear) {
            initPQ(q);
        } else {
            q->front = (q->front + 1) % MAX;
        }
        return detail;
    }
}


int main(){
    PQ queue;
    initPQ(&queue);
    PD pd;
    int i = 0;
    for (i = 0; i<3; i++){
    getDetails(&pd);
    enq(&queue,pd);
    }
    return 0;
    printf("Appointments will be in following order: \n");
    while (!isEmpty(&queue)){
    }
}
