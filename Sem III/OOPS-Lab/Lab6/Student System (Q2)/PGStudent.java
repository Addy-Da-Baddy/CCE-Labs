class PGStudent extends Student{
    int semester;
    double fees;
    static int count_PG = 0;
    PGStudent(String name, String regNo, int age, int semester, double fees){
        super(name,regNo,age);
        this.semester = semester;
        this.fees = fees;
        count_PG++;
    }

    void display(){
        super.display();
        System.out.println("Semester: " + semester);
        System.out.println("Fees: " + fees);        
        System.out.println(); 
    }

    int getPGCount(){
        return count_PG;
    }

}
