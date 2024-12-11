#include <stdio.h>
int main(){
    //defining array and vars
    int n,key,i;
    int MAX = 100;
    int arr[MAX] ;
    printf("Enter Size of Array: ");
    scanf("%d", &n);

    //Accepting array elements
    printf("Enter elements of the Array in sorted order: \n");
    for (i = 0; i<n; i++){
        scanf("%d", &arr[i]);
    }
    printf ("Enter the element to be searched: ");
    scanf("%d" , &key);

    //Binary Search
    int mid;
    int high = n-1;
    int low = 0;
    while (low<=high){
        mid = (high+low)/2 ;
        if (arr[mid]==key){
            printf ("Entered Element has been found at index: %d", mid);
                return 0;
        }
        if (arr[mid]>key){
            high = mid - 1;
        }
        if (arr[mid]<key){
            low = mid + 1;
        }
    }
    printf("Element not found in array");
    return 0;
}
