class UGStudent extends Student{
    int semester;
    double fees;
    static int count_UG = 0;
    UGStudent(String name, String regNo, int age, int semester, double fees){
        super(name,regNo,age);
        this.semester = semester;
        this.fees = fees;
        count_UG++;
    }

    void display(){
        super.display();
        System.out.println("Semester: " + semester);
        System.out.println(); 
        }

    int getUGCount(){
        return count_UG;
    }

}