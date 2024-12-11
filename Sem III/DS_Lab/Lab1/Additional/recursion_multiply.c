#include <stdio.h>
int mult(int n1, int n2){
    if (n2==0){
        return 0;
    }
    if (n2==1){
        return n1;
    }
    return n1 + mult(n1,n2-1);
}

int main(){
    int n1,n2;
    printf("Enter the numbers to be multiplied: ");
    scanf ("%d%d",&n1,&n2);
    if ((n1>0 && n2>0)){
    printf("%d x %d = %d \n",n1,n2, mult(n1,n2));
    return 0;
    }
    else if ((n1<0 && n2<0)){
    printf("%d x %d = %d \n",n1,n2, mult(-n1,-n2));
    return 0;
    }
    else if (n2<0) {
        printf("%d x %d = %d \n",n1,n2, -mult(n1,-n2));
        return 0;
    }
    else if (n1<0) {
        printf("%d x %d = %d \n",n1,n2, -mult(-n1,n2));
        return 0;
    }

}
