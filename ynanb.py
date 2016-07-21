# ynanb (You need a Nordea Budget) by Ian Tuomi (iant@iki.fi), MIT Licence

import csv
import datetime
import itertools

def convertDate(nordea_date):
    return { 'Date': nordea_date.replace('.', '/') }

def convertFlow(amount_string):
    # e.g. -7,40
    # n.b. This can result in rounding errors
    amount = round(float(amount_string.replace(',', '.')), 2)
    if amount > 0:
        return { 'Inflow': amount }
    else:
        return { 'Outflow': -amount }

def convertMessage(msg):
    return { 'Memo': msg }

def convertPayee(payee):
    return { 'Payee': payee }

converters = {
    'Kirjauspäivä': convertDate,
    'Määrä': convertFlow,
    'Saaja/Maksaja': convertPayee,
    'Viesti': convertMessage
}

in_file_name = 'nordea_example.txt'
ynab_fields = ['Date', 'Payee', 'Category', 'Memo', 'Outflow', 'Inflow']
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
    writer = csv.DictWriter(out_file, fieldnames=ynab_fields)
    writer.writeheader()
    for row in output:
        writer.writerow(row)