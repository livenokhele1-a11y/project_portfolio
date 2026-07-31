import csv
from datetime import datetime


class Transaction:
    """Handles all the banking transactions"""

    @staticmethod
    def deposit(account_number, phone):
        """Deposit money into the account"""

        amount = float(input("Enter amount to deposit: "))

        records = []

        with open("account_balances.txt", "r") as file:
            reader = csv.reader(file)
            for row in reader:
                acc_num, phone_num, pin, balance = row

                if acc_num == account_number:
                    balance = float(balance) + amount
                    # Updates the balance
                    print(f"Deposit successful. New balance is: R{balance}")

                    Transaction.log_transaction
                    (phone, "DEPOSIT", amount, balance)

                    records.append([acc_num, phone_num, pin, balance])
                else:
                    records.append(row)

        with open("account_balances.txt", "w", newline="") as file:
            # Rewrites the file with the updated balance
            writer = csv.writer(file)
            writer.writerows(records)

    @staticmethod
    def log_transaction(phone, transaction_type, amount, balance):
        """Log the transaction details in a file"""
        timestamp = datetime.now().strftime("%Y=%m-%d %H:%M:%S")

        with open("transations.txt", "a") as file:
            file.write(
                f"{timestamp}, {phone}, {transaction_type}, {amount}, {balance}\n"
                )

    @staticmethod
    def withdraw(account_number, phone):
        """Withdraw money from the account"""
        amount = float(input("Enter amount to withdraw: "))

        records = []
        found = False

        with open("account_balances.txt", "r") as file:
            reader = csv.reader(file)
            for row in reader:
                acc_num, phone_num, pin, balance = row
                balance = float(balance)

                if acc_num == account_number:
                    found = True
                    if amount > balance:
                        # Prevents overdrawing the account
                        print("Insufficient funds.")
                        return

                    new_balance = balance - amount
                    print(f"Withdraw successful. New balance is: R{new_balance}")

                    Transaction.log_transaction
                    (phone, "WITHDRAW", amount, new_balance)

                    records.append([acc_num, phone_num, pin, new_balance])
                else:
                    records.append(row)

        if not found:
            print("Account not found.")
            return

        with open("account_balances.txt", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(records)

    @staticmethod
    def transfer(sender_acc, sender_phone):
        """Transfer money to another account (EFT)"""

        recipient_acc = input("Enter reciepient account number (8 digits): ")

        # Check the length of the recipent's account number
        if len(recipient_acc) != 8 or not recipient_acc.isdigit():
            print("Error: Account number must be exactly 8 digits.")
            return

        # Prevent user from transferring to their own account
        if recipient_acc == sender_acc:
            print("Error: You cannot transfer to your own account.")
            return

        amount = float(input("Enter amount to transfer: "))

        records = []
        sender_found = False
        recipient_found = False

        sender_balance = 0

        # Read the file
        with open("account_balances.txt", "r") as file:
            reader = csv.reader(file)
            for row in reader:
                acc_num, phone_num, pin, balance = row
                balance = float(balance)

                # Find the sender's account and check for succient funds
                if acc_num == sender_acc:
                    sender_found = True

                    if amount > balance:
                        print("Insufficient funds.")
                        return

                    sender_balance = balance - amount
                    records.append([acc_num, phone_num, pin, sender_balance])

                # Find the recipient's account and update the balance
                elif acc_num == recipient_acc:
                    recipient_found = True
                    new_balance = balance + amount
                    records.append([acc_num, phone_num, pin, new_balance])

                else:
                    records.append(row)

        # If the recipient account is not found, show an error message
        if not recipient_found:
            print("Error: Account not found.")
            return

        # Write the updated balances back to the file
        with open("account_balances.txt", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(records)

        print(f"Transfer successful! R{amount} sent to {recipient_acc}")
        print(f"Your new balance is: R{sender_balance}")

        # Log the transaction for the sender
        Transaction.log_transaction(
            sender_phone, "EFT_OUT", amount, sender_balance
            )

    @staticmethod
    def view_statement(phone):
        """Display the user's transaction history"""

        print("\n--- Statement ---")

        try:
            with open("transactions.txt", "r") as file:
                found = False

                for line in file:
                    parts = (x.strip() for x in line.strip().split(","))

                    if len(parts) != 5:
                        continue

                    timestamp, phone_num, transaction_type, amount, balance = parts

                    if phone_num == phone:
                        # Only shows transactions related to logged in user
                        found = True

                        # Format the output for better readability
                        if transaction_type == "DEPOSIT":
                            sign = "+"
                        elif transaction_type == "WITHDRAW" or transaction_type == "EFT_OUT":
                            sign = "-"
                        else:
                            sign = ""

                        print(
                            f"{timestamp} | {transaction_type} | "
                            f"{sign}R{amount} | Balance: R{balance}"
                            )

                if not found:
                    print("No transactions found.")

        except FileNotFoundError:
            print("No transactions yet")
