README 

DESCRIPTION:
    The Notice Board application provides tutors to share important updates and changes for their student's courses 
    ensuring that students are up to date with all information for their studies. 


INSTALLATION:
    The application requires the following libraries to be installed:
        datetime
        flask_login
        flask
        pytest
        requests


    During development the application was run using a virtual environment with the following packages installed:
    
        atomicwrites 1.4.0  
        attrs        21.4.0 
        click        8.0.3  
        colorama     0.4.4  
        Flask        2.0.2  
        Flask-Login  0.5.0  
        iniconfig    1.1.1  
        itsdangerous 2.0.1  
        Jinja2       3.0.3  
        MarkupSafe   2.0.1  
        packaging    21.3   
        pip          22.0.3
        pluggy       1.0.0
        py           1.11.0
        pyparsing    3.0.7
        pytest       7.0.0
        tomli        2.0.1
        Werkzeug     2.0.2

        [Python 3.9.10 was used during development]


EXECUTION:
    To start the application execute the run.py file.

    Once the application has loaded, you will be redirected to the login page (http://127.0.0.1:5000/login)

    Currently there are two users who are approved to login:
        Tutor: ID: U1010101, Password: tutor
        Student: ID: U1930545, Password: student

    Once logged in the user will be redirected to the Notice Board Home Page


PAGE FEATURES:
    The following text provides information about functionality on each page depending on admin status:

    Notice Board Home Page:
        Tutor:
            Create New Boards
            Modify Existing Boards
            Delete Boards 
            Open Boards

        Student:
            Open Boards

    Notice List Page:
        Tutor:
            Create New Notices
            Modify Existing Notices
            Delete Notices
            Open Notices
        Student:
            Open Notices

    Comment Page:
        Tutor:
            Open Comments
        Student:
            Create New Comment
            Open Comments

    Replies Page:
        Tutor:
            Reply to Comments
        Student:
            View Comment Replies 