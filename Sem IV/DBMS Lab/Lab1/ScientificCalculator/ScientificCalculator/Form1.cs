using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace ScientificCalculator
{
    public partial class Form1 : Form
    {
        int val1;
        int val2;
        bool gotVal1 = false;
        bool gotVal2 = false;
        String numVal = "" ;
        String op = "" ;
        int scientifcVal;
        public Form1()
        {
            InitializeComponent();
        }

        private void textBox1_TextChanged(object sender, EventArgs e)
        {

        }


        private void button1_Click(object sender, EventArgs e)
        {
            numVal = numVal + '1';
            displayOnScreen();
        }

        private void button2_Click(object sender, EventArgs e)
        {
            numVal = numVal + '2';
            displayOnScreen();

        }

        private void button3_Click(object sender, EventArgs e)
        {
            numVal = numVal + '3';
            displayOnScreen();
        }

        private void button4_Click(object sender, EventArgs e)
        {
            numVal = numVal + '4';
            displayOnScreen();
        }

        private void button5_Click(object sender, EventArgs e)
        {
            numVal = numVal + '5';
            displayOnScreen();
        }

        private void button6_Click(object sender, EventArgs e)
        {
            numVal = numVal + '6';
            displayOnScreen();
        }

        private void button7_Click(object sender, EventArgs e)
        {
            numVal = numVal + '8';
            displayOnScreen();
        }

        private void button8_Click(object sender, EventArgs e)
        {
            numVal = numVal + '7';
            displayOnScreen();
        }

        private void button9_Click(object sender, EventArgs e)
        {
            numVal = numVal + '9';
            displayOnScreen();
        }

        private void button0_Click(object sender, EventArgs e)
        {
            numVal = numVal + '0';
            displayOnScreen();
        }

        private void button_sqrt_Click(object sender, EventArgs e)
        {
            operatorClicked();
            op = "sqrt";
            displayBasicOp(op);
        }

        private void button_sin_Click(object sender, EventArgs e)
        {
            operatorClicked();
            op = "sin";
            displayBasicOp(op);
        }

        private void button_cos_Click(object sender, EventArgs e)
        {
            operatorClicked();
            op = "cos";
            displayBasicOp(op);
        }

        private void button_tan_Click(object sender, EventArgs e)
        {
            operatorClicked();
            op = "tan";
            displayBasicOp(op);
        }

        private void button_plus_Click(object sender, EventArgs e)
        {
            operatorClicked();
            op = "+";
            displayBasicOp(op);
        }

        private void button_minus_Click(object sender, EventArgs e)
        {
            operatorClicked();
            op = "-";
            displayBasicOp(op);
        }

        private void button_div_Click(object sender, EventArgs e)
        {
            operatorClicked();
            op = "/";
            displayBasicOp(op);
        }

        private void button_mul_Click(object sender, EventArgs e)
        {
            operatorClicked();
            op = "x";
            displayBasicOp(op);
        }

        private void button_eq_Click(object sender, EventArgs e)
        {
            if (op == "") {
                MessageBox.Show("No Operation Selected");
            }

            switch (op)
            {
                case "+":
                    handleBasicCheck();
                    int resultp = val1 + val2;
                    textBox1.Text = resultp.ToString();  // Convert the integer to a string
                    reset();
                    break;
                case "x":
                    handleBasicCheck();
                    int resultmul = val1 * val2;
                    textBox1.Text = resultmul.ToString();  // Convert the integer to a string
                    reset();
                    break;
                case "-":
                    handleBasicCheck();
                    int resultmin = val1 - val2;
                    textBox1.Text = resultmin.ToString();  // Convert the integer to a string
                    reset();
                    break;
                case "/":
                    handleBasicCheck();
                    if (val2 == 0)
                    {
                        MessageBox.Show("Division by zero is not allowed");
                        reset();
                        textBox1.Text = "UNDEFINED";
                        break;
                    }
                    double resultdiv = (double)val1 / val2;
                    textBox1.Text = resultdiv.ToString();  // Convert the integer to a string
                    reset();
                    break;
                case "sqrt":
                    handleScientificCheck();
                    double resultsqrt = Math.Sqrt(scientifcVal);
                    textBox1.Text = resultsqrt.ToString();
                    break;
                case "sin":
                    handleScientificCheck();
                    double resultsin = Math.Sin(scientifcVal);
                    textBox1.Text = resultsin.ToString();
                    break;
                case "cos":
                    handleScientificCheck();
                    double resultcos = Math.Cos(scientifcVal);
                    textBox1.Text = resultcos.ToString();
                    break;
                case "tan":
                    handleScientificCheck();
                    double resulttan = Math.Tan(scientifcVal);
                    textBox1.Text = resulttan.ToString();
                    break;
            }

            

        }

        void displayOnScreen()
        {
            textBox1.Text = numVal;
        }

        void operatorClicked()
        {
            if (!gotVal1 && numVal!="") {
                gotVal1 = true;
                val1 = Convert.ToInt32(numVal);
                numVal = "";
            }

            
        }

        void displayBasicOp(String op)
        {
            textBox1.Text = op;
        }

        void handleBasicCheck()
        {
            if (!gotVal1)
            {
                MessageBox.Show("Expected an Operand");
                reset();
            }
            else
            {
                if (!gotVal2 && numVal != "")
                {
                    gotVal2 = true;
                    val2 = Convert.ToInt32(numVal);
                    numVal = "";
                }
            }
        }

        void handleScientificCheck()
        {
            if (numVal == "")
            {
                MessageBox.Show("Expected atleast one operand after scientific operator");
                reset();
            }
            else
            {
                scientifcVal = Convert.ToInt32(numVal);
                numVal = "";

            }
        }

        void reset()
        {
         gotVal1 = false;
         gotVal2 = false;
         numVal = "" ;
         op = "";

        }

        private void button10_Click(object sender, EventArgs e)
        {
            reset();
            textBox1.Text = "";
        }

    }
}
