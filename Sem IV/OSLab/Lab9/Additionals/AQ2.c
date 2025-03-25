#include <stdio.h>
#include <unistd.h> // For sleep()

int main() {
    int frames, pages, pageFaults = 0, pageHits = 0, current = 0;
    printf("Enter the number of frames: ");
    scanf("%d", &frames);
    printf("Enter the number of pages: ");
    scanf("%d", &pages);

    int pageReference[pages], frame[frames];
    for (int i = 0; i < frames; i++)
        frame[i] = -1; // Initialize frames as empty (-1)

    printf("Enter the page reference string: ");
    for (int i = 0; i < pages; i++)
        scanf("%d", &pageReference[i]);

    // FIFO Page Replacement Algorithm
    for (int i = 0; i < pages; i++) {
        int found = 0;

        // Simulate processing delay
        printf("\nProcessing page %d...\n", pageReference[i]);
        sleep(1); // 1-second delay to simulate "cool" wait

        // Check if page is already in frame (Page Hit)
        for (int j = 0; j < frames; j++) {
            if (frame[j] == pageReference[i]) {
                found = 1; // Page hit
                pageHits++;
                break;
            }
        }

        if (!found) { // Page Fault
            frame[current] = pageReference[i];
            current = (current + 1) % frames; // Move to the next frame in FIFO order
            pageFaults++;
        }

        // Display status for the current page
        printf("Page %d: %s\n", pageReference[i], found ? "Hit" : "Fault");
        printf("Frame status: ");
        for (int j = 0; j < frames; j++) {
            if (frame[j] != -1)
                printf("%d ", frame[j]);
            else
                printf("- ");
        }
        printf("\n");
        sleep(1); // Additional delay for coolness factor
    }

    // Calculate and display the page fault rate
    float faultRate = (float)pageFaults / pages * 100;
    printf("\nSimulation complete! Here’s the summary:\n");
    sleep(1); // Pause before summary
    printf("Total Page Faults: %d\n", pageFaults);
    printf("Total Page Hits: %d\n", pageHits);
    printf("Page Fault Rate: %.2f%%\n", faultRate);

    return 0;
}
