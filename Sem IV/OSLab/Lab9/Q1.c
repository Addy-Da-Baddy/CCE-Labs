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

void firstFit(Process processes[], int numProcesses, Block blocks[], int numBlocks) {
    for (int i = 0; i < numProcesses; i++) {
        for (int j = 0; j < numBlocks; j++) {
            if (blocks[j].freeSpace >= processes[i].size) {
                processes[i].allocatedBlock = blocks[j].id;
                blocks[j].freeSpace -= processes[i].size;
                break;
            }
        }
    }
}

void bestFit(Process processes[], int numProcesses, Block blocks[], int numBlocks) {
    for (int i = 0; i < numProcesses; i++) {
        int bestBlockIndex = -1;
        for (int j = 0; j < numBlocks; j++) {
            if (blocks[j].freeSpace >= processes[i].size) {
                if (bestBlockIndex == -1 || blocks[j].freeSpace < blocks[bestBlockIndex].freeSpace) {
                    bestBlockIndex = j;
                }
            }
        }
        if (bestBlockIndex != -1) {
            processes[i].allocatedBlock = blocks[bestBlockIndex].id;
            blocks[bestBlockIndex].freeSpace -= processes[i].size;
        }
    }
}

void worstFit(Process processes[], int numProcesses, Block blocks[], int numBlocks) {
    for (int i = 0; i < numProcesses; i++) {
        int bestBlockIndex = -1;
        for (int j = 0; j < numBlocks; j++) {
            if (blocks[j].freeSpace >= processes[i].size) {
                if (bestBlockIndex == -1 || blocks[j].freeSpace > blocks[bestBlockIndex].freeSpace) {
                    bestBlockIndex = j;
                }
            }
        }
        if (bestBlockIndex != -1) {
            processes[i].allocatedBlock = blocks[bestBlockIndex].id;
            blocks[bestBlockIndex].freeSpace -= processes[i].size;
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
    int numProcesses, numBlocks;

    printf("Enter the number of processes: ");
    scanf("%d", &numProcesses);

    Process *processes = (Process *)malloc(numProcesses * sizeof(Process));
    
    for (int i = 0; i < numProcesses; i++) {
        printf("Enter ID and size for process %d: ", i + 1);
        scanf("%d %d", &processes[i].id, &processes[i].size);
        processes[i].allocatedBlock = -1;
    }

    printf("Enter the number of blocks: ");
    scanf("%d", &numBlocks);

    Block *blocks = (Block *)malloc(numBlocks * sizeof(Block));
    
    // User input for block details
    for (int i = 0; i < numBlocks; i++) {
        printf("Enter ID, total space, and free space for block %d: ", i + 1);
        scanf("%d %d %d", &blocks[i].id, &blocks[i].totalSpace, &blocks[i].freeSpace);
    }

    // First Fit Allocation
    printf("\nFirst Fit Allocation:\n");
    firstFit(processes, numProcesses, blocks, numBlocks);
    printAllocation(processes, numProcesses);
    printBlockStatus(blocks, numBlocks);

    // Reset free space for blocks
    for (int i = 0; i < numBlocks; i++) {
        blocks[i].freeSpace = blocks[i].totalSpace;
    }

    // Best Fit Allocation
    printf("\nBest Fit Allocation:\n");
    bestFit(processes, numProcesses, blocks, numBlocks);
    printAllocation(processes, numProcesses);
    printBlockStatus(blocks, numBlocks);

    free(processes);
    free(blocks);

    return 0;
}
