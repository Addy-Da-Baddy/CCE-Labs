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


    public partial class Form2 : Form
    {
        double b;
        DateTime lad;
        String user;
        int[] l5;
        int i;
        public Form2()
        {
            InitializeComponent();

        }
        public Form2(double Balance, DateTime LastAccessDate, String Username, int[] Last5Transactions, int index)
        {
            InitializeComponent();
            b = Balance;
            lad = LastAccessDate;
            user = Username;
            l5 = Last5Transactions;
            label2.Text = "USERNAME: " + user;
            label3.Text = "BALANCE: " + b.ToString("C2");
            label4.Text = "LAST ACCESS DATE: " + lad.ToString("dd MMM yyyy");
            i = index;
            // Display the last 5 transactions 
            listBox1.Items.Clear();
            foreach (var transaction in l5)
            {
                if (transaction > 0)
                {
                    listBox1.Items.Add("CREDITED: " + transaction);
                }
                else
                {
                    listBox1.Items.Add("DEBITED: " + -1*transaction);
                }
            }
        }

        private void button1_Click(object sender, EventArgs e)
        {
            Form4 f = new Form4(b,lad, user, l5, i);
            f.Show();
            this.Hide();
        }

        private void button2_Click(object sender, EventArgs e)
        {
            Form1 f = new Form1();
            f.Show();
            this.Hide();
        }
    }
}
