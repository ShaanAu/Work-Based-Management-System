# Import Packages & Libraries
import dash
import dash_auth
import dash_html_components as html
import plotly
import pandas as pd
import smtplib, ssl
import base64
from sqlalchemy import create_engine
import concurrent.futures
import sqlite3 as sql

engine = create_engine('sqlite://', echo=False)


class Email:

    """
    Class used for setting up the connection to send emails after updating
    SubTasks or Projects Data Table

    ...

    Attributes
    ----------
    port : int
        port for email connection
    smtp_server : str
        internet standard communication protcol for email
    sender_email : str
        email used to send our automated emails
    password : str
        password for sender_email

    Methods
    -------
    GetPort()
        return the port as an int

    SenderEmail_Password()
        returns both sender_email and password

    smtp_server()
        returns smtp sever as string
    """


    def __init__(self, port, smtp_server, sender_email, password):
        self.port = port
        self.smtp_server = smtp_server
        self.sender_email = sender_email
        self.password = password
    def GetPort(self):
        """
        return the port as an int
        """


        return self.port

    def SenderEmail_Password(self):
        """
        returns both sender_email and password
        """
        return self.sender_email, self.password

    def SmtpServer(self):
        """
        returns smtp sever as string
        """
        return self.smtp_server



class Projects:

    """
    Class used for setting up Projects and SubTasks

    ...

    Attributes
    ----------
    csv_file_projects : csv_file
        csv_file containing project data
    csv_file_subtasks : csv_file
        csv_file_subtasks containing subtasks data

    Methods
    -------
    fetch_data_locally_projects()
        read in local data from csv file for projects tab and return dataframe

    fetch_data_locally_subtasks()
        read in local data from csv file for subtasks tab and return dataframe

    update_data_in_memory()
        update in-memory database using df

    read_data_database()
        read in data from in-memory database using table name

    update_data_csv()
        update local csv file


    """


    def __init__(self, csv_file_projects, csv_file_subtasks):
        """
        Attributes
        ----------
        csv_file_projects : csv_file
            csv_file containing project data
        csv_file_subtasks : csv_file
            csv_file_subtasks containing subtasks data
        """

        self.csv_file_projects = csv_file_projects
        self.csv_file_subtasks = csv_file_subtasks

    def fetch_data_locally_projects(self):
        """
        read in local data from csv file for projects tab and return dataframe

        """
        df = pd.read_csv(self.csv_file_projects)
        return df

    def fetch_data_locally_subtasks(self):
        '''
        read in local data from csv file for subtasks tab and return dataframe

        '''
        df = pd.read_csv(self.csv_file_subtasks, index_col=0)
        return df

    def update_data_in_memory(self, df_local, table_db):
        '''
        update in-memory database using df

        Parameters
        ----------
        df_local : array
            array of users choice converted to df
        table_db: string
            string containing table name to be uploaded to in-memory database

        '''

        self.df_local = df_local
        self.table_db = table_db
        pd.DataFrame(self.df_local).to_sql(self.table_db, con=engine, if_exists='replace')

    def read_data_in_memory(self, tablename):
        '''
        read in data from in-memory database using table name

        Parameters
        ----------
        tablename: string
            string containing table name to be read from in-memory database

        '''
        self.tablename = tablename
        datatable = engine.execute(f"SELECT * FROM {tablename}").fetchall()
        return datatable

    def upload_data_local_database(self, tablename, df, conn):
        '''
        upload data from local database using table name

        Parameters
        ----------
        tablename: string
            string containing table name to be uploaded to local database
        df: datagrame
            dataframe of users choice
        conn: object
            connection for sqllite database

        '''
        self.tablename = tablename
        self.df = df
        self.conn = conn
        self.df = pd.DataFrame(self.df)
        self.df = self.df.reset_index(drop=True)
        self.df.to_sql(self.tablename, self.conn, if_exists="replace", index=False)
        self.conn.commit()
        self.conn.close()

    def read_data_local_database(self, tablename, conn):
        '''
        read in data from local database using table name

        Parameters
        ----------
        tablename: string
            string containing table name to be uploaded to local database
        df: datagrame
            dataframe of users choice
        conn: object
            connection for sqllite database

        '''
        self.tablename = tablename
        self.conn = conn
        df = pd.read_sql_query(f"SELECT * FROM {tablename};", conn)
        self.conn.commit()
        self.conn.close()
        return df




    def update_data_csv(self, df_local, csv_file,index):
        '''
        update csv file using df

        Parameters
        ----------
        df_local : dataframe
            array of users choice converted to df
        csv: string
            csv_file of users choice to update
        index: bool
            whether index is kept or not for csv file
        '''
        self.df_local = df_local
        self.csv_file = csv_file
        self.index = index
        df = pd.DataFrame(self.df_local)
        df = df.reset_index(drop=True)
        df.to_csv(self.csv_file,index=self.index)





