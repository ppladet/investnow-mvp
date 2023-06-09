"""
register.py: This module provides the Register class, which is responsible for registering 
new users to the InvestNow application. It handles the user prompt for registration and 
writes new user data to a JSON file.
"""

import json

class Register:
    """
    The Register class, responsible for registering new users to the InvestNow application.
    This includes checking if a username already exists, prompting for user credentials, 
    and writing the new user data to a JSON file.
    """

    def __init__(self):
        """
        Initialize the Register class.
        Load the user data from the users.json file into a dictionary.
        If the file is not found, an empty dictionary is created instead.
        """
        self.file = 'users.json'
        self.users = self.load_users()

    def load_users(self):
        """
        Load the user data from the users.json file into a dictionary.
        If the file is not found or invalid, an empty dictionary is created instead.
        """
        try:
            with open(self.file, encoding='utf-8') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def prompt_username(self):
        """
        Prompt the user to enter their username.
        """
        while True:
            username = input("Enter your username: ")
            if username.strip():
                return username
            else:
                print("\nUsername cannot be empty. Please enter a valid username.")

    def prompt_password(self):
        """
        Prompt the user to enter their password.
        """
        while True:
            password = input("Enter your password: ")
            if password.strip():
                return password
            else:
                print("\nPassword cannot be empty. Please enter a valid password.")

    def prompt_email(self):
        """
        Prompt the user to enter their email.
        """
        while True:
            email = input("Enter your email: ")
            if email.strip():
                return email
            else:
                print("\nEmail cannot be empty. Please enter a valid email.")

    def prompt_continue(self):
        """
        Ask the user whether to continue or quit.
        """
        while True:
            continue_choice = input("Would you like to continue? (Y/N): ").lower()
            if continue_choice == 'y':
                break
            elif continue_choice == 'n':
                raise SystemExit
            else:
                print("\nInvalid choice. Please enter Y or N.")

    def prompt_user(self):
        """
        Prompt the user to enter their credentials for registration.
        If the entered username already exists in the users dictionary, 
        the user is asked to try again with a different username.
        After successful registration, the user is given a choice to continue or quit.
        """
        print("\nInvestNow - Registration")  # Display welcome message.

        while True:
            username = self.prompt_username()
            if username in self.users:
                print("\nUsername already taken. Please try another one.")
            else:
                break

        password = self.prompt_password()
        email = self.prompt_email()

        # Add user data to the dictionary.
        self.users[username] = {"password": password, "email": email, "stocks": []}

        with open(self.file, 'w', encoding='utf-8') as file:
            json.dump(self.users, file)

        print("\nRegistration successful. Welcome to InvestNow.")

        self.prompt_continue()
