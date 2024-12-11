class Student{
    String name;
    String regNo;
    int age;

    Student (String name, String regNo, int age) {
        this.name = name;
        this.age = age;
        this.regNo = regNo;
    }

    void display(){
        System.out.println("Name: " + name);
        System.out.println("Age: " + age);
        System.out.println("Registration Number: " + regNo);
    }
}

