# Import Packages & Libraries
import unittest
import pandas as pd
import smtplib, ssl
import sqlite3 as sql


# Import Classes
from classes import Employee, Email, Projects, CreatePairs, CreateGUI

# run line below for unittesting
# python3 -m unittest -v unittesting.py

class TestEmail(unittest.TestCase):

    '''
    Checks that our email class works as expected

    '''

    def test_email_port(self):
        '''
        Checksa that email port for automated emails is equal to 465
        '''
        setupEmail = Email(465, "smtp.gmail.com", "ntuworksystem@gmail.com", "Lucky1234")
        port = setupEmail.GetPort()
        self.assertEquals(port, 465)

    def test_sender_email(self):
        '''
        checks that sender email is equal to ntuworksystem@gmail.com
        '''
        setupEmail = Email(465, "smtp.gmail.com", "ntuworksystem@gmail.com", "Lucky1234")
        sender_email, password = setupEmail.SenderEmail_Password()
        self.assertEquals(sender_email, "ntuworksystem@gmail.com")

    def test_password_email(self):
        '''
        checks that password is equal to Lucky1234
        '''
        setupEmail = Email(465, "smtp.gmail.com", "ntuworksystem@gmail.com", "Lucky1234")
        sender_email, password = setupEmail.SenderEmail_Password()
        self.assertEquals(password, "Lucky1234")

    def test_smtp_server(self):
        '''
        checks that smtp server is equal to smtp.gmail.com
        '''
        setupEmail = Email(465, "smtp.gmail.com", "ntuworksystem@gmail.com", "Lucky1234")
        smtp_server = setupEmail.SmtpServer()
        self.assertEquals(smtp_server, "smtp.gmail.com")

if __name__ == '__main__':
    unittest.main()

class TestEmployee(unittest.TestCase):
    '''
    Checks That our Employee Class works as expected
    '''

    def test_password(self):
        '''
        Checks that password for A1 is world
        '''
        Employee1 = Employee("A1", "world", 'info@shaanaucharagram.com', 'Shaan', 'Aucharagram', 'Data Scientist')
        password = Employee1.GetPassword()
        self.assertEquals(password, 'world')

    def test_username(self):
        '''
        checks that username is A1
        '''
        Employee1 = Employee("A1", "world", 'info@shaanaucharagram.com', 'Shaan', 'Aucharagram', 'Data Scientist')
        username = Employee1.GetUserName()
        self.assertEquals(username, 'A1')

    def test_email(self):
        '''
        Checks that email for A1 is correct
        '''
        Employee1 = Employee("A1", "world", 'info@shaanaucharagram.com', 'Shaan', 'Aucharagram', 'Data Scientist')
        email = Employee1.GetEmail()
        self.assertEquals(email, "info@shaanaucharagram.com")

    def test_status_admin(self):
        '''
        Checks that status for A1 and M1 are True
        '''
        Employee1 = Employee("A1", "world", 'info@shaanaucharagram.com', 'Shaan', 'Aucharagram', 'Data Scientist')
        status_e1 = Employee1.GetStatus()
        Employee5 = Employee("M1", "luck123", "mumtaz@gmail.com", 'Sofia', 'Mumtaz', 'Account Manager')
        status_e4 = Employee5.GetStatus()
        self.assertTrue(status_e1)
        self.assertTrue(status_e4)


    def test_status_not_admin(self):
        '''
        Checks that E2 status is false
        '''
        Employee4 = Employee("E2", "luck123", "smith@gmail.com", 'John', 'Smith', 'Software Engineer')
        status = Employee4.GetStatus()
        self.assertFalse(status)

    def test_status_card_admin(self):
        '''
        Checks that A1 status card is Admin
        '''
        Employee1 = Employee("A1", "world", 'info@shaanaucharagram.com', 'Shaan', 'Aucharagram', 'Data Scientist')
        status_card = Employee1.GetStatusCard()
        self.assertEquals(status_card, "Admin")

    def test_status_card_manager(self):
        '''
        Checks that M1 status card is Manager
        '''
        Employee5 = Employee("M1", "luck123", "mumtaz@gmail.com", 'Sofia', 'Mumtaz', 'Account Manager')
        status_card = Employee5.GetStatusCard()
        self.assertEquals(status_card, "Manager")

    def test_status_card_employee(self):
        '''
        Checks that A1 status card is Employee
        '''
        Employee4 = Employee("E2", "luck123", "smith@gmail.com", 'John', 'Smith', 'Software Engineer')
        status_card = Employee4.GetStatusCard()
        self.assertEquals(status_card, "Employee")

    def test_get_name(self):
        '''
        Checks that get name return concatentation of first and last name
        '''
        Employee4 = Employee("E2", "luck123", "smith@gmail.com", 'John', 'Smith', 'Software Engineer')
        employee_name = Employee4.GetName()
        self.assertEquals(employee_name, "John Smith")

    def test_get_job(self):
        '''
        Checks that get_job func returns job
        '''
        Employee4 = Employee("E2", "luck123", "smith@gmail.com", 'John', 'Smith', 'Software Engineer')
        employee_job = Employee4.GetJob()
        self.assertEquals(employee_job, "Software Engineer")

