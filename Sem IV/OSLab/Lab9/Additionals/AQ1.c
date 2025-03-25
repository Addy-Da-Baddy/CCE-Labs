#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int id;
    int size;
    int allocatedBlock;
} Process;

typedef struct {
    int id;
    int totalSpace;
    int freeSpace;
} Block;

void worstFit(Process processes[], int numProcesses, Block blocks[], int numBlocks) {
    for (int i = 0; i < numProcesses; i++) {
        int worstBlockIndex = -1;
        for (int j = 0; j < numBlocks; j++) {
            if (blocks[j].freeSpace >= processes[i].size) {
                if (worstBlockIndex == -1 || blocks[j].freeSpace > blocks[worstBlockIndex].freeSpace) {
                    worstBlockIndex = j;
                }
            }
        }
        if (worstBlockIndex != -1) {
            processes[i].allocatedBlock = blocks[worstBlockIndex].id;
            blocks[worstBlockIndex].freeSpace -= processes[i].size;
        }
    }
}

void printAllocation(Process processes[], int numProcesses) {
    printf("Process Allocation:\n");
    printf("Process ID\tSize\tAllocated Block\n");
    for (int i = 0; i < numProcesses; i++) {
        if (processes[i].allocatedBlock != -1) {
            printf("%d\t\t%d\t%d\n", processes[i].id, processes[i].size, processes[i].allocatedBlock);
        } else {
            printf("%d\t\t%d\tNot Allocated\n", processes[i].id, processes[i].size);
        }
    }
}

void printBlockStatus(Block blocks[], int numBlocks) {
    printf("\nBlock Status:\n");
    printf("Block ID\tTotal Space\tFree Space\n");
    for (int i = 0; i < numBlocks; i++) {
        printf("%d\t\t%d\t\t%d\n", blocks[i].id, blocks[i].totalSpace, blocks[i].freeSpace);
    }
}

int main() {
    int numProcesses = 4, numBlocks = 3;

    Process processes[] = {
        {1, 100, -1},
        {2, 150, -1},
        {3, 200, -1},
        {4, 50, -1}
    };

    Block blocks[] = {
        {1, 300, 300},
        {2, 150, 150},
        {3, 250, 250}
    };

    printf("Worst Fit Allocation:\n");
    worstFit(processes, numProcesses, blocks, numBlocks);
    printAllocation(processes, numProcesses);
    printBlockStatus(blocks, numBlocks);

    return 0;
}
