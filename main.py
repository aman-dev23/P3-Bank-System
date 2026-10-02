import os
import json
import sqlite3
import bcrypt

connection = sqlite3.connect("accounts_data.db")
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS accounts (
account_no VARCHAR(10),
holder_name VARCHAR(10),
phone_no VARCHAR(10),
pin TEXT,
balance INT
)""")
# connection.close()

def hasg_pin(pin):
    return bcrypt.hashpw(
        pin.encode(),
        bcrypt.gensalt()
    ).decode()

def check_pin(pin, stored_hash):
    return bcrypt.checkpw(
        pin.encode(),
        stored_hash.encode()
    )


def add_account(account_no, name, phone_no, pin, balance):

    #SQL =================================
    cursor.execute("""
    INSERT INTO accounts VALUES (?, ?, ?, ?, ?)
    """, (account_no, name, phone_no, pin, balance))
    connection.commit()

    print(f"Account Created Successfully! \n Your Account no is {phone_no} \n Remember these information to access your account.\n")
    return

def view_details(account_no):
    cursor.execute("""
        SELECT * FROM accounts
        WHERE account_no = ?
    """, (account_no,))
    result = cursor.fetchone()

    if result is None:
        print('Account not found.')
        return

    print(f'''
< === Account Details for Acount No : {account_no} === >
    Name = {result[1]}
    Phone No = {result[2]}
    Balance = {result[4]}''')

def check_balance(account_no):
    cursor.execute("""
        SELECT balance FROM accounts
        WHERE account_no = ?
    """, (account_no,))
    result = cursor.fetchone()
    print(f"Balance : {result[0]}")

def deposit_money(account_no):
    try:
        amount = int(input("Enter the amount you want to deposit : "))
    except ValueError:
        print("Please Enter a valid amount!")
        return
    if amount <= 0:
        print("Can,t deposit 0 amount!")
        return
    #SQL ================================
    cursor.execute("""
        UPDATE accounts
        SET balance = balance + ?
        WHERE account_no = ?
    """, (amount, account_no))

    print(f" Amount {amount} Deposited into {account_no} successfully! ")

def withdraw_money(account_no):
    try:
        amount = int(input("Enter the amount you want to withdraw : "))
    except ValueError:
        print("Please Enter a valid amount!")
        return
    if amount <= 0:
        print("Can,t withdraw 0 amount!")
        return

    cursor.execute("""
        SELECT balance FROM accounts
        WHERE account_no = ?
    """, (account_no,))
    result = cursor.fetchone()
    if amount > result[0]:
            print("aukaat me ! itna to tere pass nahi hai 🤷‍♂️")
            return
    #SQL =============================
    cursor.execute("""
            UPDATE accounts
            SET balance = balance - ?
            WHERE account_no = ?
        """, (amount, account_no))

    print(f" Amount {amount} Withdrawn from {account_no} successfully!\n\tHere is your Cash 💸💸")

def transfer_money(account_no):
    receivers_account_no = input("Enter 10 digit account No where you want to transfer money : ")
    if not receivers_account_no.isdigit():
        print("Only numbers are allowed!")
        return
    if len(str(receivers_account_no)) != 10:
        print("Account no should contain 10 digits")
        return
    cursor.execute("""
        SELECT account_no FROM accounts
    """)
    result = cursor.fetchone()
    if receivers_account_no not in result:
        print(f"Account {receivers_account_no} not fount!")
        return
    if receivers_account_no == account_no:
        print("You cannot transfer money to yourself!")
        return
    try:
        amount = int(input(f"Enter the amount you want to transfer to {receivers_account_no} : "))
        cursor.execute("""
            SELECT balance FROM accounts
            WHERE account_no = ?
        """, (account_no,))
        result = cursor.fetchone()
        if amount > result[0]:
            print("aukaat me ! itna to tere pass hi nahi hai 🤷‍♂️")
            return
    except ValueError:
        print("Please Enter a valid amount!")
        return
    if amount <= 0:
        print("Can,t transfer 0 amount!")
        return

    #SQL ==========================================>
    cursor.execute("""
            UPDATE accounts
            SET balance = balance + ?
            WHERE account_no = ?
        """, (amount, receivers_account_no))

    cursor.execute("""
            UPDATE accounts
            SET balance = balance - ?
            WHERE account_no = ?
        """, (amount, account_no))

    print(f" Amount {amount} successfully transfered from {account_no} to {receivers_account_no}")

def login():
    while True:
        account_no = input("Enter your 10 digit Account number : ")
        if not account_no.isdigit():
            print("Only numbers are allowed!")
            continue
        if len(account_no) != 10:
            print("Account_no should be of 10 digits!")
            continue
        break
    cursor.execute("""
        SELECT account_no FROM accounts
        WHERE account_no = ?
    """, (account_no,))
    result = cursor.fetchone()
    if result is None:
        print("account no not registered first create an account!")
        return

    while True:
        pin = input("Enter your 4 digit pin : ")
        if not pin.isdigit():
            print("Only numbers allowed!")
            continue
        if len(pin) != 4:
            print("Pin should contain only 4 digits!")
            continue
        break
    cursor.execute("""
        SELECT pin FROM accounts
        WHERE account_no = ?
    """, (account_no,))
    result = cursor.fetchone()
    if check_pin(pin, result[0]):
        access(account_no)
    else:
        print("Wronge Pin!\n contect our Customer support if you forgoten your pin\n")
        return

def create_account():
    while True:
        name = input("Enter Your Full Name : ")
        if name.strip( ) == "":
            print("Name should not be Empty!")
            continue
        if name.replace(" ", "").isalpha():
            break
        else:
            print("Name should only contains Alphabets and spaces")
    while True:
        phone_no = input("Enter your 10 digit phone no : ")
        if not phone_no.isdigit():
            print("Only numbers are allowed!")
            continue
        if len(phone_no) != 10:
            print("Phone no should be of 10 digits")
            continue
        cursor.execute("""
            SELECT phone_no FROM accounts
            WHERE account_no = ?
        """, (phone_no,))
        result = cursor.fetchone()
        if result is not None:
            print("This Phone no is alredy linked to an account!")
            continue   
        break
    while True:
        pin = input("Set PIN for your Account : ")
        if not pin.isdigit():
            print("Only intergers allowed!")
            continue
        if len(pin) != 4:
            print("Pin should be of 4 digits")
            continue
        break
    pin = hasg_pin(pin)
    account_no = phone_no
    balance = 500
    add_account(account_no, name, phone_no, pin, balance)
 
def user():
    while True:
        try:
            user_choice1 = int(input('''
< ==== BANK MANAGMENT SYSTEM ==== >\n
   1. Log in
   2. Create account
(press 1 to Log in and 2 for Creating Account) : '''))
        except ValueError:
            print("Please Select 1 or 2 ")
            continue
        
        if user_choice1 == 1:
            login()
        elif user_choice1 == 2:
            create_account()

def access(account_no):
    cursor.execute("""
        SELECT holder_name FROM accounts
        WHERE account_no = ?
    """, (account_no,))
    result = cursor.fetchone()
    while True:
        user_choice2 = int(input(f'''
< == WELCOME {result[0]}! == >\n
    1. View details
    2. Check Balance
    3. deposit Money
    4. Withdraw Money
    5. Transfer Money
    6. Exit\n
(select 1/2/3/4/5 or 6 to Exit : )'''))

        if user_choice2 == 1:
            view_details(account_no)
        elif user_choice2 == 2:
            check_balance(account_no)
        elif user_choice2 == 3:
            deposit_money(account_no)
        elif user_choice2 == 4:
            withdraw_money(account_no)
        elif user_choice2 == 5:
            transfer_money(account_no)
        elif user_choice2 == 6:
            break
        else:
            print("Select valid option between 1/2/3/4/5 and 6")
            continue
user()