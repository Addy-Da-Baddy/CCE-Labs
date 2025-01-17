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
    public partial class Form3 : Form
    {
        String[] userNames;
        String[] pass;
        public Form3(String[] userName, String[] password)
        {
            InitializeComponent();
            userNames = userName;
            pass = password;
        }

        private void button1_Click(object sender, EventArgs e)
        {
            bool userFound = false;
            for (int i = 0; i < userNames.Length; i++)
            {
                if (textBox1.Text == userNames[i])
                {
                    userFound = true;
                    if (textBox2.Text == pass[i])
                    {
                        pass[i] = textBox4.Text;
                        MessageBox.Show("Password Changed Successfully");
                        Form1 f = new Form1(userNames, pass);
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
    }
}
