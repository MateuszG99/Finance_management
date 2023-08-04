import matplotlib.pyplot as plt
import pandas as pd
import csv
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

class BudgetManager:
    def __init__(self):
        self.budgets = {}
        self.current_budget = None

    '''Creating budget'''
    def create_budget(self, name, amount):
        if not name:
            print("Budget name cannot be empty.")
            return

        if name in self.budgets:
            print("Budget with this name already exists!")
            return

        try:
            amount = float(amount)
        except ValueError:
            print("Invalid initial amount. Please enter a valid number.")
            return

        if amount <= 0:
            print("Initial amount must be greater than zero.")
            return

        self.budgets[name] = {
            'amount': amount,
            'transactions': []
        }
        print(f"Budget '{name}' created with initial amount: ${amount}")
        self.current_budget = name


    '''Choosing a budget'''
    def select_budget(self, name):
        if name in self.budgets:
            self.current_budget = name
            print(f"Selected budget: '{name}'")
        else:
            print("Budget not found!")

    '''Editing budget'''
    def edit_budget(self, name) :
        if name in self.budgets :
            print(f"Editing '{name}' budget:")
            new_name = input("Enter the new name (leave empty to keep the current name): ")
            new_amount = input("Enter the new initial amount (leave empty to keep the current amount): ")

            # Validation of new budget name
            if new_name and new_name != name :
                if new_name in self.budgets :
                    print("Budget with this name already exists. Please choose a different name.")
                    return
                else :
                    self.budgets[new_name] = self.budgets.pop(name)
                    name = new_name
                    print(f"Budget name updated to '{name}'.")

            # Validation of the new starting amount
            if new_amount :
                try :
                    new_amount = float(new_amount)
                    self.budgets[name]['amount'] = new_amount
                    print(f"Initial amount of '{name}' budget updated to ${new_amount}.")
                except ValueError :
                    print("Invalid amount. The budget amount will not be changed.")

            print(f"Budget '{name}' has been updated.")
        else :
            print("Budget not found!")

    '''Showing transactions'''
    def show_transactions(self):
        if self.current_budget:
            transactions = self.budgets[self.current_budget]['transactions']
            print(f"Transaction history for '{self.current_budget}' budget:")
            for idx, (amount, description) in enumerate(transactions, 1):
                print(f"{idx}. Amount: ${amount}, Description: '{description}'")
        else:
            print("Please select a budget first!")
    '''Showing budgets'''
    def show_budgets(self):
        print("Available budgets:")
        for budget, amount in self.budgets.items():
            print(f"'{budget}' - ${amount}")

    def get_budget_balance(self, name) :
        budget_info = self.budgets.get(name)
        if budget_info :
            return budget_info['amount']
        else :
            print("Budget not found.")
            return None

    '''Creating a chart'''
    def generate_balance_chart(self, filename=None) :
        if not self.budgets :
            print("No budgets found. Please create a budget first.")
            return

        data = {'Budget' : [], 'Balance' : []}
        for budget, info in self.budgets.items() :
            data['Budget'].append(budget)
            data['Balance'].append(info['amount'])

        df = pd.DataFrame(data)
        ax = df.plot(kind='bar', x='Budget', y='Balance', legend=False)
        plt.title('Budget Balances')
        plt.xlabel('Budget')
        plt.ylabel('Balance')
        ax.grid(axis='y')

        if filename :
            plt.savefig(filename)
            print(f"Chart saved as '{filename}'")
        else :
            plt.show()

    '''Exporting to csv file'''
    def export_to_csv(self, filename) :
        if not self.budgets :
            print("No budgets found. Please create a budget first.")
            return

        with open(filename, mode='w', newline='') as file :
            writer = csv.writer(file)
            writer.writerow(['Budget', 'Balance'])
            for budget, info in self.budgets.items() :
                writer.writerow([budget, info['amount']])

        print(f"Data exported to '{filename}' in CSV format.")

    '''Exporting to pdf file'''
    def export_to_pdf(self, filename) :
        if not self.budgets :
            print("No budgets found. Please create a budget first.")
            return

        c = canvas.Canvas(filename, pagesize=letter)
        c.setFont("Helvetica", 12)

        c.drawString(100, 750, "Budget Balances:")
        c.drawString(100, 730, "----------------")

        y = 700
        for budget, amount in self.budgets.items() :
            c.drawString(100, y, f"{budget}: ${amount}")
            y -= 20

        c.save()

        print(f"Data exported to '{filename}' in PDF format.")

    '''Deleting budget'''
    def delete_budget(self, name):
        if name in self.budgets:
            choice = input(f"Are you sure you want to delete '{name}' budget? (yes/no): ").lower()

            while choice not in ['yes', 'no']:
                print("Invalid choice. Please enter 'yes' or 'no'.")
                choice = input(f"Are you sure you want to delete '{name}' budget? (yes/no): ").lower()

            if choice == "yes":
                del self.budgets[name]
                print(f"Budget '{name}' has been deleted.")
                self.current_budget = None
            else:
                print("Budget deletion canceled.")
        else:
            print("Budget not found!")

if __name__ == "__main__":
    budget_manager = BudgetManager()

    while True:
        print("\n1. Create Budget")
        print("2. Delete Budget")
        print("3. Select Budget")
        print("4. Edit Budget")
        print("5. Show Budgets")
        print("6. Get Budget Balance")
        print("7. Generate Balance Chart")
        print("8. Export file to csv")
        print("9. Export file to pdf")
        print("10. Show transactions ")
        print("11. Exit")

        choice = input("Enter your choice: ")
        '''Choices of individual options'''
        if choice == "1":
            name = input("Enter the name of the budget: ")
            amount = float(input("Enter the initial amount: "))
            budget_manager.create_budget(name, amount)

        elif choice == "2" :
            name = input("Enter the name of the budget to delete: ")
            budget_manager.delete_budget(name)

        elif choice == "3":
            name = input("Enter the name of the budget to select: ")
            budget_manager.select_budget(name)

        elif choice == "4":
            name = input("Enter the name of the budget to edit: ")
            budget_manager.edit_budget(name)

        elif choice == "5":
            budget_manager.show_budgets()

        elif choice == "6":
            name = input("Enter the name of the budget to get balance: ")
            balance = budget_manager.get_budget_balance(name)
            print(f"Balance of '{name}' budget: ${balance}")

        elif choice == "7":
            budget_manager.generate_balance_chart()

        elif choice == "8" :
            filename = input("Enter the filename to export (without extension): ")
            budget_manager.export_to_csv(f"{filename}.csv")

        elif choice == "9" :
            filename = input("Enter the filename to export (without extension): ")
            budget_manager.export_to_pdf(f"{filename}.pdf")

        elif choice == "10":
            budget_manager.show_transactions()

        elif choice == "11":
            print("Exiting the Budget Manager.")
            break


        else:
            print("Invalid choice. Please try again.")
