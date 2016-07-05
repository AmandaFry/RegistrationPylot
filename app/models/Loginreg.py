from system.core.model import Model
from flask import Flask, flash, session
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
NOSPACE_REGEX = re.compile(r'^[a-zA-Z0-9]*$')
PW_REGEX = re.compile(r'^(?=.*?[A-Z])(?=.*?\d)[A-Za-z\d]{8,}$')

# EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
# NAME_REGEX = re.compile(r'^[a-zA-Z]*$')
                        #is there upper case, number, at least 8 charater
# PW_REGEX = re.compile(r'^(?=.*?[A-Z])(?=.*?\d)[A-Za-z\d]{8,}$')
# NOSPACE_REGEX = re.compile(r'^[a-zA-Z0-9]*$')

class Loginreg(Model):
    def __init__(self):
        super(Loginreg, self).__init__()
    """
    Below is an example of a model method that queries the database for all users in a fictitious application
    
    Every model has access to the "self.db.query_db" method which allows you to interact with the database

    def get_users(self):
        query = "SELECT * from users"
        return self.db.query_db(query)

    def get_user(self):
        query = "SELECT * from users where id = :id"
        data = {'id': 1}
        return self.db.get_one(query, data)

    def add_message(self):
        sql = "INSERT into messages (message, created_at, users_id) values(:message, NOW(), :users_id)"
        data = {'message': 'awesome bro', 'users_id': 1}
        self.db.query_db(sql, data)
        return True
    
    def grab_messages(self):
        query = "SELECT * from messages where users_id = :user_id"
        data = {'user_id':1}
        return self.db.query_db(query, data)

    """
    def get_all_users(self):
        print "I reached get_all_users model"
        query = "SELECT * from users"

        return self.db.query_db(query)

    def get_user_email(self, user_info):
        # This section processing user login info
        errors=[] #reset errors to blank

        #check to see if both field has at least two entry
        if len(user_info['email'])<2 or len(user_info['password'])<2:
            errors.append("email or password was too short")
        #check to see if email has an email format
        elif not EMAIL_REGEX.match(user_info['email']):
            errors.append("Please enter a valid email format")
        # check to see if any of the entry is only spaces
        elif not NOSPACE_REGEX.match(user_info['password']):
            errors.append("Email or password did not match")
        if errors:
            #if found error than send back a dictionary for status False and the error message
            return {"status": False, "errors": errors}
        else:
            #the initial check to send infor to database passed now prefomaning access to the db.
            #pulls the information it needs for user_info to perform the db qurey 
            data = {'email': user_info['email']}
            #the query to db
            query = "SELECT * FROM users WHERE email = :email"
            #execting the the db, once excuted users is populated but not returned to contoroller yet
            # I still need to do a return to send the info back to the controller
            users = self.db.query_db(query, data)

            #if the users are 0 length than it did not find the entr in the db. Tis check should
            #be done before checking password
            if len(users) == 0:
                errors.append("User was not found please register")
            #check to see if the password is matches what was typed in
            # elif not self.bcrypt.check_password_hash(users[0]['password'],user_info['password']):
            #     errors.append('Incorrect password - login was not successful')
                return {"status": False, "errors": errors}
            else:
                #the user exist and the password matched return the status True and users information
                return {"status": True, "users": users[0] }

