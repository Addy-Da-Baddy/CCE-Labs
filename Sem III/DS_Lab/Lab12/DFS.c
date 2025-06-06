#include <stdio.h>
#include <stdlib.h>

#define MAX 20

// Node structure for adjacency list
struct Node {
    int vertex;
    struct Node* next;
};

// Graph structure
struct Graph {
    struct Node* adjLists[MAX];
    int vertices;
};

// Function to create a new node
struct Node* createNode(int vertex) {
    struct Node* newNode = malloc(sizeof(struct Node));
    newNode->vertex = vertex;
    newNode->next = NULL;
    return newNode;
}

// Function to create a graph
struct Graph createGraph(int vertices) {
    struct Graph graph;
    graph.vertices = vertices;

    for (int i = 0; i < vertices; i++) {
        graph.adjLists[i] = NULL; // Initialize each adjacency list as empty
    }
    return graph;
}

// Function to add an edge
void addEdge(struct Graph* graph, int start, int end, int directed) {
    struct Node* newNode = createNode(end);
    newNode->next = graph->adjLists[start];
    graph->adjLists[start] = newNode;

    if (!directed) {
        newNode = createNode(start);
        newNode->next = graph->adjLists[end];
        graph->adjLists[end] = newNode;
    }
}

// DFS function
void dfs(struct Graph* graph, int vertex, int visited[]) {
    visited[vertex] = 1; // Mark the vertex as visited
    printf("%d ", vertex); // Print the visited vertex

    // Visit all adjacent vertices
    struct Node* temp = graph->adjLists[vertex];
    while (temp) {
        int adjVertex = temp->vertex;
        if (!visited[adjVertex]) {
            dfs(graph, adjVertex, visited);
        }
        temp = temp->next;
    }
}

// Function to print the graph
void printGraph(struct Graph* graph) {
    for (int i = 0; i < graph->vertices; i++) {
        struct Node* temp = graph->adjLists[i];
        printf("Vertex %d: ", i);
        while (temp) {
            printf("-> %d ", temp->vertex);
            temp = temp->next;
        }
        printf("\n");
    }
}

// Main function
int main() {
    int vertices, directed;

    printf("Enter the number of vertices: ");
    scanf("%d", &vertices);
    printf("Is the graph directed? (1 for Yes, 0 for No): ");
    scanf("%d", &directed);

    struct Graph graph = createGraph(vertices);

    int edges, start, end;
    printf("Enter the number of edges: ");
    scanf("%d", &edges);

    for (int i = 0; i < edges; i++) {
        printf("Enter edge (start end): ");
        scanf("%d %d", &start, &end);
        addEdge(&graph, start, end, directed);
    }

    printGraph(&graph);

    int visited[MAX] = {0}; // Array to track visited vertices
    printf("Enter the starting vertex for DFS: ");
    scanf("%d", &start);

    printf("DFS Traversal: ");
    dfs(&graph, start, visited);
    printf("\n");

    return 0;
}
