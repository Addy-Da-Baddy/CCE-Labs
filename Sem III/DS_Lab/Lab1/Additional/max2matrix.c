#include <stdio.h>
int main(){
    //defining array and vars
    int n,m,i,j;
    printf("Enter dimensions of the matrices: ");
    scanf("%d%d", &m,&n);
    int A[m][n] ;
    int B[m][n] ;

    //Accepting array elements
    printf("Enter elements of  Matrix 1 : \n");
    for (i = 0; i<m; i++){
            for (j = 0; j<n; j++)
            scanf("%d", &A[i][j]);
    }

      printf("Enter elements of  Matrix 2 : \n");
      for (i = 0; i<m; i++){
            for (j = 0; j<n; j++)
            scanf("%d", &B[i][j]);
    }

      printf("Matrix 1 : \n");
    for (i = 0; i<m; i++){
            for (j = 0; j<n; j++)
            printf("%d ", A[i][j]);
        printf("\n");
    }


      printf("Matrix 2 : \n");
    for (i = 0; i<m; i++){
            for (j = 0; j<n; j++)
            printf("%d ", B[i][j]);
        printf("\n");
    }

    int C[m][n];
      for (i = 0; i<m; i++){
            for (j = 0; j<n; j++){
            int e1 = A[i][j];
            int e2 = B[i][j];
            int *e3 = &C[i][j];

            if (e1>e2)
                *e3 = e1;
            else
                *e3 = e2;

        }
    }
     printf("Matrix 3 : \n");
    for (i = 0; i<m; i++){
            for (j = 0; j<n; j++)
            printf("%d ", C[i][j]);
        printf("\n");
    }

}
