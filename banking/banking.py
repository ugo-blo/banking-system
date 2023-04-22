import random
import sqlite3


class BankDataBase:

    def __init__(self):
        self.conn = sqlite3.connect('card.s3db')
        self.cur = self.conn.cursor()
        self.cur.execute('create table if not exists card (id integer primary key autoincrement, number text, pin text, balance integer default 0)')
        self.conn.commit()

    def credential_exists(self, card_number) -> bool:
        self.cur.execute(f'select number from card where number = {card_number}')
        return self.cur.fetchone() is not None

    def add_account(self, card_number, pin):
        self.cur.execute(f'insert into card (number, pin) values ({card_number}, {pin})')
        self.conn.commit()

    def check_credentials(self, card_number, pin) -> bool:
        self.cur.execute(f'select number, pin from card where number = {card_number} and pin = {pin}')
        return self.cur.fetchone() is not None

    def get_balance(self, card_number):
        self.cur.execute(f'select balance from card where number = {card_number}')
        return self.cur.fetchone()[0]

    def update_income(self, card_number, income):
        self.cur.execute(f'update card set balance = balance + {income} where number = {card_number}')
        self.conn.commit()

    def close_account(self, card_number):
        self.cur.execute(f'delete from card where number = {card_number}')
        self.conn.commit()


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
        for i in range(9):
            card_number += str(random.randint(0, 9))
        check_sum = AccountGenerator.luhn_algorithm(card_number)
        card_number = card_number + check_sum
        return card_number

    @staticmethod
    def generate_pin() -> str:
        pin = ""
        for i in range(4):
            pin += str(random.randint(0, 9))
        return pin

    @staticmethod
    def luhn_algorithm(card_number: str):
        card_number = list(card_number)
        for i in range(0, len(card_number), 2):
            card_number[i] = str(int(card_number[i]) * 2)
        for i in range(len(card_number)):
            if int(card_number[i]) > 9:
                card_number[i] = str(int(card_number[i]) - 9)
        card_number = [int(i) for i in card_number]
        sum_of_digits = sum(card_number)
        if sum_of_digits % 10 == 0:
            return "0"
        else:
            return str(10 - (sum_of_digits % 10))

    @staticmethod
    def check_for_luhn(card_number):
        digits = [int(i) for i in str(card_number)][::-1]
        doubled_digits = []
        for i in range(len(digits)):
            if i % 2 == 1:
                doubled_digits.append(digits[i] * 2)
            else:
                doubled_digits.append(digits[i])
        subtracted_digits = [x - 9 if x > 9 else x for x in doubled_digits]
        sum_of_digits = sum(subtracted_digits)
        if sum_of_digits % 10 == 0:
            return True
        else:
            return False


class Account:

    def __init__(self, card_number, pin, database: BankDataBase):
        self.database = database
        self.card_number = card_number
        self.pin = pin
        self.balance = 0

    def get_balance(self):
        return self.database.get_balance(self.card_number)

    def add_income(self, income: int):
        if income < 0:
            return
        self.database.update_income(self.card_number, income)
        print("Income was added!")

    def pull_income(self, income: int):
        if income > 0:
            return
        self.database.update_income(self.card_number, income)

    def push_income(self, income: int, card_number_transaction):
        if income < 0:
            return
        self.database.update_income(card_number_transaction, income)

    def make_transaction(self, card_number_transaction):
        if card_number_transaction == self.card_number:
            print("You can't transfer money to the same account!")
        elif not AccountGenerator.check_for_luhn(card_number_transaction):
            print("Probably you made a mistake in the card number. Please try again!")
        elif not self.database.credential_exists(card_number_transaction):
            print("Such a card does not exist.")
        else:
            print("Enter how much money you want to transfer")
            transfer_amount = int(input())
            if transfer_amount > self.get_balance():
                print("Not enough money!")
            else:
                self.pull_income(-transfer_amount)
                self.push_income(transfer_amount, card_number_transaction)
                print("Success!")

    def close_account(self):
        self.database.close_account(self.card_number)
        print("The account has been closed!")


def main_interface():
    print("1. Create an account")
    print("2. Log into account")
    print("0. Exit")


def logged_in_interface():
    print("1. Balance")
    print("2. Add income")
    print("3. Do transfer")
    print("4. Close account")
    print("5. Log out")
    print("0. Exit")


def main():
    database = BankDataBase()
    while True:
        main_interface()
        user_input = input()
        if user_input == "1":
            account_generation = AccountGenerator(database)
            account = Account(account_generation.card_number, account_generation.pin, database)
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
                account = Account(card_number, pin, database)
                print("You have successfully logged in!")
                while True:
                    logged_in_interface()
                    user_input = input()
                    if user_input == "1":
                        print("Balance: " + str(account.get_balance()))
                    elif user_input == "2":
                        print("Enter income:")
                        income_to_add = int(input())
                        account.add_income(income_to_add)
                    elif user_input == "3":
                        print("Transfer")
                        print("Enter card number:")
                        card_number = input()
                        account.make_transaction(card_number)
                    elif user_input == "4":
                        account.close_account()
                        break
                    elif user_input == "5":
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


if __name__ ==  '__main__':
    main()
