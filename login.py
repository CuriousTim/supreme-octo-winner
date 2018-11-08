"""
Presents the login screen for the application. This should be the entry point
of the application from the perspective of the end user. The page prompts for a
username and password and verifies the credentials.
"""

import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
from user import UserManager

class SampleApp(tk.Tk):
    """Controller for the login screen

    Creates and displays the view for the login screen. Provides
    authentication and routes the user according to whether or not authentication
    was successful.
    """

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold")
        self.title("EHRS")

        container = ttk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)

        self.frames = {}
        for page in (LoginPage, LoggedInPage, LoginFailPage,
                     CreateNewUserPage):
            page_name = page.__name__
            frame = page(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        frame = self.frames["LoginPage"]
        frame.tkraise()

        """Database collection."""
        self.db = UserManager("./users.db")
        """Create an initial user."""
        self.create_new_user("root", "password")

    def authenticate(self, username, password):
        """Authenticates a username and password.

        Checks a user database for username and verifies that the given
        password belongs to username.

        Args:
        username - username to verify
        password - password to verify
        """

        if (self.db.verifyPassword(username, password)):
            frame = self.frames["LoggedInPage"]
            frame.tkraise()
        else:
            frame = self.frames["LoginFailPage"]
            frame.tkraise()

    def create_new_user(self, username, password):
        """Creates a new user.

        Creates a new user and adds the credentials to a database if the
        username does not already exists.

        Args:
        username - username of the new user
        password - password of the new user
        """
        self.db.createUser(username, password)


    def go_to_login(self):
        """ Presents the login page."""

        frame = self.frames["LoginPage"]
        frame.tkraise()

    def go_to_create_user(self):
        """Presents the page to create new users."""

        frame = self.frames["CreateNewUserPage"]
        frame.tkraise()

class LoginPage(ttk.Frame):
    """Constructs the login page."""

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        username = tk.StringVar()
        password = tk.StringVar()

        username_entry = ttk.Entry(self, width=7, textvariable=username)
        username_entry.grid(column=2, row=1, sticky=("we"))

        password_entry = ttk.Entry(self, width=7, show="*", textvariable=password)
        password_entry.grid(column=2, row=2, sticky=("we"))

        ttk.Label(self, text="User Name").grid(column=1, row=1, sticky="w")
        ttk.Label(self, text="Password").grid(column=1, row=2, sticky="w")

        submit_btn = ttk.Button(self, text="Login", command=lambda:
                                controller.authenticate(username, password))
        submit_btn.grid(column=2, row=3, sticky="es")

class LoggedInPage(ttk.Frame):
    """Constructs page for successful logins."""

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        label = ttk.Label(self, text="Success!", font=controller.title)
        label.pack(side="top", fill="x", pady=10)
        logout_btn = ttk.Button(self, text="Logout",
                            command=lambda: controller.go_to_login())
        create_user_btn = ttk.Button(self, text="Logout",
                            command=lambda: controller.go_to_create_user())
        logout_btn.pack()
        create_user_btn.pack()


class CreateNewUserPage(ttk.Frame):
    """Constructs page for registering new users."""

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        username = tk.StringVar()
        password = tk.StringVar()

        username_entry = ttk.Entry(self, width=7, textvariable=username)
        username_entry.grid(column=2, row=1, sticky=("we"))

        password_entry = ttk.Entry(self, width=7, show="*", textvariable=password)
        password_entry.grid(column=2, row=2, sticky=("we"))

        ttk.Label(self, text="User Name").grid(column=1, row=1, sticky="w")
        ttk.Label(self, text="Password").grid(column=1, row=2, sticky="w")

        submit_btn = ttk.Button(self, text="Create User", command=lambda:
                                controller.create_new_user(username, password))
        submit_btn.grid(column=2, row=3, sticky="es")


class LoginFailPage(ttk.Frame):
    """Constructs the page for failed logins."""
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        label = ttk.Label(self, text="WRONG!", font=controller.title)
        label.pack(side="top", fill="x", pady=10)
        button = ttk.Button(self, text="Try Again",
                            command=lambda: controller.go_to_login())
        button.pack()

if __name__ == "__main__":
    APP = SampleApp()
    APP.mainloop()
