#!/usr/bin/env python3

# ynanb (You Need a Nordea Budget) by Ian Tuomi (iant@iki.fi), MIT Licence

import csv
import datetime
import itertools
import sys

YNAB_FIELDS = ['Date', 'Payee', 'Category', 'Memo', 'Outflow', 'Inflow']

def convert_date(nordea_date):
    return { 'Date': nordea_date.replace('.', '/') }

def convert_flow(amount_string):
    # Input e.g. -7,40
    # n.b. Using round on float may result in rounding errors
    amount = round(float(amount_string.replace(',', '.')), 2)
    if amount > 0:
        return { 'Inflow': amount }
    else:
        return { 'Outflow': -amount }

def convert_message(msg):
    return { 'Memo': msg }

def convert_payee(payee):
    return { 'Payee': payee }

converters = {
    'Kirjauspäivä': convert_date,
    'Määrä': convert_flow,
    'Saaja/Maksaja': convert_payee,
    'Viesti': convert_message
}

def main(in_file_name = 'nordea.txt'):
    output = []

    with open(in_file_name) as in_file:
        # Skip first two lines, and every other line afterwards
        sliced_file = itertools.islice(in_file, 2, None, 2)
        reader = csv.DictReader(sliced_file, delimiter='\t')
        for input_row in reader:
            output_row = {}
            for key, value in input_row.items():
                if key in converters:
                    output_row.update(converters[key](value))
            output.append(output_row)

    with open('ynab_{}'.format(in_file_name), 'w') as out_file:
        writer = csv.DictWriter(out_file, fieldnames=YNAB_FIELDS)
        writer.writeheader()
        for row in output:
            writer.writerow(row)

if __name__ == '__main__':
    main() if len(sys.argv) < 2 else main(sys.argv[1])
