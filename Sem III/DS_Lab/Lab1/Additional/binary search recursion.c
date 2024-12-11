#include <stdio.h>

int binarySearch(int arr[], int key, int high, int low){
    if (low<=high){
        int mid = (high+low)/2;
        if (arr[mid]==key)
            return mid;
        else if (arr[mid]>key)
            return binarySearch(arr,key,mid-1,low);
        else if (arr[mid]<key)
            return binarySearch(arr,key,high,mid+1);
    }
    return -1;
}




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

    int indx = binarySearch(arr,key,n-1,0);
    if (indx == -1){
        printf("Not found ");
        return 0;
    }
    else {
        printf ("Entered Element has been found at index: %d", indx);
    }
    return 0;
}
