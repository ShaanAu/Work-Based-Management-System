# Import Packages & Libraries
import dash
import dash_auth
import dash_core_components as dcc
import dash_html_components as html
import plotly
from flask import request
import pandas as pd
import dash_table
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import smtplib, ssl
import base64
from sqlalchemy import create_engine
import dash_bootstrap_components as dbc
import dash_html_components as html
import concurrent.futures
import sqlite3 as sql

# Import Classes
from classes import Employee, Email, Projects, CreatePairs, CreateGUI


# Create An In-Memory sqlite database
engine = create_engine('sqlite://', echo=False)

# Creating Seperate Thread To Set Up Email Settings
with concurrent.futures.ThreadPoolExecutor() as executor1:
    setupEmailFuture = executor1.submit(Email, 465, "smtp.gmail.com", "ntuworksystem@gmail.com", "Lucky1234")
    # Get Result from thread
    setupEmail = setupEmailFuture.result()
    port = setupEmail.GetPort()
    sender_email, password = setupEmail.SenderEmail_Password()
    smtp_server = setupEmail.SmtpServer()



# Creating Seperate Thread To read in data from database
with concurrent.futures.ThreadPoolExecutor() as executor2:
    # Create Object
    object_project_futue = executor2.submit(Projects, 'projects.csv', "subtasks.csv")
    # Get Result from thread
    object_project = object_project_futue.result()

    # Read in Projects & Subtasks From Local Database, If Not availiable uses local files instead
    conn = sql.connect('worksystem2.db')
    try:
        projects = object_project.read_data_local_database('projects', conn)
    except:
        projects = object_project.fetch_data_locally_projects()

    conn = sql.connect('worksystem2.db')
    try:
        subtasks = object_project.read_data_local_database('subtasks', conn)
    except:
        subtasks = object_project.fetch_data_locally_subtasks()
    # Create Dictionaires and append columns for projects and subtasks
    projects_columns = []
    subtask_col_param = []
    for col in projects.columns:
        projects_columns.append({"name": str(col), "id": str(col)})
    for col in subtasks.columns:
        subtask_col_param.append({"name": str(col), "id": str(col)})





# Creating Seperate Thread to set up employee details
with concurrent.futures.ThreadPoolExecutor() as executor3:
    # Creating Employees Data
    Employee1Future = executor3.submit(Employee, "A1", "world", 'info@shaanaucharagram.com', 'Shaan', 'Aucharagram', 'Data Scientist')
     # Get Result from thread
    Employee1 = Employee1Future.result()
    Employee2Future = executor3.submit(Employee, "A2", "password", "anthony@gmail.com", 'Tuchan', 'Anthony', 'IT Consultant')
    # Get Result from thread
    Employee2 = Employee2Future.result()
    Employee3Future = executor3.submit(Employee, "E1", "lucky12", "davies@gmail.com", 'Adam', 'Davies', 'Business Analyst')
    # Get Result from thread
    Employee3 = Employee3Future.result()
    Employee4Future = executor3.submit(Employee, "E2", "luck123", "smith@gmail.com", 'John', 'Smith', 'Software Engineer')
    # Get Result from thread
    Employee4 = Employee4Future.result()
    Employee5Future = executor3.submit(Employee, "M1", "luck123", "mumtaz@gmail.com", 'Sofia', 'Mumtaz', 'Account Manager')
    # Get Result from thread
    Employee5 = Employee5Future.result()
    Employee6Future = executor3.submit(Employee, "M2" ,"luck123", "baker@gmail.com", 'Ted', 'Baker', 'Marketing Executive')
    # Get Result from thread
    Employee6 = Employee6Future.result()



# Creating Seperate Thread to create dictionairies for employee details
with concurrent.futures.ThreadPoolExecutor() as executor4:
    # Creating Objects for CreatingPairs On All Employees
    employee_pairs_future = executor4.submit(CreatePairs, Employee1, Employee2, Employee3, Employee4, Employee5, Employee6)
    # Get Result from thread
    employee_pairs = employee_pairs_future.result()
    # Call Methods
    VALID_USERNAME_PASSWORD_PAIRS = employee_pairs.get_username_password_pair()
    EMAIL_PAIRS = employee_pairs.get_username_email_pairs()
    STATUS_PAIRS = employee_pairs.get_status_pairs()
    JOB_PAIRS = employee_pairs.get_job_pairs()
    NAME_PAIRS = employee_pairs.get_name_pairs()
    STATUS_CARD_PAIRS = employee_pairs.get_status_card_pairs()


