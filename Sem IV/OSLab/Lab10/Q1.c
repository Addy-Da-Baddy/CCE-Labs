#include <stdio.h>
#include <stdlib.h>
#include <unistd.h> // For sleep()

// Function for FIFO Page Replacement
void fifoPageReplacement(int pages[], int numPages, int numFrames) {
    int *frames = (int *)malloc(numFrames * sizeof(int));
    int pageFaults = 0, pageHits = 0, current = 0;

    for (int i = 0; i < numFrames; i++) {
        frames[i] = -1; // Initialize frames as empty (-1)
    }

    for (int i = 0; i < numPages; i++) {
        int found = 0;

        // Simulate processing delay for user experience
        printf("\nProcessing page %d...\n", pages[i]);
        sleep(1); // 1-second delay to simulate "working" feel

        // Check for page hit
        for (int j = 0; j < numFrames; j++) {
            if (frames[j] == pages[i]) {
                found = 1; // Page hit
                pageHits++;
                break;
            }
        }

        if (!found) { // Page fault
            frames[current] = pages[i];
            current = (current + 1) % numFrames; // FIFO replacement
            pageFaults++;
        }

        // Display frame status
        printf("Page %d: %s\n", pages[i], found ? "Hit" : "Fault");
        printf("Frame status: ");
        for (int j = 0; j < numFrames; j++) {
            if (frames[j] != -1) {
                printf("%d ", frames[j]);
            } else {
                printf("- ");
            }
        }
        printf("\n");
        sleep(1); // Additional coolness delay
    }

    // Summary of FIFO
    float faultRate = (float)pageFaults / numPages * 100;
    printf("\nFIFO Summary:\n");
    printf("Total Page Faults: %d\n", pageFaults);
    printf("Total Page Hits: %d\n", pageHits);
    printf("Page Fault Rate: %.2f%%\n", faultRate);
    free(frames);
}

// Function for Optimal Page Replacement
void optimalPageReplacement(int pages[], int numPages, int numFrames) {
    int *frames = (int *)malloc(numFrames * sizeof(int));
    int pageFaults = 0, pageHits = 0;

    for (int i = 0; i < numFrames; i++) {
        frames[i] = -1; // Initialize frames as empty (-1)
    }

    for (int i = 0; i < numPages; i++) {
        int found = 0;

        // Simulate processing delay for user experience
        printf("\nProcessing page %d...\n", pages[i]);
        sleep(1); // 1-second delay to simulate "working" feel

        // Check for page hit
        for (int j = 0; j < numFrames; j++) {
            if (frames[j] == pages[i]) {
                found = 1; // Page hit
                pageHits++;
                break;
            }
        }

        if (!found) { // Page fault
            int replaceIndex = -1, farthest = -1;
            for (int j = 0; j < numFrames; j++) {
                int futureUse = -1;
                for (int k = i + 1; k < numPages; k++) {
                    if (frames[j] == pages[k]) {
                        futureUse = k;
                        break;
                    }
                }
                if (futureUse == -1) {
                    replaceIndex = j; // Not used in future
                    break;
                } else if (futureUse > farthest) {
                    farthest = futureUse;
                    replaceIndex = j;
                }
            }
            frames[replaceIndex] = pages[i];
            pageFaults++;
        }

        // Display frame status
        printf("Page %d: %s\n", pages[i], found ? "Hit" : "Fault");
        printf("Frame status: ");
        for (int j = 0; j < numFrames; j++) {
            if (frames[j] != -1) {
                printf("%d ", frames[j]);
            } else {
                printf("- ");
            }
        }
        printf("\n");
        sleep(1); // Additional coolness delay
    }

    // Summary of Optimal
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

    printf("\n--- FIFO Page Replacement ---\n");
    fifoPageReplacement(pages, numPages, numFrames);

    printf("\n--- Optimal Page Replacement ---\n");
    optimalPageReplacement(pages, numPages, numFrames);

    free(pages);
    return 0;
}
