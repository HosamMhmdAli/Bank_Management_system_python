import sqlite3
from tkinter import *
import datetime

#--------------------------------Database Managing-----------------------------------------------------------
db = sqlite3.connect(r"/media/albraa/Pop/Files/Accounts_Version_1.db")

cr = db.cursor()
# cr.execute("CREATE TABLE accounts (id INTEGER PRIMARY KEY AUTOINCREMENT, first_name TEXT NOT NULL, middle_name TEXT NOT NULL, last_name TEXT NOT NULL, password TEXT NOT NULL, balance INTEGER NOT NULL, created_date DATE NOT NULL, updated_time DATE) ")

def create_account(fn, mn, ln, p, b):
    try :
        if b > 0:
            cr = db.cursor()
            t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cr.execute("INSERT INTO accounts (first_name, middle_name, last_name, password, balance, created_date) VALUES (?, ?, ?, ?, ?, ?)", (fn, mn, ln, p, b, t))
            db.commit()
            cr.execute("SELECT id FROM accounts WHERE first_name = ? and middle_name = ? and last_name = ? and password = ?", (fn,mn,ln,p,))
            i = cr.fetchone()
            cr.close()
            return f"Mission Success, Account Has Been Created\nYour Id Is {i[0]}"
        else:
            return "Balance Is Invalid Amount"
    except:
        return("Mission Failed")

def delete_account(i, p):
    try :
        cr = db.cursor()
        cr.execute("SELECT password FROM accounts WHERE id = ?", (i,))
        record = cr.fetchone()
        if record == None:
            return("Id That You Entered Is Wrong")
        else:
            if record[0] == p:
                cr.execute("DELETE FROM accounts WHERE id = ?", (i,))
                db.commit()
                cr.close()
                return("Mission Success, Account Has Been Deleted")
            else :
                return("Password That You Entered Is Wrong")
    except:
        return("Mission Failed")

def deposit_operation(i, p, amount):
    try :
        cr = db.cursor()
        cr.execute("SELECT balance, password FROM accounts WHERE id = ?", (i,))
        record = cr.fetchone()
        if record == None:
            return "Id That You Entered Is Wrong"
        else:
            if record[1] == p:
                if isinstance(amount, int):
                    if amount > 0:
                        bal = record[0] + amount
                        t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        cr.execute("UPDATE accounts SET balance = ?, updated_time = ? WHERE id = ?", (bal, t, i))
                        db.commit()
                        cr.close()
                        return f"Mission Success, Your Balance Is {bal}"
                    else :
                        return "Invalid Amount"
                else :
                    return "Amount Is Invalid"
            else :
                return "Password That You Entered Is Wrong"
    except:
        return "Mission Failed"

def withdraw_operation(i, p, amount):
    try :
        cr = db.cursor()
        cr.execute("SELECT balance, password FROM accounts WHERE id = ?", (i,))
        record = cr.fetchone()
        if record == None:
            return "Id That You Entered Is Wrong"
        else:
            if record[1] == p:
                if isinstance(amount, int):
                    if amount > 0 and record[0] >= amount:
                        bal = record[0] - amount
                        t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        cr.execute("UPDATE accounts SET balance = ?, updated_time = ? WHERE id = ?", (bal, t, i))
                        cr.close()
                        db.commit()
                        return f"Mission Success, Your Balance Is {bal}"
                    else :
                        return "Invalid Amount"
                else :
                    return "Amount Is Invalid"
            else :
                return "Password That You Entered Is Wrong"
    except:
        return "Mission Failed"

def check_balance(i, p):
    try :
        cr = db.cursor()
        cr.execute("SELECT balance, password FROM accounts WHERE id = ?", (i,))
        record = cr.fetchone()
        if record == None:
            return ("Id That You Entered Is Wrong")
        else:
            if record[1] == p:
                return (f"Your Balance Is {record[0]}")
            else :
                return ("Password That You Entered Is Wrong")
    except:
        return ("Mission Failed")

def modify_name(i, p, fn, mn, ln):
    try :
        cr = db.cursor()
        cr.execute("SELECT password FROM accounts WHERE id = ?", (i,))
        record = cr.fetchone()
        if record == None:
            return "Id That You Entered Is Wrong"
        else:
            if record[0] == p:
                t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                cr.execute("UPDATE accounts SET first_name = ?, middle_name = ?, last_name = ?, updated_time = ? WHERE id = ?", (fn, mn, ln,t,i,))
                db.commit()
                cr.close()
                return "Mission Success, Name Has Been Updated"
            else :
                return "Password That You Entered Is Wrong"
    except:
        return "Mission Failed"