class Employee:

        """
        Class used for setting up Employee Details

        ...

        Attributes
        ----------
        username : string
            username for individual in organisation e.g. A1, M1, E1
        password : str
            username for individual in organisation
        email : str
            email for respective username
        firstname : str
            firstname for respective user e.g. John
        lastname : str
            lastname for respective user e.g. Smith
        job : str
            Job title for respective user e.g. Data Scientist


        Methods
        -------
        GetUserName()
            return username

        GetPassword()
            return password for respective username

        GetEmail()
            return email for respective username

        GetStatus()
            return status as bool true or false to determine whether they have admin/manager access or not

        GetStatusCard()
            return status as string, either as 'Manager', 'Admin' or 'Employee'

        GetName()
            return concatenation of first and last name

        GetJob()
            return job title of respective name

        """

        def __init__(self, username, password, email, firstname, lastname, job):

            '''
            Parameters
            ----------
            username : string
                username for individual in organisation e.g. A1, M1, E1
            password : str
                username for individual in organisation
            email : str
                email for respective username
            firstname : str
                firstname for respective user e.g. John
            lastname : str
                lastname for respective user e.g. Smith
            job : str
                Job title for respective user e.g. Data Scientist

            '''
            self.username = username
            self.password = password
            self.email = email
            self.job = job
            self.firstname = firstname
            self.lastname = lastname


        def GetUserName(self):
            '''
            return username
            '''
            return self.username

        def GetPassword(self):
            '''
            return password for respective username
            '''
            return self.password

        def GetEmail(self):
            '''
            return email for respective username
            '''
            return self.email

        def GetStatus(self):
            '''
            return status as bool true or false to determine whether they have admin/manager access or not
            '''
            if 'A' in self.username:
                Access = True
            elif 'M' in self.username:
                Access = True
            else:
                Access = False
            return Access

        def GetStatusCard(self):
            '''
            return status as string, either as 'Manager', 'Admin' or 'Employee'
            '''
            if 'A' in self.username:
                StatusCard = 'Admin'
            elif 'M' in self.username:
                StatusCard = 'Manager'
            else:
                StatusCard = 'Employee'
            return StatusCard

        def GetName(self):
            '''
            return concatenation of first and last name
            '''
            full_name = " ".join([self.firstname, self.lastname])
            return full_name

        def GetJob(self):
            '''
            return job title of respective name
            '''
            return self.job




