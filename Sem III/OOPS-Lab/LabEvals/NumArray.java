import java.util.*;
class NumArray{
    int arr[] = new int[10];
    Scanner sc = new Scanner(System.in);

    NumArray(){
        for (int i = 0; i<10; i++){
            System.out.println("Enter the value at index: " + i);
            arr[i] = sc.nextInt();
        }
    }

    void even(){
        int cnt = 0;
        for (int ele:arr){
            if (ele%2==0)
                cnt++;
        }
        System.out.println("no. of even numbers: " + cnt);
    }

    void odd(){
        int cnt = 0;
        for (int ele:arr){
            if (ele%2!=0)
                cnt++;
        }
        System.out.println("no. of odd numbers: " + cnt);
    }

    void zero(){
        int cnt = 0;
        for (int ele:arr){
            if (ele==0)
                cnt++;
        }
        System.out.println("no. of zeroes : " + cnt);
    }

    public static void main(String args[]){
        NumArray n1 = new NumArray();
        n1.even();
        n1.odd();
        n1.zero();

    }



}