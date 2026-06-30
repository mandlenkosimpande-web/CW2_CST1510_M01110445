import bcrypt
import time 
import csv
import os 
import sqlite3, pandas as pd

from app_model.db import conn
from app_model.users import add_user, get_user

TXT_FILE = 'DATA/users.txt'

#Create TXT file if it doesn't exist
if not os.path.exists(TXT_FILE):
    with open(TXT_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['username', 'password', 'role']) 

#hashed by using bycrpt
def generates_hash(psw):
    bytes_psw = psw.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(bytes_psw, salt)
    return hashed.decode('utf-8')

#validating hash vs password
def is_valid_hash(psw, hash):
    hash_ = hash.encode('utf-8')
    byte_psw = psw.encode('utf-8')
    is_valid = bcrypt.checkpw(byte_psw, hash_)
    return is_valid

#user registration
def register_user(conn):
    username = input("Enter username: ").strip() #this first line will remove any leading or trailing whitespace from the username input
    role = input("Enter role (admin/user): ").strip().lower()

    if role not in ['admin', 'user']:
        print("Invalid role. Please enter 'admin' or 'user'.")
        return
    #checking if the username is empty afer the initial strip
    if not username:
        print("Username cannot contain spaces. Please enter a valid username.")
        return

#check if the username already exists 
    with open(TXT_FILE, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row ['username'] == username:#goes through every row under username and checks if there is a similar username.
                print("Username already exists. Please choose a different username.")
                return
            
    password = input ("Enter password: ")
    hashed = generates_hash(password)
    add_user(conn, username, hashed)


  


#user login 
def login_user(conn):
    username = input("Enter username: ").strip()
    user = get_user(conn, username)
    if not user:
        print("Username not found. Please register first.")
        return
    
    id, username, stored_hash, role = user
    print(f"WELCOME {username} !!")
    #Allow the user to enter password a max amount of 3 times
    max_attempts = 3

    for attempts in range(1, max_attempts + 1):
        password = input(f"Enter password attempt {attempts}/ {max_attempts}: ")


        if is_valid_hash(password, stored_hash):
            print(f"Login successful. Welcome, {username}!")
            #create a time stamp for the login attempts
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print(f"Login attempt timestamp: {timestamp}")
            return
        

        else:
            remaining_attempts = max_attempts - attempts
            if remaining_attempts > 0:
                print(f"Invalid password. You have {remaining_attempts} attempts left.")
            else:
                print("Maximum login attempts reached. Please try again later.")
                return
            
def main():            
    while True:
        print("\n WELCOME TO THE SYSTEM!!!")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            register_user(conn)
        elif choice == '2':
            login_user(conn)
        elif choice == '3':
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()




    





  








        


