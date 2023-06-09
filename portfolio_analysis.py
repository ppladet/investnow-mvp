import json

class PortfolioAnalysis:
    """
    Class to handle portfolio analysis operations for a user.
    """

    def __init__(self, session):
        """
        Initialize the PortfolioAnalysis object and load users.

        Parameters
        ----------
        session : Session
            The user's session.
        """
        self.session = session
        self.user_file = 'users.json'

    def portfolio_menu(self):
        """
        Display the portfolio menu and handle the user's choice.
        """
        while True:
            print("\nInvestNow - Portfolio Analysis")
            print("1. View Stocks")
            print("2. Add Stock")
            print("3. Return to Main Menu")

            choice = input("Enter your choice: ")

            if choice == "1":
                self.view_stocks()
            elif choice == "2":
                self.add_stock()
            elif choice == "3":
                print("\nReturning to main menu.")
                break
            else:
                print("\nInvalid choice. Please enter a number between 1 and 3.")

    def prompt_user(self):
        """Provide user with portfolio analysis options."""
        self.portfolio_menu()

    def view_stocks(self):
        """
        Function to view user's stocks.
        """
        users = self.load_users()
        username = self.session.get_current_user()
        stocks = users[username]["stocks"]

        for stock in stocks:
            print(f"Symbol: {stock['symbol']}, Shares: {stock['shares']}, Purchase price: {stock['purchase_price']}")

    def add_stock(self):
        """
        Function to add a stock to user's portfolio.
        """
        symbol = input("Enter the stock symbol: ")
        shares = input("Enter the number of shares: ")
        purchase_price = input("Enter the purchase price: ")

        new_stock = {
            "symbol": symbol,
            "shares": shares,
            "purchase_price": purchase_price
        }

        users = self.load_users()
        username = self.session.get_current_user()
        users[username]["stocks"].append(new_stock)
        self.save_users(users)

    def save_users(self, users):
        """
        Save the user data to a json file.
        """
        with open(self.user_file, 'w', encoding='utf-8') as file:
            json.dump(users, file)

    def load_users(self):
        """
        Load the user data from a json file. If a user does not have a "stocks" key,
        it is added with an empty list as its value.
        """
        try:
            with open(self.user_file, encoding='utf-8') as file:
                users = json.load(file)
                
                # Add "stocks" key for current user if it doesn't exist
                username = self.session.get_current_user()
                if "stocks" not in users[username]:
                    users[username]["stocks"] = []
                    self.save_users(users)
                
                return users
        except FileNotFoundError:
            return {}