# Create Dictionairy with GetUserName method and GetPassword method
class CreatePairs:
        """
        Class used for creating dictionaires for username to respective pair

        ...

        Attributes
        ----------
        Employee1 : object
            sample employee for company
        Employee2 : object
            sample employee for company
        Employee3 : object
            sample employee for company
        Employee4 : object
            sample employee for company
        Employee5 : object
            sample employee for company
        Employee6 : object
            sample employee for company


        Methods
        -------
        get_username_password_pair()
            returns a dictionary of username as the key and passwords as the values for all employees

        get_username_email_pairs()
            returns a dictionary of username as the key and emails as the values for all employees

        get_status_pairs()
            returns a dictionary of username as the key and status as the values for all employees

        get_status_card_pairs()
            returns a dictionary of username as the key and status_cards as the values for all employees

        get_name_pairs()
            returns a dictionary of username as the key and first_name+last_name as the values for all employees

        get_job_pairs()
            returns a dictionary of username as the key and jobs as the values for all employees


        """


        def __init__(self, Employee1, Employee2, Employee3, Employee4, Employee5, Employee6):
            '''
            Attributes
            ----------
            Employee1 : object
                sample employee for company
            Employee2 : object
                sample employee for company
            Employee3 : object
                sample employee for company
            Employee4 : object
                sample employee for company
            Employee5 : object
                sample employee for company
            Employee6 : object
                sample employee for company
            '''

            self.Employee1 = Employee1
            self.Employee2 = Employee2
            self.Employee3 = Employee3
            self.Employee4 = Employee4
            self.Employee5 = Employee5
            self.Employee6 = Employee6

        def get_username_password_pair(self):

            '''
            returns a dictionary of username as the key and passwords as the values for all employees

            '''
            # Usernames beginning with A - Admin
            # Usernames beginning with E - Employee
            # Usernames begging with M - Manager
            VALID_USERNAME_PASSWORD_PAIRS = {
                self.Employee1.GetUserName():self.Employee1.GetPassword() ,
                self.Employee2.GetUserName():self.Employee2.GetPassword() ,
                self.Employee3.GetUserName():self.Employee3.GetPassword() ,
                self.Employee4.GetUserName():self.Employee4.GetPassword() ,
                self.Employee5.GetUserName():self.Employee5.GetPassword() ,
                self.Employee6.GetUserName():self.Employee6.GetPassword()

            }
            return VALID_USERNAME_PASSWORD_PAIRS

        def get_username_email_pairs(self):
            '''
            returns a dictionary of username as the key and emails as the values for all employees

            '''

            EMAIL_PAIRS = {
                self.Employee1.GetUserName():self.Employee1.GetEmail() ,
                self.Employee2.GetUserName():self.Employee2.GetEmail() ,
                self.Employee3.GetUserName():self.Employee3.GetEmail() ,
                self.Employee4.GetUserName():self.Employee4.GetEmail() ,
                self.Employee5.GetUserName():self.Employee5.GetEmail() ,
                self.Employee6.GetUserName():self.Employee6.GetEmail()

            }
            return EMAIL_PAIRS

        def get_status_pairs(self):
            '''
            returns a dictionary of username as the key and status as the values for all employees

            '''

            STATUS_PAIRS = {
                self.Employee1.GetUserName():self.Employee1.GetStatus() ,
                self.Employee2.GetUserName():self.Employee2.GetStatus() ,
                self.Employee3.GetUserName():self.Employee3.GetStatus() ,
                self.Employee4.GetUserName():self.Employee4.GetStatus() ,
                self.Employee5.GetUserName():self.Employee5.GetStatus() ,
                self.Employee6.GetUserName():self.Employee6.GetStatus()

            }
            return STATUS_PAIRS


        def get_status_card_pairs(self):
            '''
            returns a dictionary of username as the key and status_cards as the values for all employees

            '''
            STATUS_CARD_PAIRS = {
                self.Employee1.GetUserName():self.Employee1.GetStatusCard() ,
                self.Employee2.GetUserName():self.Employee2.GetStatusCard() ,
                self.Employee3.GetUserName():self.Employee3.GetStatusCard() ,
                self.Employee4.GetUserName():self.Employee4.GetStatusCard() ,
                self.Employee5.GetUserName():self.Employee5.GetStatusCard() ,
                self.Employee6.GetUserName():self.Employee6.GetStatusCard()

            }
            return STATUS_CARD_PAIRS

        def get_name_pairs(self):
            '''
            returns a dictionary of username as the key and first_name+last_name as the values for all employees
            '''
            NAME_PAIRS = {
                self.Employee1.GetUserName():self.Employee1.GetName() ,
                self.Employee2.GetUserName():self.Employee2.GetName() ,
                self.Employee3.GetUserName():self.Employee3.GetName() ,
                self.Employee4.GetUserName():self.Employee4.GetName() ,
                self.Employee5.GetUserName():self.Employee5.GetName() ,
                self.Employee6.GetUserName():self.Employee6.GetName()

            }
            return NAME_PAIRS

        def get_job_pairs(self):
            '''
            returns a dictionary of username as the key and jobs as the values for all employees

            '''
            JOB_PAIRS = {
                self.Employee1.GetUserName():self.Employee1.GetJob(),
                self.Employee2.GetUserName():self.Employee2.GetJob(),
                self.Employee3.GetUserName():self.Employee3.GetJob(),
                self.Employee4.GetUserName():self.Employee4.GetJob(),
                self.Employee5.GetUserName():self.Employee5.GetJob(),
                self.Employee6.GetUserName():self.Employee6.GetJob()

            }
            return JOB_PAIRS




