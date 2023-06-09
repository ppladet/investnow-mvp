"""
login.py: This module provides the Login class, which is responsible for handling 
user logins for the InvestNow application. It prompts the user for their credentials, 
verifies them against stored user data in a JSON file, and if the login is successful, 
it gives the user access to their profile, portfolio analysis, and trading algorithm options.
"""

import json
from my_profile import MyProfile
from portfolio_analysis import PortfolioAnalysis
from trading_algorithm import TradingAlgorithm
from session import Session


class Login:
    """Class to handle login operations."""

    def __init__(self, session: Session):
        """Initialize the Login object and load users."""
        self.session = session
        self.user_file = 'users.json'
        self.users = self.load_users()

    def load_users(self):
        """Load the user data from a json file."""
        try:
            with open(self.user_file, encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def user_menu(self):
        """Display the user menu and handle the user's choice."""
        profile = MyProfile(self.session)
        portfolio_analysis = PortfolioAnalysis(self.session)
        trading_algorithm = TradingAlgorithm(self.session)

        while True:
            print("\nInvestNow - Democratize Investing")
            print("1. Profile")
            print("2. Portfolio Analysis")
            print("3. Trading Algorithm")
            print("4. Logout")

            choice = input("Enter your choice: ")

            if choice == "1":
                profile.prompt_user()
            elif choice == "2":
                portfolio_analysis.prompt_user()
            elif choice == "3":
                trading_algorithm.prompt_user()
            elif choice == "4":
                print("\nLogging out.")
                break
            else:
                print("\nInvalid choice. Please enter a number between 1 and 4.")

    def prompt_user(self):
        """Prompt the user for their username and password."""
        print("\nInvestNow - Login")  # Display welcome message

        while True:
            self.users = self.load_users()  # Reload user data from the file
            username = input("\nEnter your username: ")
            if username in self.users:
                password = input("Enter your password: ")
                if self.users[username]["password"] == password:
                    print("\nLogin successful.")
                    self.session.set_current_user(username)  # Save user data in session
                    self.user_menu()
                    break
                else:
                    print("\nIncorrect password. Please select an option.")
            else:
                print("\nUsername not found. Please select an option.")

            # After an incorrect input, present options
            print("\nOptions:")
            print("1. Retry")
            print("2. Return to Main Menu")
            print("3. Quit")

            option = input("Enter your choice: ")

            if option == "1":
                continue
            elif option == "2":
                return
            elif option == "3":
                exit()
            else:
                print("\nInvalid choice. Please enter a number between 1 and 3.")
