using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using Oracle.ManagedDataAccess.Client;

namespace Frontend_InsuranceDB
{
    public partial class Form1 : Form
    {
        OracleConnection conn;
        public Form1()
        {
            InitializeComponent();
        }


        public void ConnectDB()
        {

            conn = new OracleConnection("DATA SOURCE=172.16.54.24:1521/ictorcl;USER ID=CCE230953244;PASSWORD=student");

            try
            {

                conn.Open();

                MessageBox.Show("Connected");

            }

            catch (Exception e1)
            {

            }

        }
        private void label1_Click(object sender, EventArgs e)
        {

        }

        private void button1_Click(object sender, EventArgs e)
        {
            ConnectDB();
            OracleCommand command1 = conn.CreateCommand();
            String id;
            id = textBox2.Text;
            command1.CommandText = "select name,driver_id from person where driver_id = '" + id + "'";
            command1.CommandType = CommandType.Text;
            OracleDataReader dr = command1.ExecuteReader();
            dr.Read();
            textBox1.Text = dr.GetString(0);
            textBox2.Text = dr["Driver_ID"].ToString();
            command1.Dispose();
            conn.Close();
        }

        private void button2_Click(object sender, EventArgs e)
        {
            ConnectDB();
            String id1 = textBox2.Text;
            OracleCommand command1 = conn.CreateCommand();
            command1.CommandText = "DELETE FROM person WHERE Driver_ID=' " + id1 + "'";
            command1.CommandType = CommandType.Text;
            command1.ExecuteNonQuery();
            command1.Dispose();
            conn.Close();
            MessageBox.Show("Deleted Successfully");
        }


        private void button3_Click(object sender, EventArgs e)
        {
            ConnectDB();
            String name;
            String id1;
            ConnectDB();
            OracleCommand command1 = conn.CreateCommand();

            name = textBox1.Text;
            id1 = textBox2.Text;
            command1.CommandText = "update person set name=" + "'" + name + "'" + " where Driver_ID=" + id1;
            command1.CommandType = CommandType.Text;
            command1.ExecuteNonQuery();
            command1.Dispose();
            conn.Close();
            MessageBox.Show("Update SuccessfuL");
        }

        private void button2_Click_1(object sender, EventArgs e)
        {
            ConnectDB();
            String id1 = textBox2.Text;
            OracleCommand command1 = conn.CreateCommand();
            command1.CommandText = "DELETE FROM person WHERE Driver_ID=' " + id1 + "'";
            command1.CommandType = CommandType.Text;
            command1.ExecuteNonQuery();
            command1.Dispose();
            conn.Close();
            MessageBox.Show("Deleted Successfully");
        }

        private void button3_Click_1(object sender, EventArgs e)
        {
            ConnectDB();
            String name;
            String id1;
            ConnectDB();
            OracleCommand command1 = conn.CreateCommand();

            name = textBox1.Text;
            id1 = textBox2.Text;
            command1.CommandText = "update person set name=" + "'" + name + "'" + " where Driver_ID= '" + id1 + "'";
            command1.CommandType = CommandType.Text;
            command1.ExecuteNonQuery();
            command1.Dispose();
            conn.Close();
            MessageBox.Show("Update Successfull");
        }

        private void button4_Click(object sender, EventArgs e)
        {
            ConnectDB();
            OracleCommand comm1 = new OracleCommand();
            comm1.Connection = conn;
            comm1.CommandText = "select * from person";
            comm1.CommandType = CommandType.Text;

            OracleDataAdapter da = new OracleDataAdapter(comm1.CommandText, conn);

            // An OracleDataAdapter object represents a data provider object that populates the    DataSet and updates changes in the DataSet to the Oracle database

            DataSet ds = new DataSet();  // This is a collection of DataTables. We use the DataSet type to store many DataTables in a single collection
            da.Fill(ds, "instructor");   // DataAdapter.Fill (ds) here fetches the data from User and fills in the DataSet ds.

            dataGridView1.DataSource = ds.Tables[0]; 
        }
    }
}
