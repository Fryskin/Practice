import json
import os
from datetime import datetime

import requests

CURRENCY_RATES_FILE = 'currency_rates.json'


def main():
    while True:
        currency_from = input('\nSelect the currency you want to transfer from:'
                              '\n1.USD\n2.EUR\n3.RUB\n4.CZK\n5.GBP\n6.CHF\n7.JPY\nEnter: ')

        if currency_from not in ('1', '2', '3', '4', '5', '6', '7'):
            print('Wrong enter.\n')
            continue

        if currency_from == '1':
            currency_from = 'USD'
        elif currency_from == '2':
            currency_from = 'EUR'
        elif currency_from == '3':
            currency_from = 'RUB'
        elif currency_from == '4':
            currency_from = 'CZK'
        elif currency_from == '5':
            currency_from = 'GBP'
        elif currency_from == '6':
            currency_from = 'CHF'
        elif currency_from == '7':
            currency_from = 'JPY'

        currency_to = input('\nSelect the currency you want to transfer to:'
                            '\n1.USD\n2.EUR\n3.RUB\n4.CZK\n5.GBP\n6.CHF\n7.JPY\nEnter: ')

        if currency_to not in ('1', '2', '3', '4', '5', '6', '7'):
            print('Wrong enter.\n')
            continue

        if currency_to == '1':
            currency_to = 'USD'
        elif currency_to == '2':
            currency_to = 'EUR'
        elif currency_to == '3':
            currency_to = 'RUB'
        elif currency_to == '4':
            currency_to = 'CZK'
        elif currency_to == '5':
            currency_to = 'GBP'
        elif currency_to == '6':
            currency_to = 'CHF'
        elif currency_to == '7':
            currency_to = 'JPY'

        amount = input('\nEnter amount: ')
        if amount.isdigit() is False:
            print('Wrong enter.')
            continue

        rate = get_currency_rate(currency_from, currency_to)
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        result = get_convert(currency_from, currency_to, int(amount))

        print(f"\nRate of {currency_from} to {currency_to}: {rate} ")
        print(f"{amount} {currency_from} = {result} {currency_to}")

        data = {'currency_from': currency_from, 'currency_to': currency_to, 'rate': rate, 'timestamp': timestamp}
        save_to_json_file(data)

        user_choice = input('\nSelect action:\n1.Continue\n2.Exit\nEnter: ')
        if user_choice == '1':
            continue
        elif user_choice == '2':
            break
        else:
            print('Wrong enter.')


def get_currency_rate(transfer_from: str, transfer_to: str) -> float:
    url = f"https://api.apilayer.com/exchangerates_data/latest"

    headers = {"apikey": "6P1XTawkoro3KuC72gOpmQRNzrmK2lOe"}

    response = requests.get(url, headers=headers, params={'base': transfer_from})
    rate = response.json()['rates'][transfer_to]

    return rate


def get_convert(transfer_from: str, transfer_to: str, amount: int) -> float:
    url = f"https://api.apilayer.com/exchangerates_data/convert?to={transfer_to}&from={transfer_from}&amount={amount}"

    headers = {"apikey": "6P1XTawkoro3KuC72gOpmQRNzrmK2lOe"}

    response = requests.get(url, headers=headers)
    result = response.json()["result"]

    return result


def save_to_json_file(data: dict) -> None:
    with open(CURRENCY_RATES_FILE, 'a') as f:
        if os.stat(CURRENCY_RATES_FILE).st_size == 0:
            json.dump([data], f)
        else:
            with open(CURRENCY_RATES_FILE) as file:
                data_list = json.load(file)
                data_list.append(data)
            with open(CURRENCY_RATES_FILE, 'w') as f:
                json.dump(data_list, f)


if __name__ == '__main__':
    main()
