#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>

int main() {
    pid_t pid = fork();

    if (pid == -1) {
        printf("Fork failed\n");
        return 1;
    }

    if (pid == 0) {
        printf("Child process: This is the child process\n");
        printf("Child PID: %d\n", getpid());  
        printf("Child PPID: %d\n", getppid());  
    } else {
        printf("Parent process: This is the parent process\n");
        printf("Parent PID: %d\n", getpid());  
        printf("Parent PPID: %d\n", getppid());
    }
    return 0;
}

