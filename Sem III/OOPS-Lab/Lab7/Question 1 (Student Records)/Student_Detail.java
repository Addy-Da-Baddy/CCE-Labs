public class Student_Detail {
    String name, id, college_name;
    Student_Detail(String name, String id){
        this.name = name;
        this.id = id;
        this.college_name = "MIT";
    }
    static void display_details(Student_Detail details[]){
        for (Student_Detail s:details){
            System.out.println("Name: " + s.name);
            System.out.println("ID: " + s.id);
            System.out.println("College: : " + s.college_name);
        }
    }
}
