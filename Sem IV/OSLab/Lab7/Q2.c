#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <semaphore.h>
#include <unistd.h>

sem_t mutex;       
sem_t write_lock; 
int read_count = 0; 
void *reader(void *arg) {
    int reader_id = *(int *)arg;
    while (1) {
        sem_wait(&mutex); 
        read_count++;
        if (read_count == 1) {
            sem_wait(&write_lock); 
        }
        sem_post(&mutex);

        printf("Reader %d is reading\n", reader_id);
        sleep(1);  

        sem_wait(&mutex); 
        read_count--;
        if (read_count == 0) {
            sem_post(&write_lock); 
        }
        sem_post(&mutex); 

        sleep(1); 
    }
    pthread_exit(NULL);
}

void *writer(void *arg) {
    int writer_id = *(int *)arg;
    while (1) {
        sem_wait(&write_lock); 

        printf("Writer %d is writing\n", writer_id);
        sleep(2);  
        sem_post(&write_lock); 

        sleep(1);  
    }
    pthread_exit(NULL);
}

int main() {
    pthread_t readers[5], writers[2];
    int reader_ids[5] = {1, 2, 3, 4, 5};
    int writer_ids[2] = {1, 2};

    sem_init(&mutex, 0, 1);      
    sem_init(&write_lock, 0, 1);  

    for (int i = 0; i < 5; i++) {
        pthread_create(&readers[i], NULL, reader, (void *)&reader_ids[i]);
    }

    for (int i = 0; i < 2; i++) {
        pthread_create(&writers[i], NULL, writer, (void *)&writer_ids[i]);
    }

    for (int i = 0; i < 5; i++) {
        pthread_join(readers[i], NULL);
    }
    for (int i = 0; i < 2; i++) {
        pthread_join(writers[i], NULL);
    }

    sem_destroy(&mutex);
    sem_destroy(&write_lock);

    return 0;
}
