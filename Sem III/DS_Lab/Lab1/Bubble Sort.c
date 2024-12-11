#include <stdio.h>

//Function for bubble sort
void bubbleSort(int arr[],int n){
    int temp,i,j;
    for (i = 0; i< n-1 ; i++){
        for (j = 0 ; j<n-1-i; j++){
            if (arr[j]>arr[j+1]){
                temp = arr[j];
                arr[j] = arr[j+1];
                arr[j+1] = temp;
            }
        }
    }
}


int main(){
    //defining array and vars
    int n,i;
    int MAX = 100;
    int arr[100] ;
    printf("Enter Size of Array: ");
    scanf("%d", &n);

    //Accepting array elements
    printf("Enter elements of the Array: \n");
    for (i = 0; i<n; i++){
        scanf("%d", &arr[i]);
    }

    //Passing into function
    bubbleSort(arr, n);

    //printing sorted array
    printf("Sorted Array : \n");
    for (i = 0; i<n; i++){
        printf("%d ", arr[i]);
    }
        return 0;

}
