import java.util.Scanner;

public class Time {
    private int hours;
    private int minutes;
    private int seconds;

    public Time() {
        this.hours = 0;
        this.minutes = 0;
        this.seconds = 0;
    }

    public Time(int hours, int minutes, int seconds) {
        this.hours = hours;
        this.minutes = minutes;
        this.seconds = seconds;
        normalizeTime(); 
    }

    public void displayTime() {
        System.out.printf("%02d:%02d:%02d\n", hours, minutes, seconds);
    }

    public static void addTime(Time t1, Time t2) {
        Time result = new Time();

        result.hours = t1.hours + t2.hours;
        result.minutes = t1.minutes + t2.minutes;
        result.seconds = t1.seconds + t2.seconds;

        result.normalizeTime();

        System.out.print("Time after addition: ");
        result.displayTime();
    }

    private void normalizeTime() {
        if (seconds >= 60) {
            minutes += seconds / 60;
            seconds %= 60;
        }
        if (minutes >= 60) {
            hours += minutes / 60;
            minutes %= 60;
        }
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        System.out.println("Enter hours, minutes, and seconds for Time 1: ");
        int hours1 = sc.nextInt();
        int minutes1 = sc.nextInt();
        int seconds1 = sc.nextInt();
        Time time1 = new Time(hours1, minutes1, seconds1);

        System.out.println("Enter hours, minutes, and seconds for Time 2: ");
        int hours2 = sc.nextInt();
        int minutes2 = sc.nextInt();
        int seconds2 = sc.nextInt();
        Time time2 = new Time(hours2, minutes2, seconds2);

        System.out.print("Time 1: ");
        time1.displayTime();
        System.out.print("Time 2: ");
        time2.displayTime();

        Time.addTime(time1, time2);

    }
}
