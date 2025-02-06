#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

void ls_l() {
    execl("/bin/ls", "ls", "-l", (char *)NULL);
    perror("execl failed");  
}

void cp(const char *src, const char *dest) {
    execl("/bin/cp", "cp", src, dest, (char *)NULL);
    perror("execl failed");  
}

void wc(const char *filename) {
    execl("/usr/bin/wc", "wc", filename, (char *)NULL);
    perror("execl failed");  
}

int main(int argc, char *argv[]) {
    if (argc < 2) {
        fprintf(stderr, "Usage: %s <command> [arguments]\n", argv[0]);
        return 1;
    }

    if (strcmp(argv[1], "ls") == 0) {
        if (argc == 3 && strcmp(argv[2], "-l") == 0) {
            ls_l();
        } else {
            printf("Usage: %s ls -l\n", argv[0]);
        }
    } else if (strcmp(argv[1], "cp") == 0) {
        if (argc == 4) {
            cp(argv[2], argv[3]);
        } else {
            printf("Usage: %s cp <source> <destination>\n", argv[0]);
        }
    } else if (strcmp(argv[1], "wc") == 0) {
        if (argc == 3) {
            wc(argv[2]);
        } else {
            printf("Usage: %s wc <filename>\n", argv[0]);
        }
    } else {
        printf("Unknown command: %s\n", argv[1]);
    }

    return 0;
}
