// generate odd numbers from 1 to 100.
class oddGenerator {
    public static void main(String[] args) {
		System.out.println("All odd numbers between 0 and 100: ");
        for (int i = 0; i<=100; i ++){
            if (i%2!=0){
                System.out.print(i + " ");
            }
        }
    }
    
}
