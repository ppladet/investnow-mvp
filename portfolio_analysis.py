import json
from prettytable import PrettyTable


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
            print("2. Add Stock Holding")
            print("3. Remove Stock Holding")
            print("4. Return to Main Menu")

            choice = input("Enter your choice: ")

            if choice == "1":
                self.view_stocks()
            elif choice == "2":
                self.add_stock()
            elif choice == "3":
                self.remove_stock()
            elif choice == "4":
                print("\nReturning to main menu.")
                return False
            else:
                print("\nInvalid choice. Please enter a number between 1 and 4.")
            
            if not self.prompt_continue():
                return False

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

        if stocks:
            table = PrettyTable(['Symbol', 'Shares', 'Purchase Price'])
            for stock in stocks:
                table.add_row([stock['symbol'], stock['shares'], stock['purchase_price']])
            print("\n")
            print(table)
        else:
            print("\nYou currently have no stocks in your portfolio.")

    def add_stock(self):
        """
        Function to add a stock to user's portfolio.
        """
        while True:
            symbol = input("\nEnter the stock symbol: ").strip().upper()
            if symbol:
                break
            else:
                print("\nStock symbol cannot be empty. Please enter a valid stock symbol.")

        while True:
            shares = input("Enter the number of shares: ").strip()
            try:
                shares = int(shares)
                if shares > 0:
                    break
                else:
                    print("\nNumber of shares should be a positive non-zero number. Please enter a valid number.")
            except ValueError:
                print("\nInvalid input. Please enter a number for shares.")

        while True:
            purchase_price = input("Enter the purchase price: ").strip()
            try:
                purchase_price = float(purchase_price)
                if purchase_price > 0:
                    break
                else:
                    print("\nPurchase price should be a positive non-zero number. Please enter a valid price.")
            except ValueError:
                print("\nInvalid input. Please enter a number for price.")

        self._add_stock_to_user(symbol, shares, purchase_price)

    def remove_stock(self):
        """
        Function to remove a specific quantity of a stock from user's portfolio.
        """
        while True:
            symbol = input("\nEnter the stock symbol: ").strip().upper()
            if symbol:
                break
            else:
                print("\nStock symbol cannot be empty. Please enter a valid stock symbol.")

        while True:
            shares_to_remove = input("Enter the number of shares to remove: ").strip()
            try:
                shares_to_remove = int(shares_to_remove)
                if shares_to_remove > 0:
                    break
                else:
                    print("\nNumber of shares should be a positive non-zero number. Please enter a valid number.")
            except ValueError:
                print("\nInvalid input. Please enter a number for shares.")

        users = self.load_users()
        username = self.session.get_current_user()

        for stock in users[username]["stocks"]:
            if stock["symbol"].lower() == symbol.lower():
                if shares_to_remove > stock["shares"]:
                    print(f"\nYou do not own enough shares of {symbol}. You currently own {stock['shares']} shares.")
                elif shares_to_remove == stock["shares"]:
                    users[username]["stocks"].remove(stock)
                    print(f"\nAll shares of {symbol} have been removed from your portfolio.")
                else:
                    stock["shares"] -= shares_to_remove
                    print(f"\n{shares_to_remove} shares of {symbol} have been removed from your portfolio. You now own {stock['shares']} shares.")

                self.save_users(users)
                return

        print(f"\nStock {symbol} does not exist in your portfolio.")

    def _add_stock_to_user(self, symbol, shares, purchase_price):
        """
        Internal method to add a stock to a user's portfolio.
        """
        users = self.load_users()
        username = self.session.get_current_user()

        for stock in users[username]["stocks"]:
            if stock["symbol"].lower() == symbol.lower():
                total_shares = stock["shares"] + shares
                weighted_price = (stock["shares"] * stock["purchase_price"] + shares * purchase_price) / total_shares
                weighted_price = round(weighted_price, 2)  # Rounded to 2 decimal places
                stock["shares"] = total_shares
                stock["purchase_price"] = weighted_price
                print(f"\nAdded {shares} shares of {symbol} to your portfolio. You now own {total_shares} shares with a weighted purchase price of {weighted_price}.")
                self.save_users(users)
                return

        new_stock = {
            "symbol": symbol,
            "shares": shares,
            "purchase_price": round(purchase_price, 2)  # Rounded to 2 decimal places
        }

        users[username]["stocks"].append(new_stock)
        self.save_users(users)
        print(f"\nAdded {shares} shares of {symbol} to your portfolio at a purchase price of {purchase_price}.")

    def save_users(self, users):
        """
        Save the user data to a json file.
        """
        with open(self.user_file, 'w', encoding='utf-8') as file:
            json.dump(users, file)

    def load_users(self):
        """
        Load the user data from a json file.
        """
        try:
            with open(self.user_file, encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def prompt_continue(self):
        """
        Ask the user whether to continue or quit.
        """
        while True:
            continue_choice = input("\nWould you like to continue? (Y/N): ").lower()
            if continue_choice == 'y':
                return True
            elif continue_choice == 'n':
                return False
            else:
                print("\nInvalid choice. Please enter Y or N.")
