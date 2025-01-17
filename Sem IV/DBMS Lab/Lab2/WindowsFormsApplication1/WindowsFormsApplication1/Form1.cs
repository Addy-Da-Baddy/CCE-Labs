using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace WindowsFormsApplication1
{
    public partial class Form1 : Form
    {

              public string[] userNames = new string[] { "ADAS001", "CSHARMA021", "RSHETTY005", "GPAI234", "VSINGH442" };
              public string[] password = new string[] { "pass1", "pass2", "pass3", "pass4", "pass4" };
        public Form1()
        {
            InitializeComponent();
                    userNames = new string[] { "ADAS001", "CSHARMA021", "RSHETTY005", "GPAI234", "VSINGH442" };
                    password = new string[] { "pass1", "pass2", "pass3", "pass4", "pass4" };   
        }



        public Form1(string[] newUsers, String[] newPass)
        {
            InitializeComponent();
            userNames = newUsers;
            password = newPass;
        }

        public Form1(double Balance, DateTime LastAccessDate, String Username, int[] Last5Transactions, int index)
        {
            User updated = new User(Balance, LastAccessDate, Username, Last5Transactions);
            users[index] = updated;
        }


        public class User { public double Balance; public DateTime LastAccessDate; public string Username; public int[] Last5Transactions; public User(double balance, DateTime lastAccessDate, string username, int[] last5Transactions) { this.Balance = balance; this.LastAccessDate = lastAccessDate; this.Username = username; this.Last5Transactions = last5Transactions; } }
        User[] users = new User[] { new User(1500.75, DateTime.Now.AddDays(-1), "ADAS001", new int[] { 1000, -23, 500, -100, 200 }), new User(2000.50, DateTime.Now.AddDays(-2), "CSHARMA021", new int[] { 250, -50, 300, -200, 150 }), new User(3200.00, DateTime.Now.AddDays(-3), "RSHETTY005", new int[] { 100, -75, 200, -150, 300 }), new User(1750.25, DateTime.Now.AddDays(-4), "GPAI234", new int[] { 400, -60, 500, -80, 250 }), new User(4500.75, DateTime.Now.AddDays(-5), "VSINGH442", new int[] { 150, -30, 350, -100, 400 }) };

        private void button1_Click(object sender, EventArgs e)
        {
            bool userFound = false;

            for (int i = 0; i < userNames.Length; i++)
            {
                if (textBox1.Text == userNames[i])
                {
                    userFound = true;
                    if (textBox2.Text == password[i])
                    {
                        Form2 f = new Form2(users[i].Balance, users[i].LastAccessDate, users[i].Username, users[i].Last5Transactions, i);
                        f.Show();
                        this.Hide();
                    }
                    else
                    {
                        MessageBox.Show("Invalid Password");
                    }
                }
            }

            if (!userFound)
            {
                MessageBox.Show("Username not Found");
            }

        }

        private void button2_Click(object sender, EventArgs e)
        {
            Form3 f = new Form3(userNames, password);
            f.Show();
            this.Hide();

        }
    }
}
