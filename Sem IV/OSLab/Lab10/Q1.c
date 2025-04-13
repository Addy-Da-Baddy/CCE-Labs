#include <stdio.h>
#include <stdlib.h>
#include <unistd.h> 

void fifoPageReplacement(int pages[], int numPages, int numFrames) {
    int *frames = (int *)malloc(numFrames * sizeof(int));
    int pageFaults = 0, pageHits = 0, current = 0, filled = 0;

    for (int i = 0; i < numFrames; i++) {
        frames[i] = -1;
    }

    for (int i = 0; i < numPages; i++) {
        int found = 0;

        printf("\nProcessing page %d...\n", pages[i]);
        sleep(1);

        for (int j = 0; j < numFrames; j++) {
            if (frames[j] == pages[i]) {
                found = 1;
                pageHits++;
                break;
            }
        }

        if (!found) {
            if (filled < numFrames) {
                frames[filled++] = pages[i];
            } else {
                frames[current] = pages[i];  
                current = (current + 1) % numFrames;
            }
            pageFaults++;
        }

        printf("Page %d: %s\n", pages[i], found ? "Hit" : "Fault");
        printf("Frame status: ");
        for (int j = 0; j < numFrames; j++) {
            frames[j] != -1 ? printf("%d ", frames[j]) : printf("- ");
        }
        printf("\n");
        sleep(1);
    }

    float faultRate = (float)pageFaults / numPages * 100;
    printf("\nFIFO Summary:\n");
    printf("Total Page Faults: %d\n", pageFaults);
    printf("Total Page Hits: %d\n", pageHits);
    printf("Page Fault Rate: %.2f%%\n", faultRate);
    free(frames);
}

void optimalPageReplacement(int pages[], int numPages, int numFrames) {
    int *frames = (int *)malloc(numFrames * sizeof(int));
    int pageFaults = 0, pageHits = 0, filled = 0;

    for (int i = 0; i < numFrames; i++) {
        frames[i] = -1;
    }

    for (int i = 0; i < numPages; i++) {
        int found = 0;

        printf("\nProcessing page %d...\n", pages[i]);
        sleep(1);

        for (int j = 0; j < numFrames; j++) {
            if (frames[j] == pages[i]) {
                found = 1;
                pageHits++;
                break;
            }
        }

        if (!found) {
            if (filled < numFrames) {
                frames[filled++] = pages[i];
            } else {
                int replaceIndex = -1, farthest = -1;

                for (int j = 0; j < numFrames; j++) {
                    int nextUse = -1;
                    for (int k = i + 1; k < numPages; k++) {
                        if (frames[j] == pages[k]) {
                            nextUse = k;
                            break;
                        }
                    }

                    if (nextUse == -1) {
                        replaceIndex = j;
                        break;
                    } else if (nextUse > farthest) {
                        farthest = nextUse;
                        replaceIndex = j;
                    }
                }

                frames[replaceIndex] = pages[i];
            }
            pageFaults++;
        }

        // Display frame state
        printf("Page %d: %s\n", pages[i], found ? "Hit" : "Fault");
        printf("Frame status: ");
        for (int j = 0; j < numFrames; j++) {
            frames[j] != -1 ? printf("%d ", frames[j]) : printf("- ");
        }
        printf("\n");
        sleep(1);
    }

    float faultRate = (float)pageFaults / numPages * 100;
    printf("\nOptimal Summary:\n");
    printf("Total Page Faults: %d\n", pageFaults);
    printf("Total Page Hits: %d\n", pageHits);
    printf("Page Fault Rate: %.2f%%\n", faultRate);
    free(frames);
}

int main() {
    int numPages, numFrames;

    printf("Enter the number of pages: ");
    scanf("%d", &numPages);

    int *pages = (int *)malloc(numPages * sizeof(int));
    printf("Enter the page reference string:\n");
    for (int i = 0; i < numPages; i++) {
        scanf("%d", &pages[i]);
    }

    printf("Enter the number of frames: ");
    scanf("%d", &numFrames);

    printf("\nFIFO Page Replacement\n");
    fifoPageReplacement(pages, numPages, numFrames);

    printf("\nOptimal Page Replacement\n");
    optimalPageReplacement(pages, numPages, numFrames);

    free(pages);
    return 0;
}
