"""
main.py: This module serves as the entry point for the InvestNow application. 
It handles the main operations such as logging in, registering, and quitting the application.

If run directly (and not imported as a module in another script), 
it calls the main() function, which controls the primary application loop.
"""

from login import Login
from register import Register
from session import Session


def print_menu():
    """
    Prints the main menu for the InvestNow application.
    """
    print("\nInvestNow - Main Menu")
    print("1. Login")
    print("2. Register")
    print("3. Quit")


def get_choice():
    """
    Prompts the user for their menu choice and returns it.
    """
    while True:
        choice = input("Enter your choice: ")
        if choice in ["1", "2", "3"]:
            return choice
        else:
            print("\nInvalid choice. Please enter a number between 1 and 3.")


def main():
    """
    The main function of the InvestNow application. 
    It creates instances of the Login and Register classes and provides a loop 
    for the user to choose to login, register, or quit the application.
    """
    session = Session()
    login = Login(session)
    register = Register()

    while True:
        print_menu()

        try:
            choice = get_choice()

            if choice == "1":
                login.prompt_user()
            elif choice == "2":
                register.prompt_user()
            elif choice == "3":
                print("\nClosing InvestNow.")
                break
        except SystemExit:
            print("\nClosing InvestNow.")
            break


if __name__ == "__main__":
    main()