# Use external stylesheet
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', 'style.css']

# Create Sepetayte Thread to set up our GUI app
with concurrent.futures.ThreadPoolExecutor() as executor5:
    # Creating Objects for GUI
    GUI_app_future = executor5.submit(CreateGUI, VALID_USERNAME_PASSWORD_PAIRS, 'Work Management System', external_stylesheets)
    # Get Result from thread
    GUI_app = GUI_app_future.result()
    # Instantiate Dash App
    app = GUI_app.create_gui()
    # Return Log-In Form
    auth = GUI_app.log_in(app)





app.layout = html.Div([

    html.Div([
    # Banner
        html.Div([
            html.H1("Work Management System",
                    style={"color": "white",
                           "fontFamily": "Open Sans",
                           "fontSize": 30,
                           "fontWeight": "bold",
                           "text-align": "center",
                           "display": "inline-block",'margin-left':'100px'}
                    )
        ],
            className="twelve columns",
            style={"padding-top": "10px", "text-align": "center"})
    ],
        className="row",
        style={"backgroundColor": "#EC0000"}

    # End of Banner
    ),

    dcc.Tabs([
        dcc.Tab(label='All Projects', children=[
        # First Tab

        html.Div([
        # Add Row Button
        html.Button('Add Row', id='save-data-button-projects', n_clicks=0),
        ]),

        html.Div([
            # DataFrame
            dash_table.DataTable(
                id='datatable-rows-projects',
                columns=projects_columns,
                data=projects.to_dict('records'),
                editable=True,
                row_deletable=True            ),
            html.Div([

            html.Div([

            # Save Button
            html.Button(id="save-button-projects",n_clicks=0,children="Save"),
            html.Div(id="div-projects",children="Press button to save changes")
                        ],className = 'fo columns'),

            ],className = 'row'),

            html.Br(),
            html.Hr(),

            html.Div([

            # Email Section

            # Input Box
            dcc.Input(id='username-placeholder-subtasks', placeholder='Enter Username e.g. A1', type="text"),
            # Submit Button
            html.Button('Send Email', id='send-email-button-subtasks'),
            ],style = {'width': '100%', 'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}),
            html.Br(),


            html.Div(id="send-email-subtasks-div",children="Press button to send email"),
            # Text Area to Submit Custom Email Message
                dcc.Textarea(
                id='email-message-custom-subtasks',
                placeholder='Enter Email Message Here',
                style={'width': '100%', 'height': 300},
                ),


        ])


        ]),
        dcc.Tab(label='SubTasks', children=[

            # Second Tab - SubTasks

                html.Div([

            # Data Table - SubTasks
                dash_table.DataTable(
                  id='datatable-subtasks',
                  columns=subtask_col_param,
                  data=subtasks.to_dict('records'),
                  editable=True,
                  row_deletable=True,
                  export_format='csv'
                ),            ]),

                # Add Button
                html.Button(id="save-data-button-subtasks",n_clicks=0,children="Add Row"),

                # Save Button
                html.Button(id="save-button-projects-subtasks",n_clicks=0,children="Save"),
                html.Div(id="div-subtasks",children="Press button to save changes"),

                html.Br(),
                html.Hr(),

            html.Div([

            # Email Section

                html.Div([

                # Input Box
                dcc.Input(id='username-placeholder-projects', placeholder='Enter Username e.g. A1', type="text"),

                # Button To Send Email
                html.Button('Send Email', id='send-email-button-projects'),
                html.Br(),

                html.Div(id="send-email-projects-div",children="Press button to send email"),
                ],style = {'width': '100%', 'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}),

                # Message Area for email
                dcc.Textarea(
                id='email-message-custom-projects',
                placeholder='Enter Email Message Here',
                style={'width': '100%', 'height': 300},
                ),

            ])

        ]),
        dcc.Tab(label='Find Person', children=[
        # Find Person Page
        # Input Box
        dcc.Input(id='user-name-placeholder', placeholder='Enter Username e.g. A1', type="text"),
        # Button to search username
        html.Button('Find Employee', id='button-find-employee'),

        html.Div(id="div-find-employee",children="Search Employee Details"),

        # Cards for user details
        html.Div(id='find-employee-cards')


        ])
    ])
])



@app.callback(
    Output('datatable-subtasks', 'data'),
    Input('save-data-button-subtasks', 'n_clicks'),
    State('username-placeholder-projects', 'value'),
    State('datatable-subtasks', 'data'),
    State('datatable-subtasks', 'columns')
)
def add_row_subtasks(n_clicks, input_value, rows, columns):
    """
    Updating rows when a new sub-task is added

    Parameters
    ----------
    n_clicks : int
        number of times save-data-button-subtasks has been clicked
    data : array
        contains updated data for subtasks table
    columns : list
        contains list of subtasks columns
    """
    if n_clicks > 0:
        rows.append({c['id']: '' for c in columns})
    return rows


@app.callback(
    Output('datatable-rows-projects', 'data'),
    Input('save-data-button-projects', 'n_clicks'),
    State('datatable-rows-projects', 'data'),
    State('datatable-rows-projects', 'columns'))
def add_row_projects(n_clicks, rows, columns):
    """
    Updating rows when a new project is added

    Parameters
    ----------
    n_clicks : int
        number of times save-data-button-projects has been clicked
    data : array
        contains updated data for project table
    columns : list
        contains list of project columns

    """
    if n_clicks > 0:
        rows.append({c['id']: '' for c in columns})
    return rows



@app.callback(
        Output("div-projects","children"),
        [Input("save-button-projects","n_clicks")],
        [State("datatable-rows-projects","data")]
        )

def update_projects_automated_email(nclicks,table1):
    """
    Automated email, to the current user, that the projects data-table and in-memory database has been modified

    Parameters
    ----------
    n_clicks : int
        number of times save-button-projects has been clicked
    table1 : array
        contains updated data for project table
    """
    username = request.authorization['username']
    if STATUS_PAIRS[username] == True:
        if nclicks == 0:
            raise PreventUpdate
        else:
            # Update Local CSV File for Projects
            object_project.update_data_csv(table1, 'projects.csv', False)
            # Update In-Memory Database for Projects

            object_project.update_data_in_memory(table1, 'Projects')

            # Update Local Database for projects
            conn = sql.connect('worksystem2.db')
            object_project.upload_data_local_database('projects', table1, conn)

            newDict = dict(filter(lambda elem: elem[0] == username,EMAIL_PAIRS.items()))
            receiver_email = newDict[username]
            message = """\
            Subject: Sucessfully Modified Projects

            You have successfully modified Projects data table, all team members will now be able to view any of the updates in the GUI.
            """
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, message)
            return "Data Submitted"
    else:
            return "Only a Manager or Admin can update this"


@app.callback(
        Output("div-subtasks","children"),
        [Input("save-button-projects-subtasks","n_clicks")],
        [State("datatable-subtasks","data")]
        )

def update_subtasks_automated_email(nclicks,table1):
    """
    Automated email, to the current user, that the subtasks data-table and in-memory database has been modified

    Parameters
    ----------
    n_clicks : int
        number of times save-button-projects-subtasks has been clicked
    table1 : array
        contains updated data for subtasks df
    """
    username = request.authorization['username']
    if nclicks == 0:
        raise PreventUpdate
    else:
        # Upsate Local CSV file for subtasks
        object_project.update_data_csv(table1, 'subtasks.csv', False)
        # Update In Memory Database for SubTask
        object_project.update_data_in_memory(table1, 'SubTasks')

        # Update Local Database For Subtasks
        conn = sql.connect('worksystem2.db')
        object_project.upload_data_local_database('subtasks', table1, conn)


        newDict = dict(filter(lambda elem: elem[0] == username,EMAIL_PAIRS.items()))
        receiver_email = newDict[username]
        message = """\
        Subject: Sucessfully Modified SubTasks

        You have successfully modified subtasks data table, all team members will now be able to view any of the updates in the GUI.

        """
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)
        return "Data Submitted"

@app.callback(
    Output('send-email-projects-div', 'children'),
    [Input('send-email-button-projects', 'n_clicks')],
    [State('username-placeholder-projects', 'value'),
    State('email-message-custom-projects', 'value')]
)
def send_email_projects(n_clicks, username, message):
    """
    Callback function used to send a custom email, to specific users to provide updates to projects tab

    Parameters
    ----------
    n_clicks : int
        number of times send-email-button-projects has been clicked
    username : str
        username, that has been entered within username-placeholder-projects
    message : str
        message typed into email-message-custom-projects to send in custom email
    """
    if n_clicks:
        newDict = dict(filter(lambda elem: elem[0] == username,EMAIL_PAIRS.items()))
        receiver_email = newDict[username]
        message = f"""\
        Subject: {username} Work Update

        {message}"""

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)
        return "Email Sent"


@app.callback(
    Output('send-email-subtasks-div', 'children'),
    [Input('send-email-button-subtasks', 'n_clicks')],
    [State('username-placeholder-subtasks', 'value'),
    State('email-message-custom-subtasks', 'value')]
)
def send_email_subtasks(n_clicks, username, message):
    """
    Callback function used to send a custom email, to specific users to provide updates to subtasks tab

    Parameters
    ----------
    n_clicks : int
        number of times send-email-button-subtasks has been clicked
    username : str
        username, that has been entered within username-placeholder-subtasks
    message : str
        message typed into email-message-custom-subtasks to send in custom email
    """
    if n_clicks:
        newDict = dict(filter(lambda elem: elem[0] == username,EMAIL_PAIRS.items()))
        receiver_email = newDict[username]
        message = f"""\
        Subject: {username} Work Update

        {message}"""
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)
        return "Email Sent"


