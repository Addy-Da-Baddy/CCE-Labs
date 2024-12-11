#include <stdio.h>

//Function for insertion sort
void insertionSort(int arr[],int n){
    int i,j,key;
    for (i = 0; i < n; i++){
        key = arr[i];
        j = i - 1;
        while (j>=0 && arr[j]>key){
            arr[j+1] = arr[j];
            j = j - 1;
        }
        arr[j+1] = key;
    }
}


int main(){
    //defining array and vars
    int n,i;
    int MAX = 100;
    int arr[MAX] ;
    printf("Enter Size of Array: ");
    scanf("%d", &n);

    //Accepting array elements
    printf("Enter elements of the Array: \n");
    for (i = 0; i<n; i++){
        scanf("%d", &arr[i]);
    }

    //Passing into function
    insertionSort(arr, n);

    //printing sorted array
    printf("Sorted Array : \n");
    for (i = 0; i<n; i++){
        printf("%d ", arr[i]);
    }
        return 0;

}
