#include <stdio.h>
int main(){
    //defining array and vars
    int n,key,i;
    int MAX = 100;
    int arr[MAX] ;
    printf("Enter Size of Array: ");
    scanf("%d", &n);

    //Accepting array elements
    printf("Enter elements of the Array: \n");
    for (i = 0; i<n; i++){
        scanf("%d", &arr[i]);
    }
    printf ("Enter the element to be searched: ");
    scanf("%d" , &key);

    //Linear Search
    for (i = 0 ; i<n; i++){
        if (arr[i]==key){
                printf ("Entered Element has been found at index: %d", i);
                return 0;
        }
    }

    printf("Element not found in array");
    return 0;
}
