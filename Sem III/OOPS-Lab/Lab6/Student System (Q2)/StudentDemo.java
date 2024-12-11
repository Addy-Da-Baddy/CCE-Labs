 class StudentDemo {
    public static void main(String args[]){
        UGStudent ug1 = new UGStudent("Adriteyo Das" , "UGCCE321", 19, 3, 500000 );
        UGStudent ug2 = new UGStudent("Shivam Lahoty" , "UGCSE001", 18, 1, 400000 );
        UGStudent ug3 = new UGStudent("Aditya Bhansali" , "UGECE121", 21, 7, 300000 );
        PGStudent pg1 = new PGStudent("Samarth Patel" , "PGEE102", 23, 1, 100000 );
        PGStudent pg2 = new PGStudent("Vibhas Prasoon" , "PGMS321", 24, 3, 100000 );

        System.out.println("Total Number of UG Students: " + UGStudent.count_UG);
        System.out.println("Details of UG Students: ");
        System.out.println(); 
        ug1.display();
        ug2.display();
        ug3.display();

        System.out.println("Total Number of PG Students: " + PGStudent.count_PG);
        System.out.println("Details of PG Students: ");
        System.out.println(); 
        pg1.display();
        pg2.display();




    }
}
