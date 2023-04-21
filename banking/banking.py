import random

class BankDataBase:
    stored_credentials = {}

    def __init__(self):
        pass

    def credential_exists(self, card_number):
        if card_number in self.stored_credentials:
            return True
        else:
            return False

    def add_account(self, card_number, pin):
        self.stored_credentials[card_number] = pin

    def check_credentials(self, card_number, pin):
        if card_number in self.stored_credentials and self.stored_credentials[card_number] == pin:
            return True
        else:
            return False


class AccountGenerator:

    def __init__(self, database):
        self.database = database
        self.card_number = AccountGenerator.generate_card_number()
        if self.database.credential_exists(self.card_number):
            self.card_number = AccountGenerator.generate_card_number()
        self.pin = AccountGenerator.generate_pin()

    @staticmethod
    def generate_card_number() -> str:
        card_number = "400000"
        check_digit = random.randint(0, 9)
        for i in range(9):
            card_number += str(random.randint(0, 9))
        card_number += str(check_digit)
        return card_number

    @staticmethod
    def generate_pin() -> str:
        pin = ""
        for i in range(4):
            pin += str(random.randint(0, 9))
        return pin


class Account:
    def __init__(self, card_number, pin):
        self.card_number = card_number
        self.pin = pin
        self.balance = 0

    def add_income(self, income):
        self.balance += income

    def close_account(self):
        pass


def main_interface():
    print("1. Create an account")
    print("2. Log into account")
    print("0. Exit")


def logged_in_interface():
    print("1. Balance")
    print("2. Log out")
    print("0. Exit")


def main():
    database = BankDataBase()

    while True:
        main_interface()
        user_input = input()
        if user_input == "1":
            account_generation = AccountGenerator(database)
            account = Account(account_generation.card_number, account_generation.pin)
            database.add_account(account.card_number, account.pin)
            print("Your card has been created")
            print("Your card number:")
            print(account.card_number)
            print("Your card PIN:")
            print(account.pin)
        elif user_input == "2":
            print("Enter your card number:")
            card_number = input()
            print("Enter your PIN:")
            pin = input()
            if database.check_credentials(card_number, pin):
                print("You have successfully logged in!")
                while True:
                    logged_in_interface()
                    user_input = input()
                    if user_input == "1":
                        print("Balance: " + str(account.balance))
                    elif user_input == "2":
                        print("You have successfully logged out!")
                        break
                    elif user_input == "0":
                        print("Bye!")
                        exit()
                    print()
            else:
                print("Wrong card number or PIN!")
        elif user_input == "0":
            print("Bye!")
            exit()
        print()

main()