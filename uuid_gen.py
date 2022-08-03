"""
uuid_gen.py
Quickly generate a CSV file with UUIDs and random countries.
This data is completely fictional, and is used solely for testing.
"""
import csv
import uuid
import random


def generate_csv(amount):
    countries = [
        'Belgium',
        'The Netherlands',
        'France',
        'Germany',
        'United States of America',
        'Luxembourg',
        'Portugal',
        'Spain',
        'Sweden',
        'Finland',
        'Norway',
        'United Kingdom',
        'Ireland',
        'Poland',
        'Ukraine',
        'Japan',
        'South Korea',
        'Australia'
    ]
    with open('testdata_uuid.csv', 'w') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(['UUID', 'Country'])
        for row in range(amount):
            filewriter.writerow([str(uuid.uuid4()), countries[random.randint(0, len(countries)-1)]])

        csvfile.close()


if __name__ == '__main__':
    generate_csv(40)
