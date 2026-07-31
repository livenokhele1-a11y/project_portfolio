import random
import csv
import hashlib
from datetime import datetime


class Account:
    """This section will handle single account registration and login"""

    @staticmethod
    def generate_account_number():
        """Generates a unique 8-digit account number"""
        while True:
            acc_num = str(random.randint(10000000, 99999999))

            if not Account.account_exists(acc_num):
                return acc_num

    @staticmethod
    def account_exists(acc_num):
        """Checks if an account number already exists"""
        try:
            with open("account_balances.txt", "r") as file:
                reader = csv.reader(file)
                for row in reader:
                    if acc_num == row[0]:  # Checks the account number column
                        return True

        except FileNotFoundError:
            return False

        return False

    @staticmethod
    def hash_pin(pin):
        """Hash the PIN using SHA-256"""
        """SHA-256 is widely trusted and secure for password hashing,
        making it a good choice for protecting PINs."""
        return hashlib.sha256(pin.encode()).hexdigest()

    @staticmethod
    def register():
        """Registers a new account"""
        phone = input("Enter your phone number (10 digits):")

        if len(phone) != 10 or not phone.isdigit():
            # Checks length of phone number and ensures it only contains digits
            print("Invalid phone number.")
            return

        if Account.phone_exists(phone):
            # Prevents duplicate accounts created with the same phone number
            print("Phone number is already registered.")
            return

        pin = input("Enter PIN (4-5 digits): ")
        confirm_pin = input("Confirm PIN: ")

        if pin != confirm_pin:
            print("PINs do not match")
            return

        if len(pin) not in [4, 5] or not pin.isdigit():
            print("Invalid PIN format.")
            return

        account_number = Account.generate_account_number()
        # Creates unique 8-digit account
        hashed_pin = Account.hash_pin(pin)

        # Save to file
        with open("account_balances.txt", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([account_number, phone, hashed_pin, 0])

        print(f"Registration successful!")
        print(f"Your account number is: {account_number}")

        Account.log_event(phone, "REGISTERED")
        # Logs the registration event

    @staticmethod
    def phone_exists(phone):
        """Checks if a phone number is already registered"""
        try:
            with open("account_balances.txt", "r") as file:
                reader = csv.reader(file)
                for row in reader:
                    if phone == row[1]:  # Check the phone number column
                        return True
        except FileNotFoundError:
            return False

        return False

    @staticmethod
    def login():
        """Login user with 3 attempts"""
        attempts = 0

        while attempts < 3:
            phone = input("Phone number: ")
            pin = input("PIN: ")

            hashed_pin = Account.hash_pin(pin)

            try:
                with open("account_balances.txt", "r") as file:
                    reader = csv.reader(file)

                    for row in reader:
                        acc_num, stored_phone, stored_pin, balance = row

                        if phone == stored_phone and hashed_pin == stored_pin:
                            print("Login successful!")
                            Account.log_event(phone, "LOGIN_SUCCESS")
                            return acc_num, phone

            except FileNotFoundError:
                print("No accounts found.")
                return

            print("Login failed.")
            Account.log_event(phone, "LOGIN_FAILED")
            attempts += 1

        print("Too many failed attempts.")

    @staticmethod
    def log_event(phone, event):
        """Log each event with a timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open("log.txt", "a") as file:
            file.write(f"{timestamp}, {phone}, {event}\n")
