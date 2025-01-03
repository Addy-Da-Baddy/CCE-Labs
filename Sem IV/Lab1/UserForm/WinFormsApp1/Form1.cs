using System.Windows.Forms;

namespace WinFormsApp1
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        private void label1_Click(object sender, EventArgs e)
        {

        }

        private void textBox1_TextChanged(object sender, EventArgs e)
        {

        }

        private void dateTimePicker1_ValueChanged(object sender, EventArgs e)
        {

        }

        private void button1_Click(object sender, EventArgs e)
        {
            string name = "";          // Empty string for name
            string reg_num = "";       // Empty string for registration number
            string gender = "";        // Empty string for gender
            string course = "";        // Empty string for course
            bool isHostel = false;     // Default to false (not selected)
            bool isMess = false;       // Default to false (not selected)
            DateTime dob = DateTime.MinValue; // Default to the minimum possible date (if no date is selected)
            bool isValid = true;

            if (textBox1.Text == "")
            {
                MessageBox.Show("Name field should not be empty");
                isValid = false;
            }
            else
            {
                name = textBox1.Text;
            }

            if (textBox2.Text == "")
            {
                MessageBox.Show("Registration Number field should not be empty");
                isValid = false;
            }
            else
            {
                reg_num = textBox2.Text;
            }
            if (radioButton1.Checked) 
            {
                gender = "Female";
            }
            else if (radioButton2.Checked) 
            {
                gender = "Male";
            }
            else 
            {
                MessageBox.Show("Gender not selected");
                isValid = false;

            }

            if (comboBox1.SelectedIndex == -1) 
            {
                MessageBox.Show("Course not selected");
                isValid = false;

            }
            else 
            {
                course = comboBox1.SelectedItem.ToString();
            }

            if (dateTimePicker1.Value == dateTimePicker1.MinDate) 
            {
                MessageBox.Show("Date not selected");
                isValid = false;

            }
            else 
            {
                dob = dateTimePicker1.Value;
            }

            if (checkBox1.Checked) 
            {
                isHostel = true;
            }

            if (checkBox2.Checked) 
            {
                isMess = true;
            }

            string studentDetails = "Name: " + name + "\n" +
                                "Registration Number: " + reg_num + "\n" +
                                "Gender: " + gender + "\n" +
                                "Course: " + course + "\n" +
                                "Hostel: " + (isHostel ? "Yes" : "No") + "\n" +
                                "Mess: " + (isMess ? "Yes" : "No") + "\n" +
                                "Date of Birth: " + dob.ToString("dd-MM-yyyy");  // Format the date as dd-MM-yyyy


            if (isValid)
            {
                MessageBox.Show(studentDetails, "Student Details");
            }






        }
    }
}