class CreateGUI:
        """
        Class used for setting up the GUI in Plotly Dash & LogIn Authentcation

        ...

        Attributes
        ----------
        VALID_USERNAME_PASSWORD_PAIRS : dict
            valid usernames for log-in authentication
        title : str
            title of the project
        external_stylesheets : list
            external_stylesheets used to style plotly dash app


        Methods
        -------
        create_gui()
            used to create the base plotly dash app, with title of gui & the external stylesheets

        log_in()
            used to pass through the password/username dictionary that will allow user to log-in to the gui


        """


        def __init__(self, VALID_USERNAME_PASSWORD_PAIRS, title, external_stylesheets):
            '''
            Parameters
            ----------
            VALID_USERNAME_PASSWORD_PAIRS : dict
                valid usernames for log-in authentication
            title : str
                title of the project
            external_stylesheets : list
                external_stylesheets used to style plotly dash app

            '''
            self.VALID_USERNAME_PASSWORD_PAIRS = VALID_USERNAME_PASSWORD_PAIRS
            self.title = title
            self.external_stylesheets = external_stylesheets

        def create_gui(self):
            '''
            used to create the base plotly dash app, with title of gui & the external stylesheets
            '''
            app = dash.Dash(__name__, external_stylesheets=self.external_stylesheets, title=self.title)
            return app

        def log_in(self, app):
            '''
            used to pass through the password/username dictionary that will allow user to log-in to the gui

            Parameters
            ----------
            app : dash.Dash
                Dash app that has been created

            '''
            self.app = app
            auth = dash_auth.BasicAuth(
                self.app,
                self.VALID_USERNAME_PASSWORD_PAIRS
            )
            return auth

class CreateGUI:
        """
        Class used for setting up the GUI in Plotly Dash & LogIn Authentcation

        ...

        Attributes
        ----------
        VALID_USERNAME_PASSWORD_PAIRS : dict
            valid usernames for log-in authentication
        title : str
            title of the project
        external_stylesheets : list
            external_stylesheets used to style plotly dash app


        Methods
        -------
        create_gui()
            used to create the base plotly dash app, with title of gui & the external stylesheets

        log_in()
            used to pass through the password/username dictionary that will allow user to log-in to the gui


        """


        def __init__(self, VALID_USERNAME_PASSWORD_PAIRS, title, external_stylesheets):
            '''
            Parameters
            ----------
            VALID_USERNAME_PASSWORD_PAIRS : dict
                valid usernames for log-in authentication
            title : str
                title of the project
            external_stylesheets : list
                external_stylesheets used to style plotly dash app

            '''
            self.VALID_USERNAME_PASSWORD_PAIRS = VALID_USERNAME_PASSWORD_PAIRS
            self.title = title
            self.external_stylesheets = external_stylesheets

        def create_gui(self):
            '''
            used to create the base plotly dash app, with title of gui & the external stylesheets
            '''
            app = dash.Dash(__name__, external_stylesheets=self.external_stylesheets, title=self.title)
            return app

        def log_in(self, app):
            '''
            used to pass through the password/username dictionary that will allow user to log-in to the gui

            Parameters
            ----------
            app : dash.Dash
                Dash app that has been created

            '''
            self.app = app
            auth = dash_auth.BasicAuth(
                self.app,
                self.VALID_USERNAME_PASSWORD_PAIRS
            )
            return auth
