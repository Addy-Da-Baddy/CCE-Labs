#include <stdio.h>
#include <stdlib.h>
#include <unistd.h> // For sleep()

void lruPageReplacement(int pages[], int numPages, int numFrames) {
    int *frames = (int *)malloc(numFrames * sizeof(int));
    int *time = (int *)malloc(numFrames * sizeof(int));
    int pageFaults = 0, pageHits = 0, clock = 0;

    for (int i = 0; i < numFrames; i++) {
        frames[i] = -1; // Initialize frames as empty (-1)
        time[i] = 0;    // Initialize time stamps
    }

    for (int i = 0; i < numPages; i++) {
        int found = 0;

        printf("\nProcessing page %d...\n", pages[i]);
        sleep(1); // Simulate processing delay

        // Check for page hit
        for (int j = 0; j < numFrames; j++) {
            if (frames[j] == pages[i]) {
                found = 1; // Page hit
                pageHits++;
                time[j] = clock++; // Update time for the hit frame
                break;
            }
        }

        if (!found) { // Page fault
            int lruIndex = 0, minTime = time[0];
            for (int j = 1; j < numFrames; j++) {
                if (time[j] < minTime) {
                    minTime = time[j];
                    lruIndex = j;
                }
            }
            frames[lruIndex] = pages[i];
            time[lruIndex] = clock++;
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
        sleep(1); // Additional delay
    }

    // Summary of LRU
    float faultRate = (float)pageFaults / numPages * 100;
    printf("\nLRU Summary:\n");
    printf("Total Page Faults: %d\n", pageFaults);
    printf("Total Page Hits: %d\n", pageHits);
    printf("Page Fault Rate: %.2f%%\n", faultRate);

    free(frames);
    free(time);
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

    printf("\n--- LRU Page Replacement ---\n");
    lruPageReplacement(pages, numPages, numFrames);

    free(pages);
    return 0;
}
