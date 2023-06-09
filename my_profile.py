import json
from session import Session

class MyProfile:
    """
    The MyProfile class is responsible for handling the profile operations of a user.
    """

    def __init__(self, session: Session):
        """
        Initialize the MyProfile class.
        Load the user data from the users.json file into a dictionary.
        """
        self.session = session
        self.file = 'users.json'
        try:
            with open(self.file, encoding='utf-8') as file:
                self.users = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.users = {}

        # Iterate through all users and add default values for age and risk_tolerance if not present
        for user in self.users:
            if 'age' not in self.users[user]:
                self.users[user]['age'] = 'not set'
            if 'risk_tolerance' not in self.users[user]:
                self.users[user]['risk_tolerance'] = 'not set'

        self.save_users()

    def prompt_continue(self):
        """
        Ask the user whether to continue or quit.
        """
        while True:
            continue_choice = input("\nWould you like to continue? (Y/N): ").lower()
            if continue_choice == 'y':
                break
            elif continue_choice == 'n':
                return False
            else:
                print("\nInvalid choice. Please enter Y or N.")
        return True

    def prompt_email(self):
        """
        Prompt the user for a new email.
        """
        while True:
            email = input("\nEnter your new email: ")
            if email.strip():
                return email
            else:
                print("\nEmail cannot be empty. Please enter a valid email.")

    def prompt_password(self):
        """
        Prompt the user for a new password.
        """
        while True:
            password = input("\nEnter your new password: ")
            if password.strip():
                return password
            else:
                print("\nPassword cannot be empty. Please enter a valid password.")

    def prompt_age(self):
        """
        Prompt the user for their age.
        """
        while True:
            age = input("\nEnter your age: ")
            if age.isdigit() and 0 < int(age) <= 150:
                return age
            else:
                print("\nInvalid age. Please enter a valid age between 1 and 150.")

    def prompt_risk_tolerance(self):
        """
        Prompt the user for their risk tolerance.
        """
        while True:
            risk_tolerance = input("\nEnter your risk tolerance (low, medium, high): ")
            if risk_tolerance.lower() in ['low', 'medium', 'high']:
                return risk_tolerance
            else:
                print("\nInvalid risk tolerance. Please enter 'low', 'medium', or 'high'.")

    def prompt_user(self):
        """
        Prompt the user to display their profile or update profile information.
        If the user chooses to update their profile, the user is prompted for the new information.
        """
        while True:
            print("\nInvestNow - My Profile")

            print("1. View Profile")
            print("2. Update Profile")
            print("3. Return to Menu")

            choice = input("Enter your choice: ")

            if choice == "1":
                self.view_profile()
                if not self.prompt_continue():
                    break
            elif choice == "2":
                self.update_profile()
            elif choice == "3":
                break
            else:
                print("\nInvalid choice. Please enter a number between 1 and 3.")

    def view_profile(self):
        """
        View the user's profile.
        """
        # Get the username of the currently logged-in user
        current_user = self.session.get_current_user()

        print("\nProfile Details")
        print("-------------------------")
        print(f"Username: {current_user}")
        print(f"Email: {self.users[current_user]['email']}")
        print(f"\nAge: {self.users[current_user]['age']}")
        print(f"Risk Tolerance: {self.users[current_user]['risk_tolerance']}")
        print("-------------------------")

    def update_profile(self):
        """
        Update the user's profile.
        """
        # Provide options for the user to update their profile
        while True:
            print("\nUpdate Profile - Options:")
            print("1. Update Email")
            print("2. Update Password")
            print("3. Update Age")
            print("4. Update Risk Tolerance")
            print("5. Return to Menu")

            choice = input("Enter your choice: ")

            current_user = self.session.get_current_user()

            if choice == "1":
                new_email = self.prompt_email()
                self.users[current_user]['email'] = new_email
                print("\nEmail updated successfully.")
            elif choice == "2":
                new_password = self.prompt_password()
                self.users[current_user]['password'] = new_password
                print("\nPassword updated successfully.")
            elif choice == "3":
                new_age = self.prompt_age()
                self.users[current_user]['age'] = new_age
                print("\nAge updated successfully.")
            elif choice == "4":
                new_risk_tolerance = self.prompt_risk_tolerance()
                self.users[current_user]['risk_tolerance'] = new_risk_tolerance
                print("\nRisk tolerance updated successfully.")
            elif choice == "5":
                break
            else:
                print("\nInvalid choice. Please enter a number between 1 and 5.")

            self.save_users()

            # Prompt the user to continue updating their profile or not.
            if not self.prompt_continue():
                break

    def save_users(self):
        """
        Save the updated user data to the JSON file.
        """
        with open(self.file, 'w', encoding='utf-8') as file:
            json.dump(self.users, file)