if __name__ == '__main__':
    unittest.main()

class TestDatabase(unittest.TestCase):
    '''
    Class used to evaluate local database
    '''

    def test_connection(self):
        '''
        test there is a connection to database
        '''
        conn = sql.connect('worksystem2.db')
        conn.cursor()
        self.assertTrue(conn)


    def test_read_database_projects(self):
        '''
        Check that we can read data from database for projects table
        '''
        conn = sql.connect('worksystem2.db')
        object_project = Projects('projects.csv', "subtasks.csv")
        try:
            projects = object_project.read_data_local_database('projects', conn)
            db_read = True
        except:
            db_read = False
        self.assertTrue(db_read)

    def test_read_database_subtasks(self):
        '''
        Check that we can read data from database table
        '''
        conn = sql.connect('worksystem2.db')
        object_project = Projects('projects.csv', "subtasks.csv")
        try:
            subtasks = object_project.read_data_local_database('subtasks', conn)
            db_read = True
        except:
            db_read = False
        self.assertTrue(db_read)

    def test_dummy_upload_database_table(self):
        '''
        Check that we can upload dummy table to database
        '''
        conn = sql.connect('worksystem2.db')
        object_project = Projects('projects.csv', "subtasks.csv")
        data = {"A" : ["John","Deep","Julia","Kate","Sandy"],
                     "MonthSales" : [25,30,35,40,45]}
        try:
            object_project.upload_data_local_database('dummytable', data, conn)
            db_upload = True
        except:
            db_upload = False
        self.assertTrue(db_upload)

class TestGUI(unittest.TestCase):
    '''
    Class used to test our GUI app
    '''

    def test_gui_app(self):
        '''
        Check that GUI app is created with base layout
        '''
        VALID_USERNAME_PASSWORD_PAIRS = {'A1' : 'World',
                                        'E1' : 'Hello'}
        external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', 'style.css']
        try:
            GUI_app = CreateGUI(VALID_USERNAME_PASSWORD_PAIRS, 'Work Management System', external_stylesheets)
            app = GUI_app.create_gui()
            gui_success = True
        except:
            gui_success = False
        self.assertTrue(gui_success)

    def test_login(self):
        '''
        Check that Log-In credentials are passed into GUI app
        '''
        VALID_USERNAME_PASSWORD_PAIRS = {'A1' : 'World',
                                        'E1' : 'Hello'}
        external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', 'style.css']
        try:
            GUI_app = CreateGUI(VALID_USERNAME_PASSWORD_PAIRS, 'Work Management System', external_stylesheets)
            app = GUI_app.create_gui()
            auth = GUI_app.log_in(app)
            login_form = True
        except:
            login_form = False
        self.assertTrue(login_form)



if __name__ == '__main__':
    unittest.main()
