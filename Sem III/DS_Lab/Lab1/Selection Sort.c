#include <stdio.h>

//Function for selection sort
void selectionSort(int arr[],int n){
    int min_indx,i,j,temp;
    for (i = 0; i < n; i++){
        min_indx = i;
        for (j = i + 1; j < n ; j++){
            if (arr[j] < arr[min_indx]){
                min_indx = j;
            }
        }
        if (min_indx!=i){
            temp = arr[i];
            arr[i] = arr[min_indx];
            arr[min_indx] = temp;
        }
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
    selectionSort(arr, n);

    //printing sorted array
    printf("Sorted Array : \n");
    for (i = 0; i<n; i++){
        printf("%d ", arr[i]);
    }
    return 0;
}
