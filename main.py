import tkinter as Tk
import tkinter.messagebox as msg
from window import Welcome
import sqlite3
import bcrypt

class Login(Tk.Tk):
    """this class creates a window for a login"""
    def __init__(self):
        super().__init__()

        self.conn = sqlite3.connect('myData.db')
        self.cur = self.conn.cursor()

        # creates the main window
        self.title('Login Page')
        self.resizable(0,0)
        self.geometry("330x250")
        self.config(bg="white")

        # create labels and entries for username and password
        self.username_lbl = Tk.Label(self, font="Garamond", text="Username:")
        self.username_lbl.place(x=35, y=75)
        self.username_ent = Tk.Entry(self, font="Garamond")
        self.username_ent.place(x=125, y=75)

        self.password_lbl = Tk.Label(self, font="Garamond", text="Password:")
        self.password_lbl.place(x=35, y=125)
        self.password_ent = Tk.Entry(self,font="Garamond", show="*")
        self.password_ent.place(x=125, y=125)

        # create buttons for login and sign up
        self.login_button = Tk.Button(self, font="Garamond", text='Login', command=self.Validate_Login)
        self.login_button.place(x=165, y=180)
        self.signup_button = Tk.Button(self, font="Garamond", text='Signup', command=self.Validate_Signup)
        self.signup_button.place(x=230, y=180)

    #validates the sign up to save their username and password in the database
    def Validate_Signup(self):
        username = self.username_ent.get()
        password = self.password_ent.get()

        if username == '' or password == '':
            msg.showerror('Error', 'Username or password is incorrect')
        else:
            self.cur.execute("SELECT * FROM loginApp WHERE username=?", (username,))
            result = self.cur.fetchone()

            if result is None:
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

                enterThese = (username, hashed_password)
                self.cur.execute("INSERT into loginApp VALUES(?,?)", (enterThese))
                self.conn.commit()

                msg.showinfo('Success', 'You have successfully signed up!')
            else:
                msg.showerror('Error', 'Username already in use')

    #validates the login to see if the username and passowrd entered, exists in the database
    def Validate_Login(self):
        username = self.username_ent.get()
        password = self.password_ent.get()

        if username == '' or password == '':
            msg.showerror('Error', 'Username or password is incorrect')
        else:
            self.cur.execute("SELECT * FROM loginApp WHERE Username=?", (username,))
            result = self.cur.fetchone()

            if result is None:
                msg.showerror('Error', 'Username or password is incorrect')
            else:
                if bcrypt.checkpw(password.encode('utf-8'), result[1]):
                    myWelcome = Welcome(self.conn, self.cur).setBanner(self.username_ent.get())
                    self.withdraw()
                else:
                    msg.showerror('Error', 'Username or password is incorrect')

if __name__ == '__main__':
    myApp = Login()
    myApp.mainloop()