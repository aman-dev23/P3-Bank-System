import os
import json

path = os.path.dirname(__file__)
json_file = os.path.join(path, "accounts_data.json")

def load_accounts():
    with open(json_file, "r") as file:
        return json.load(file)
def dump_accounts():
    with open(json_file, "w") as file:
        json.dump(temp_accounts, file, indent=4)

temp_accounts = load_accounts()

def add_account(name, phone_no, pin):
    temp_accounts[phone_no] = {
        "holder_name" : name,
        "phone_no" : phone_no,
        "pin" : pin,
        "balance" : 0
    }
    dump_accounts()
    print(f"Account Created Successfully! \n Your Account no is {phone_no} and Pin is {pin}\n Remember these information to access your account.\n")
    return

def view_details(account_no):
    print(f'''
< === Account Details for Acount No : {account_no} === >
    Name = {temp_accounts[account_no]["holder_name"]}
    Phone No = {temp_accounts[account_no]["phone_no"]}
    Pin = {temp_accounts[account_no]["pin"]}
    Balance = {temp_accounts[account_no]["balance"]}''')

def check_balance(account_no):
    print(f"Balance : {temp_accounts[account_no]["balance"]}")

def deposit_money(account_no):
    try:
        amount = int(input("Enter the amount you want to deposit : "))
    except ValueError:
        print("Please Enter a valid amount!")
        return
    if amount <= 0:
        print("Can,t deposit 0 amount!")
        return
    temp_accounts[account_no]["balance"] += amount
    dump_accounts()
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
    if amount > temp_accounts[account_no]["balance"]:
            print("aukaat me ! itna to tere pass hi nahi hai 🤷‍♂️")
            return
    temp_accounts[account_no]["balance"] -= amount
    dump_accounts()
    print(f" Amount {amount} Withdrawn from {account_no} successfully!\n\tHere is your Cash 💸💸")

def transfer_money(account_no):
    receivers_account_no = input("Enter 10 digit account No where you want to transfer money : ")
    if not receivers_account_no.isdigit():
        print("Only numbers are allowed!")
        return
    if len(str(receivers_account_no)) != 10:
        print("Account no should contain 10 digits")
        return
    if receivers_account_no not in temp_accounts:
        print(f"Account {receivers_account_no} not fount!")
        return
    if receivers_account_no == account_no:
        print("You cannot transfer money to yourself!")
        return
    try:
        amount = int(input(f"Enter the amount you want to transfer to {receivers_account_no} : "))
        if amount > temp_accounts[account_no]["balance"]:
            print("aukaat me ! itna to tere pass hi nahi hai 🤷‍♂️")
            return
    except ValueError:
        print("Please Enter a valid amount!")
        return
    if amount <= 0:
        print("Can,t transfer 0 amount!")
        return
    temp_accounts[account_no]["balance"] -= amount
    temp_accounts[receivers_account_no]["balance"] += amount
    dump_accounts()
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
    
    if account_no not in temp_accounts:
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
            
    if pin == temp_accounts[account_no]["pin"]:
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
        if phone_no in temp_accounts:
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

    add_account(name, phone_no, pin)
 
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
    while True:
        user_choice2 = int(input(f'''
< == WELCOME {temp_accounts[account_no]["holder_name"]}! == >\n
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