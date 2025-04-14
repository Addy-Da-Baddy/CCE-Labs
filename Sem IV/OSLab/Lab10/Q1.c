#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

// Check if page is already in frames
bool isInFrames(int page, int frames[], int n) {
    for (int i = 0; i < n; i++) {
        if (frames[i] == page)
            return true;
    }
    return false;
}

// Display current frames
void showFrames(int frames[], int n) {
    printf("Frames: ");
    for (int i = 0; i < n; i++) {
        if (frames[i] == -1)
            printf("[ ] ");
        else
            printf("[%d] ", frames[i]);
    }
    printf("\n");
}

// ---------- LRU ----------
void LRU(int pages[], int total, int frameCount) {
    int frames[frameCount], lastUsed[frameCount], faults = 0;
    for (int i = 0; i < frameCount; i++) {
        frames[i] = -1;
        lastUsed[i] = 0;
    }

    printf("\n--- LRU Page Replacement ---\n");
    for (int t = 0; t < total; t++) {
        int page = pages[t];
        printf("Page: %d\n", page);

        if (isInFrames(page, frames, frameCount)) {
            printf("Hit!\n");
            for (int i = 0; i < frameCount; i++)
                if (frames[i] == page)
                    lastUsed[i] = t;
        } else {
            printf("Miss!\n");
            faults++;

            int replace = 0;
            for (int i = 1; i < frameCount; i++)
                if (lastUsed[i] < lastUsed[replace])
                    replace = i;

            if (frames[replace] == -1)
                for (int i = 0; i < frameCount; i++)
                    if (frames[i] == -1) {
                        replace = i;
                        break;
                    }

            frames[replace] = page;
            lastUsed[replace] = t;
        }
        showFrames(frames, frameCount);
    }

    printf("Total Page Faults (LRU): %d\n", faults);
    printf("Fault Rate: %.2f%%\n", (float)faults / total * 100);
}

// ---------- Optimal ----------
int predict(int pages[], int total, int frames[], int frameCount, int current) {
    int farthest = current, index = -1;

    for (int i = 0; i < frameCount; i++) {
        int j;
        for (j = current + 1; j < total; j++)
            if (frames[i] == pages[j])
                break;

        if (j == total)
            return i; // Never used again

        if (j > farthest) {
            farthest = j;
            index = i;
        }
    }
    return (index == -1) ? 0 : index;
}

void Optimal(int pages[], int total, int frameCount) {
    int frames[frameCount], faults = 0;
    for (int i = 0; i < frameCount; i++) frames[i] = -1;

    printf("\n--- Optimal Page Replacement ---\n");
    for (int t = 0; t < total; t++) {
        int page = pages[t];
        printf("Page: %d\n", page);

        if (isInFrames(page, frames, frameCount)) {
            printf("Hit!\n");
        } else {
            printf("Miss!\n");
            faults++;

            int replace = -1;
            for (int i = 0; i < frameCount; i++) {
                if (frames[i] == -1) {
                    replace = i;
                    break;
                }
            }

            if (replace == -1)
                replace = predict(pages, total, frames, frameCount, t);

            frames[replace] = page;
        }
        showFrames(frames, frameCount);
    }

    printf("Total Page Faults (Optimal): %d\n", faults);
    printf("Fault Rate: %.2f%%\n", (float)faults / total * 100);
}

// ---------- FIFO ----------
void FIFO(int pages[], int total, int frameCount) {
    int frames[frameCount], index = 0, faults = 0;
    for (int i = 0; i < frameCount; i++) frames[i] = -1;

    printf("\n--- FIFO Page Replacement ---\n");
    for (int t = 0; t < total; t++) {
        int page = pages[t];
        printf("Page: %d\n", page);

        if (isInFrames(page, frames, frameCount)) {
            printf("Hit!\n");
        } else {
            printf("Miss!\n");
            faults++;
            frames[index] = page;
            index = (index + 1) % frameCount;
        }
        showFrames(frames, frameCount);
    }

    printf("Total Page Faults (FIFO): %d\n", faults);
    printf("Fault Rate: %.2f%%\n", (float)faults / total * 100);
}

// ---------- MAIN ----------
int main() {
    int pages[] = {1, 2, 3, 4, 1, 2, 5, 1, 2, 3};
    int totalPages = sizeof(pages) / sizeof(pages[0]);
    int frameCount = 3;

    LRU(pages, totalPages, frameCount);
    Optimal(pages, totalPages, frameCount);
    FIFO(pages, totalPages, frameCount);

    return 0;
}
