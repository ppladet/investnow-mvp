import yfinance as yf
import pandas as pd
import numpy as np
import json
import re
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from scipy.optimize import minimize
from session import Session

class TradingAlgorithm:
    def __init__(self, session: Session):
        self.session = session
        self.start_date = '2015-01-01'
        self.end_date = datetime.today().strftime('%Y-%m-%d')

    def prompt_user(self):
        """Provide user with trading algorithm options."""
        self.prompt_menu()

    def prompt_menu(self):
        """Display the trading algorithm menu and handle the user's choice."""
        while True:
            print("\nInvestNow - Trading Algorithm")
            print("1. View MVP")
            print("2. View Correlation Matrix")
            print("3. Automated Optimization")
            print("4. Time Horizon")
            print("5. Return to Main Menu")

            choice = input("Enter your choice: ")

            if choice == "1":
                self.view_mvp()
            elif choice == "2":
                self.view_correlation_matrix()
            elif choice == "3":
                self.automated_optimization()
            elif choice == "4":
                self.handle_time_horizon()
            elif choice == "5":
                print("\nReturning to main menu.")
                return
            else:
                print("\nInvalid choice. Please enter a number between 1 and 5.")

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

    def handle_time_horizon(self):
        while True:
            print("\nTime Horizon")
            print("1. View Time Horizon")
            print("2. Change Time Horizon")
            print("3. Return to Trading Algorithm Menu")
            
            choice = input("Enter your choice: ")
            
            if choice == "1":
                print(f"\nCurrent Time Horizon: {self.start_date} to {self.end_date}")
                if not self.prompt_continue():
                    return
            elif choice == "2":
                while True:
                    new_start_date = input("\nEnter the new start date (YYYY-MM-DD): ")
                    new_end_date = input("Enter the new end date (YYYY-MM-DD): ")

                    # Validate the date format
                    if not re.match(r'\d{4}-\d{2}-\d{2}', new_start_date) or not re.match(r'\d{4}-\d{2}-\d{2}', new_end_date):
                        print("Invalid date format. Please use YYYY-MM-DD.")
                        continue
                    
                    # Convert to datetime objects
                    try:
                        new_start_date = datetime.strptime(new_start_date, '%Y-%m-%d')
                        new_end_date = datetime.strptime(new_end_date, '%Y-%m-%d')
                    except ValueError:
                        print("Invalid date. Please enter a valid date in the format YYYY-MM-DD.")
                        continue
                    
                    # Check if end_date is after start_date
                    if new_end_date < new_start_date:
                        print("End date must be after start date.")
                        continue
                    
                    # Update class attributes
                    self.start_date = new_start_date.strftime('%Y-%m-%d')
                    self.end_date = new_end_date.strftime('%Y-%m-%d')

                    break  # break out of the inner while loop once the dates are updated

                # Ask user if they want to continue adjusting the time horizon
                if not self.prompt_continue():
                    return
            elif choice == "3":
                return
            else:
                print("\nInvalid choice. Please enter a number between 1 and 3.")

    def get_user_stocks(self, username):
        with open('users.json', 'r') as f:
            users = json.load(f)
        
        user = users.get(username)
        if not user:
            print(f"User {username} not found.")
            return None
        
        stocks = user['stocks']
        total_portfolio_value = 0
        for stock in stocks:
            symbol = stock['symbol']
            data = yf.download(symbol, start=self.start_date, end=self.end_date)
            stock['current_price'] = data['Adj Close'][-1]
            stock['value'] = stock['shares'] * stock['current_price']
            total_portfolio_value += stock['value']

        for stock in stocks:
            stock['weight'] = stock['value'] / total_portfolio_value

        return stocks

    def get_stock_data(self, symbols):
        data = yf.download(symbols, start=self.start_date, end=self.end_date)
        return data['Adj Close']

    def calculate_returns(self, data):
        return data.pct_change()

    def calculate_portfolio_return(self, weights, returns):
        return np.sum(returns.mean() * weights) * 252

    def calculate_portfolio_risk(self, weights, returns):
        return np.sqrt(np.dot(weights.T, np.dot(returns.cov() * 252, weights)))

    def calculate_sharpe_ratio(self, weights, returns):
        portfolio_return = self.calculate_portfolio_return(weights, returns)
        portfolio_risk = self.calculate_portfolio_risk(weights, returns)
        sharpe_ratio = portfolio_return / portfolio_risk
        return -sharpe_ratio

    def minimum_variance_portfolio(self, returns):
        num_assets = len(returns.columns)
        args = (returns,)
        constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
        bound = (0.0,1.0)
        bounds = tuple(bound for asset in range(num_assets))
        result = minimize(self.calculate_portfolio_risk, num_assets*[1./num_assets,], args=args,
                          method='SLSQP', bounds=bounds, constraints=constraints)
        return result

    def maximum_sharpe_ratio_portfolio(self, returns):
        num_assets = len(returns.columns)
        args = (returns,)
        constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
        bound = (0.0,1.0)
        bounds = tuple(bound for asset in range(num_assets))
        result = minimize(self.calculate_sharpe_ratio, num_assets*[1./num_assets,], args=args,
                          method='SLSQP', bounds=bounds, constraints=constraints)
        return result

    def view_mvp(self):
        username = self.session.get_current_user()
        user_stocks = self.get_user_stocks(username)
        symbols = [stock['symbol'] for stock in user_stocks]
        weights = [stock['weight'] for stock in user_stocks]

        data = self.get_stock_data(symbols)
        returns = self.calculate_returns(data)

        # Print current portfolio weights
        print("\nCurrent Portfolio Weights:")
        for symbol, weight in zip(symbols, weights):
            print(f"{symbol}: {weight:.4f}")

        # Find and print minimum variance portfolio
        mvp_result = self.minimum_variance_portfolio(returns)
        print("\nMinimum Variance Portfolio Weights:")
        for symbol, weight in zip(symbols, mvp_result.x):
            print(f"{symbol}: {weight:.4f}")

        # Find and print maximum Sharpe ratio portfolio
        msr_result = self.maximum_sharpe_ratio_portfolio(returns)
        print("\nMaximum Sharpe Ratio Portfolio Weights:")
        for symbol, weight in zip(symbols, msr_result.x):
            print(f"{symbol}: {weight:.4f}")

        # Set a seed for the random number generator
        np.random.seed(42)

        # Generate random portfolios
        num_portfolios = 50000
        num_assets = len(symbols)
        results = np.zeros((3, num_portfolios))
        for i in range(num_portfolios):
            weights = np.random.random(num_assets)
            weights /= np.sum(weights)
            portfolio_return = self.calculate_portfolio_return(weights, returns)
            portfolio_risk = self.calculate_portfolio_risk(weights, returns)
            sharpe_ratio = portfolio_return / portfolio_risk
            results[0, i] = portfolio_risk
            results[1, i] = portfolio_return
            results[2, i] = sharpe_ratio

        # Convert results array to Pandas DataFrame
        results_frame = pd.DataFrame(results.T, columns=['Risk', 'Return', 'Sharpe Ratio'])

        # Plot efficient frontier with color map according to Sharpe Ratio
        plt.scatter(results_frame.Risk, results_frame.Return, c=results_frame['Sharpe Ratio'], cmap='YlGnBu', marker='o', s=10, alpha=0.3)
        plt.colorbar(label='Sharpe Ratio')
        plt.scatter(self.calculate_portfolio_risk(weights, returns), self.calculate_portfolio_return(weights, returns), marker='s', color='g', s=200, label='User Portfolio')
        plt.scatter(self.calculate_portfolio_risk(mvp_result.x, returns), self.calculate_portfolio_return(mvp_result.x, returns), marker='s', color='r', s=200, label='Minimum Variance Portfolio')
        plt.scatter(self.calculate_portfolio_risk(msr_result.x, returns), self.calculate_portfolio_return(msr_result.x, returns), marker='*', color='b', s=200, label='Maximum Sharpe Ratio Portfolio')
        plt.title('Efficient Frontier with User Portfolio')
        plt.xlabel('Risk')
        plt.ylabel('Return')
        plt.legend(labelspacing=0.8)
        plt.show()

    def view_correlation_matrix(self):
        username = self.session.get_current_user()
        user_stocks = self.get_user_stocks(username)
        symbols = [stock['symbol'] for stock in user_stocks]

        data = self.get_stock_data(symbols)
        returns = self.calculate_returns(data)

        # Calculate correlation matrix
        corr_matrix = returns.corr()

        # Create a custom diverging palette
        cmap = sns.diverging_palette(130, 10, s=80, l=55, n=100, as_cmap=True)
        
        # Plot correlation matrix
        plt.figure(figsize=(10, 10))
        sns.heatmap(corr_matrix, annot=True, cmap=cmap, vmin=0, vmax=1, center=0.5, fmt=".2f", linewidths=0.5)
        plt.title('Correlation Matrix')
        plt.show()

    def automated_optimization(self):
        """Provide user with actions needed to adjust portfolio to minimum variance or maximum Sharpe ratio portfolio."""
        while True:
            print("\nAutomated Optimization - Adjust Portfolio")
            print("1. Minimum Variance Portfolio (MVP)")
            print("2. Maximum Sharpe Ratio Portfolio (MSR)")
            print("3. Return to Trading Algorithm Menu")

            choice = input("Enter your choice: ")

            if choice == "1":
                target = 'MVP'
            elif choice == "2":
                target = 'MSR'
            elif choice == "3":
                print("\nReturning to Trading Algorithm menu.")
                return
            else:
                print("\nInvalid choice. Please enter a number between 1 and 3.")
                return

            username = self.session.get_current_user()
            user_stocks = self.get_user_stocks(username)
            symbols = [stock['symbol'] for stock in user_stocks]
            weights = [stock['weight'] for stock in user_stocks]

            data = self.get_stock_data(symbols)
            returns = self.calculate_returns(data)

            if target == 'MVP':
                result = self.minimum_variance_portfolio(returns)
            else:  # target == 'MSR'
                result = self.maximum_sharpe_ratio_portfolio(returns)

            target_weights = result.x

            print(f"\nTo adjust your portfolio to the {target}, perform the following actions:")

            for symbol, current_weight, target_weight, stock in zip(symbols, weights, target_weights, user_stocks):
                current_value = stock['value']
                target_value = target_weight * sum([stock['value'] for stock in user_stocks])
                diff_value = target_value - current_value

                if diff_value > 0:
                    action = 'Buy'
                else:
                    action = 'Sell'

                num_shares = abs(diff_value) / stock['current_price']
                print(f"{action} approximately {num_shares:.2f} shares of {symbol}.")

            if not self.prompt_continue():
                print("\nReturning to Trading Algorithm menu.")
                return
