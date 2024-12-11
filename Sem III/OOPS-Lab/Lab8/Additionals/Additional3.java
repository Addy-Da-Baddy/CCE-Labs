interface sports{
    public void dispGoals();
    public void showWinner();
}

class Football implements sports{
    int team1_g = 0;
    int team2_g = 0;
    public  void goalTeam1(){
        team1_g++;
    }
    public void goalTeam2(){
        team2_g++;
    }
    public void dispGoals(){
        System.out.println("Goals by Team 1: " + team1_g);
        System.out.println("Goals by Team 2: " + team2_g);
    }
    public void showWinner(){
        if (team1_g>team2_g){
            System.out.println("The winner is Team 1!");
        }
        else if(team2_g>team1_g){
            System.out.println("The winner is Team 2!");
        }
        else {
            System.out.println("The Match is a draw!");
        }
    }
}

class Hockey implements sports{
    int team1_g = 0;
    int team2_g = 0;
    void goalTeam1(){
        team1_g++;
    }
    void goalTeam2(){
        team2_g++;
    }
    public void dispGoals(){
        System.out.println("Goals by Team 1: " + team1_g);
        System.out.println("Goals by Team 2: " + team2_g);
    }
    public void showWinner(){
        if (team1_g>team2_g){
            System.out.println("The winner is Team 1!");
        }
        else if(team2_g>team1_g){
            System.out.println("The winner is Team 2!");
        }
        else {
            System.out.println("The Match is a draw!");
        }
    }
}

class Additional3{
    public static void main(String args[]){
        Football f1 = new Football();
        f1.goalTeam1();
        f1.goalTeam2();
        f1.goalTeam2();
        f1.goalTeam2();
        System.out.println("Results of the Football Match: ");
        f1.dispGoals();
        f1.showWinner();
        System.out.println();

        Hockey h = new Hockey();
        h.goalTeam2();
        h.goalTeam1();
        h.goalTeam1();
        h.goalTeam2();
        System.out.println("Results of the Hockey Match: ");
        h.dispGoals();
        h.showWinner();
        System.out.println();

    }
}
