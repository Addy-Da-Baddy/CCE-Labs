#include <stdio.h>
#include <stdlib.h>

#define MAX 20

void createGraph(int graph[MAX][MAX], int vertices, int directed) {
    int edges, start, end;
    printf("Enter the number of edges: ");
    scanf("%d", &edges);

    for (int i = 0; i < edges; i++) {
        printf("Enter edge (start end): ");
        scanf("%d %d", &start, &end);
        graph[start][end] = 1;
        if (!directed) {
            graph[end][start] = 1;
        }
    }
}

void printGraph(int graph[MAX][MAX], int vertices) {
    printf("Adjacency Matrix:\n");
    for (int i = 0; i < vertices; i++) {
        for (int j = 0; j < vertices; j++) {
            printf("%d ", graph[i][j]);
        }
        printf("\n");
    }
}

int main() {
    int graph[MAX][MAX] = {0};
    int vertices, directed;

    printf("Enter the number of vertices: ");
    scanf("%d", &vertices);
    printf("Is the graph directed? (1 for Yes, 0 for No): ");
    scanf("%d", &directed);

    createGraph(graph, vertices, directed);
    printGraph(graph, vertices);

    return 0;
}