@app.callback(
     Output("find-employee-cards", "children"),
    [Input('button-find-employee', 'n_clicks')],
    [State('user-name-placeholder', 'value')]
)
def find_employee_cards(n_clicks, username):
    """
    Callback function used to create display cards for individual username in last tab

    Parameters
    ----------
    n_clicks : int
        number of times button-find-employee has been clicked
    username : str
        username, that has been entered within user-name-placeholder
    """
    if n_clicks:
        DictEmail = dict(filter(lambda elem: elem[0] == username,EMAIL_PAIRS.items()))
        DictStatus = dict(filter(lambda elem: elem[0] == username,STATUS_CARD_PAIRS.items()))
        DictJob = dict(filter(lambda elem: elem[0] == username,JOB_PAIRS.items()))
        DictName = dict(filter(lambda elem: elem[0] == username,NAME_PAIRS.items()))


        email = DictEmail[username]
        status = DictStatus[username]
        job = DictJob[username]
        name = DictName[username]


        card1 = dbc.Card([
            dbc.CardBody([
                html.H4("Username"),
                html.P(username)
                ]
             )],
            style={'display': 'inline-block',
                   'width': '33.3%',
                   'text-align': 'center',
                   'color':'white',
                   'background-color': 'rgba(37, 150, 190)'},
            outline=True)

        card2 = dbc.Card([
            dbc.CardBody([
                html.H4("Name"),
                html.P(name)
                ]
             )],
            style={'display': 'inline-block',
                   'width': '33.3%',
                   'text-align': 'center',
                   'color':'white',
                   'background-color': 'rgba(37, 150, 190)'},
            outline=True)


        card3 = dbc.Card([
            dbc.CardBody([
                html.H4("Email"),
                html.P(email)
            ])
        ],
            style={'display': 'inline-block',
                   'width': '33.3%',
                   'text-align': 'center',
                   'color':'white',
                   'background-color': 'rgba(37, 150, 190)'},
            outline=True)



        card4 = dbc.Card([
            dbc.CardBody([
                html.H4("Job"),
                html.P(job)
                ]
             )],
            style={'display': 'inline-block',
                   'width': '33.3%',
                   'text-align': 'center',
                   'color':'white',
                   'background-color': 'rgba(37, 150, 190)'},
            outline=True)

        card5 = dbc.Card([
            dbc.CardBody([
                html.H4("Status"),
                html.P(status)
                ]
             )],
            style={'display': 'inline-block',
                   'width': '33.3%',
                   'text-align': 'center',
                   'color':'white',
                   'background-color': 'rgba(37, 150, 190)'},
            outline=True)

        return card1, card2, card3, card4, card5



if __name__ == '__main__':
    app.run_server(debug=True)