#--------------------------------TK-----------------------------------------------------------
main = Tk()
main.title("Bank Management System")
main.geometry("1220x760")   #set size of window
main.resizable(False, False)        
# main.configure(bg="#000000")       #set the backgrounf color

options = '''
1- Create An Account.
2- Delete An Account.
3- Deposit.
4- Withdraw.
5- Chech Balance.
6- Modify An Account Name.
'''

screen = Label(main, width=30, height=8, text=options, font=("Times New Roman", 25, "bold"))
screen.config(anchor=W)
screen.config(justify=LEFT)
# screen.config(bg="#130f40", fg="#dff9fb")
screen.place(x=360, y=60)

# Create a label to prompt the user for input
label = Label(main, text="Enter your option:", width=20)
label.place(x=542, y=400)

# Create an Entry widget for the user to enter their name
entry = Entry(main, width=20)
entry.place(x=542, y=460)

def take_action():
    option = entry.get() 
    # print(option)
    if option == '1':
        create()
        entry.delete(0, END)
    elif option == '2':
        delete()
        entry.delete(0, END)
    elif option == '3':
        deposit()
        entry.delete(0, END)
    elif option == '4':
        withdraw()
        entry.delete(0, END)
    elif option == '5':
        check()
        entry.delete(0, END)
    elif option == '6':
        modify()
        entry.delete(0, END)
    else:
        error = Label(main, text="Enter A Valid Option", width=20)
        error.place(x=542, y=520)
        entry.delete(0, END)

Button(main, text="EXIT", font=("arial", 30, "bold"), bd=1, fg="#fff", bg="#3697f5", command=main.quit).place(x=405, y=580)
ok = Button(main, text=" OK ", font=("arial", 30, "bold"), bd=1, fg="#fff", bg="#3697f5", command=lambda: take_action()).place(x=730, y=580)

#''''''''''''''''''''''''''''''''''''''''Modify Window'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
def modify():
    modify_window = Toplevel(main)
    modify_window.title("Modify Name")
    modify_window.geometry("350x300")
    # main.withdraw()
    modify_window.deiconify()

    Label(modify_window, text="Your Id", width=30).pack()
    id = Entry(modify_window, width=30, font=("Arial", 12))
    # id.insert(0, "Id") 
    id.pack()

    Label(modify_window, text="Your Password", width=30).pack()
    password = Entry(modify_window, width=30, font=("Arial", 12))
    # password.insert(0, "Password") 
    password.pack()

    Label(modify_window, text="First Name", width=30).pack()
    new_fname = Entry(modify_window, width=30, font=("Arial", 12))
    # new_fname.insert(0, "First Name") 
    new_fname.pack()

    Label(modify_window, text="Middle Name", width=30).pack()
    new_mname = Entry(modify_window, width=30, font=("Arial", 12))
    # new_mname.insert(0, "Middle Name") 
    new_mname.pack()

    Label(modify_window, text="Last Name", width=30).pack()
    new_lname = Entry(modify_window, width=30, font=("Arial", 12))
    # new_lname.insert(0, "Last Name") 
    new_lname.pack()

    Button(modify_window, text="OK", font=("arial", 30, "bold"), bd=1, fg="#fff", bg="#3697f5", command=lambda: modify_msg()).pack()

    def modify_msg():
        modify_msg_window = Toplevel(modify_window)
        modify_msg_window.title("Modify Name")
        modify_msg_window.geometry("350x300")
        modify_window.withdraw()
        modify_msg_window.deiconify()

        i = id.get()
        p = password.get()
        fn = new_fname.get()
        mn = new_mname.get()
        ln = new_lname.get()

        message = modify_name(i, p, fn, mn, ln)

        msg = Label(modify_msg_window)
        msg.config(text=message)
        msg.pack()

        Button(modify_msg_window, text="BACK", font=("arial", 30, "bold"), bd=1, fg="#fff", bg="#3697f5", command=lambda: close_modify_msg()).pack()

        def close_modify_msg():
            modify_msg_window.destroy()
            main.deiconify()


