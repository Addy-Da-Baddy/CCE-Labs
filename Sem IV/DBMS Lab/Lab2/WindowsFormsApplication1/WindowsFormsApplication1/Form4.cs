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
  
    public partial class Form4 : Form
    {
        double b;
        DateTime lad;
        String user;
        int[] l5;
        int index;
        public Form4(double Balance, DateTime LastAccessDate, String Username, int[] Last5Transactions, int i)
        {
            InitializeComponent();
            b = Balance;
            lad = LastAccessDate;
            user = Username;
            l5 = Last5Transactions;
            index = i ;
        }

        private void button1_Click(object sender, EventArgs e)
        {
            double amount;
            if (double.TryParse(textBox2.Text, out amount))
            {
                b = b - amount;

                for (int i = l5.Length - 1; i > 0; i--)
                {
                    l5[i] = l5[i - 1];
                }
                l5[0] = (int)amount;

                lad = DateTime.Now;

                MessageBox.Show("Transaction successful. New balance: " + b.ToString("C2"));

                Form2 f = new Form2(b, lad, user,l5,index);
                f.Show();
                this.Hide();
            }
            else
            {
                MessageBox.Show("Invalid amount entered.");
            }
        }

        private void button2_Click(object sender, EventArgs e)
        {
            Form2 f = new Form2(b, lad, user, l5,index);
            f.Show();
            this.Hide();
        }

    }
}
