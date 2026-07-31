from account import Account
from transaction import Transaction


def main():
    while True:
        print("\n=== Welcome to PyBank ATM ===")
        print("1. Register")
        print("2. Login")
        print("3. Exit")

        choice = input("Select an option: ")

        if choice == "1":
            Account.register()
        elif choice == "2":
            result = Account.login()

            if result:
                acc_num, phone = result
                while True:
                    print("\n--- Main Menu ---")
                    print("1. Deposit")
                    print("2. Withdraw")
                    print("3. Transfer")
                    print("4. View Statement")
                    print("5. Logout")

                    option = input("Choose an option: ")

                    if option == "1":
                        Transaction.deposit(acc_num, phone)

                    elif option == "2":
                        Transaction.withdraw(acc_num, phone)

                    elif option == "3":
                        Transaction.transfer(acc_num, phone)

                    elif option == "4":
                        Transaction.view_statement(phone)

                    elif option == "5":
                        print("Logged out.")
                        break
                    else:
                        print("Invalid option.")
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