#''''''''''''''''''''''''''''''''''''''''Deposit Window'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
def deposit():
    deposit_window = Toplevel(main)
    deposit_window.title("Deposit Operation")
    deposit_window.geometry("350x300")
    # main.withdraw()
    deposit_window.deiconify()

    Label(deposit_window, text="Your Id", width=30).pack()
    id = Entry(deposit_window, width=30, font=("Arial", 12))
    # id.insert(0, "Id") 
    id.pack()

    Label(deposit_window, text="Your Password", width=30).pack()
    password = Entry(deposit_window, width=30, font=("Arial", 12))
    # password.insert(0, "Password") 
    password.pack()

    Label(deposit_window, text="Amount", width=30).pack()
    amount = Entry(deposit_window, width=30, font=("Arial", 12))
    # amount.insert(0, "Amount") 
    amount.pack()

    Button(deposit_window, text="OK", font=("arial", 30, "bold"), bd=1, fg="#fff", bg="#3697f5", command=lambda: deposit_msg()).pack()

    def deposit_msg():
        deposit_msg_window = Toplevel(deposit_window)
        deposit_msg_window.title("Deposit Operation")
        deposit_msg_window.geometry("350x300")
        deposit_window.withdraw()
        deposit_msg_window.deiconify()

        i = id.get()
        p = password.get()
        message = ""

        try :
            a = int(amount.get())
            message = deposit_operation(i, p, a)
        except:
            message = "Amount Isn't Valid"

        msg = Label(deposit_msg_window)
        msg.config(text=message)
        msg.pack()

        Button(deposit_msg_window, text="BACK", font=("arial", 30, "bold"), bd=1, fg="#fff", bg="#3697f5", command=lambda: close_deposit_msg()).pack()

        def close_deposit_msg():
            deposit_msg_window.destroy()
            main.deiconify()


#''''''''''''''''''''''''''''''''''''''''Withhdraw Window'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
def withdraw():
    withdraw_window = Toplevel(main)
    withdraw_window.title("Withhdraw Operation")
    withdraw_window.geometry("350x300")
    # main.withdraw()
    withdraw_window.deiconify()

    Label(withdraw_window, text="Your Id", width=30).pack()
    id = Entry(withdraw_window, width=30, font=("Arial", 12))
    # id.insert(0, "Id") 
    id.pack()

    Label(withdraw_window, text="Your Password", width=30).pack()
    password = Entry(withdraw_window, width=30, font=("Arial", 12))
    # password.insert(0, "Password") 
    password.pack()

    Label(withdraw_window, text="Amount", width=30).pack()
    amount = Entry(withdraw_window, width=30, font=("Arial", 12))
    # amount.insert(0, "Amount") 
    amount.pack()

    Button(withdraw_window, text="OK", font=("arial", 30, "bold"), bd=1, fg="#fff", bg="#3697f5", command=lambda: withdraw_msg()).pack()

    def withdraw_msg():
        withdraw_msg_window = Toplevel(withdraw_window)
        withdraw_msg_window.title("Withhdraw Operation")
        withdraw_msg_window.geometry("350x300")
        withdraw_window.withdraw()
        withdraw_msg_window.deiconify()

        i = id.get()
        p = password.get()
        message = ""

        try :
            a = int(amount.get())
            message = withdraw_operation(i, p, a)
        except:
            message = "Amount Isn't Valid"

        msg = Label(withdraw_msg_window)
        msg.config(text=message)
        msg.pack()

        Button(withdraw_msg_window, text="BACK", font=("arial", 30, "bold"), bd=1, fg="#fff", bg="#3697f5", command=lambda: close_withdraw_msg()).pack()

        def close_withdraw_msg():
            withdraw_msg_window.destroy()
            main.deiconify()


#''''''''''''''''''''''''''''''''''''''''Check Window'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
def check():
    check_window = Toplevel(main)
    check_window.title("Check Operation")
    check_window.geometry("350x300")
    # main.withdraw()
    check_window.deiconify()

    Label(check_window, text="Your Id", width=30).pack()
    id = Entry(check_window, width=30, font=("Arial", 12))
    # id.insert(0, "Id") 
    id.pack()

    Label(check_window, text="Your Password", width=30).pack()
    password = Entry(check_window, width=30, font=("Arial", 12))
    # password.insert(0, "Password") 
    password.pack()

    Button(check_window, text="OK", font=("arial", 30, "bold"), bd=1, fg="#fff", bg="#3697f5", command=lambda: check_msg()).pack()

    def check_msg():
        check_msg_window = Toplevel(check_window)
        check_msg_window.title("Check Operation")
        check_msg_window.geometry("350x300")
        check_window.withdraw()
        check_msg_window.deiconify()

        i = id.get()
        p = password.get()
        message = check_balance(i, p)

        msg = Label(check_msg_window)
        msg.config(text=message)
        msg.pack()

        Button(check_msg_window, text="BACK", font=("arial", 30, "bold"), bd=1, fg="#fff", bg="#3697f5", command=lambda: close_check_msg()).pack()

        def close_check_msg():
            check_msg_window.destroy()
            main.deiconify()



#''''''''''''''''''''''''''''''''''''''''Delete Window'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
def delete():
    delete_window = Toplevel(main)
    delete_window.title("Delete operation")
    delete_window.geometry("350x300")
    # main.withdraw()
    delete_window.deiconify()

    Label(delete_window, text="Your Id", width=30).pack()            
    id = Entry(delete_window, width=30, font=("Arial", 12))
    # id.insert(0, "Id") 
    id.pack()

    Label(delete_window, text="Your Password", width=30).pack() 
    password = Entry(delete_window, width=30, font=("Arial", 12))
    # password.insert(0, "Password") 
    password.pack()

    Button(delete_window, text="OK", font=("arial", 30, "bold"), bd=1, fg="#fff", bg="#3697f5", command=lambda: delete_msg()).pack()

    def delete_msg():
        delete_msg_window = Toplevel(delete_window)
        delete_msg_window.title("Delete Operatin'")
        delete_msg_window.geometry("350x300")
        delete_window.withdraw()
        delete_msg_window.deiconify()

        i = id.get()
        p = password.get()
        message = delete_account(i, p)

        msg = Label(delete_msg_window)
        msg.config(text=message)
        msg.pack()

        Button(delete_msg_window, text="BACK", font=("arial", 30, "bold"), bd=1, fg="#fff", bg="#3697f5", command=lambda: close_delete_msg()).pack()

        def close_delete_msg():
            delete_msg_window.destroy()
            main.deiconify()


#''''''''''''''''''''''''''''''''''''''''Craete Window'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
def create():
    create_window = Toplevel(main)
    create_window.title("Craete Operation")
    create_window.geometry("350x300")
    # main.withdraw()
    create_window.deiconify()

    Label(create_window, text="First Name", width=30).pack() 
    fname = Entry(create_window, width=30, font=("Arial", 12))
    # fname.insert(0, "First Name") 
    fname.pack()

    Label(create_window, text="Middle Name", width=30).pack() 
    mname = Entry(create_window, width=30, font=("Arial", 12))
    # mname.insert(0, "Middle Name") 
    mname.pack()

    Label(create_window, text="Last Name", width=30).pack() 
    lname = Entry(create_window, width=30, font=("Arial", 12))
    # lname.insert(0, "Last Name") 
    lname.pack()

    Label(create_window, text="Password", width=30).pack() 
    password = Entry(create_window, width=30, font=("Arial", 12))
    # password.insert(0, "Password") 
    password.pack()

    Label(create_window, text="Balance", width=30).pack() 
    balance = Entry(create_window, width=30, font=("Arial", 12))
    # balance.insert(0, "Balance") 
    balance.pack()

    Button(create_window, text="OK", font=("arial", 30, "bold"), bd=1, fg="#fff", bg="#3697f5", command=lambda: create_msg()).pack()

    def create_msg():
        create_msg_window = Toplevel(create_window)
        create_msg_window.title("Craete Operation")
        create_msg_window.geometry("350x300")
        create_window.withdraw()
        create_msg_window.deiconify()

        fn = fname.get()
        mn = mname.get()
        ln = lname.get()
        p = password.get()
        message = ""

        try :
            a = int(balance.get())
            message = create_account(fn, mn, ln, p, a)
        except:
            message = "Balance Isn't Valid"

        msg = Label(create_msg_window)
        msg.config(text=message)
        msg.pack()

        Button(create_msg_window, text="BACK", font=("arial", 30, "bold"), bd=1, fg="#fff", bg="#3697f5", command=lambda: close_create_msg()).pack()

        def close_create_msg():
            create_msg_window.destroy()
            main.deiconify()

main.mainloop()