import argparse
import csv
import datetime
import os
import sqlite3
import sys
from dataclasses import dataclass

import requests


@dataclass
class DBCmds:
    table_name: str = 'stock_loans'

    def create_table(self) -> str:
        return f"""CREATE TABLE IF NOT EXISTS {self.table_name} (
            businessDate text,
            symbol text,
            newMarketLoanCount int,
            totalMarketLoanVal float,
            newBilateralLoanCount int,
            totalBilateralLoanVal float
        )"""

    def insert_row(self) -> str:
        return f"""INSERT INTO {self.table_name} VALUES (
            :businessDate,
            :symbol,
            :newMarketLoanCount,
            :totalMarketLoanVal,
            :newBilateralLoanCount,
            :totalBilateralLoanVal
        )
        """

    def update_row(self) -> str:
        return f"""UPDATE {self.table_name} SET
            newMarketLoanCount = :newMarketLoanCount,
            totalMarketLoanVal = :totalMarketLoanVal,
            newBilateralLoanCount = :newBilateralLoanCount,
            totalBilateralLoanVal = :totalBilateralLoanVal
        WHERE businessDate = :businessDate AND (symbol = :symbol OR symbol IS NULL)
        """

    def get_row(self) -> str:
        return f"""SELECT * FROM {self.table_name}
            WHERE businessDate = :businessDate AND (symbol = :symbol OR symbol IS NULL)
        """

    def get_rows(self) -> str:
        return f"SELECT * FROM {self.table_name}"


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('--report-date', default=todays_date(), help='Date to get data for')
    parser.add_argument('--db-file', default='loan_data.db', help='Database file name')
    parser.add_argument('--export-csv', default=False, help='Export database as csv', action=argparse.BooleanOptionalAction)
    parser.add_argument('--csv-file', default='loan_data.csv', help='CSV file name')
    args = parser.parse_args(argv)
    data = get_data(args.report_date)
    insert_data(args.db_file, data)
    if args.export_csv:
        export_csv(args.db_file, args.csv_file)


def get_data(report_date):
    url = 'https://marketdata.theocc.com/mdapi/stock-loan'
    params = {
        'report_date': report_date,
        'report_type': 'daily',
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()['entity']['stockLoanResults']


def todays_date():
    return datetime.date.today().strftime('%Y-%m-%d')


def insert_data(db_file, data):
    cmds = DBCmds()
    connection = sqlite3.connect(os.path.join(os.path.dirname(__file__), db_file))
    cursor = connection.cursor()
    cursor.execute(cmds.create_table())
    for row in data:
        row_exists = len(cursor.execute(cmds.get_row(), row).fetchall())
        cursor.execute(cmds.update_row() if row_exists else cmds.insert_row(), row)
    connection.commit()
    connection.close()


def export_csv(db_file, csv_file):
    connection = sqlite3.connect(os.path.join(os.path.dirname(__file__), db_file))
    cursor = connection.cursor()
    data = cursor.execute(DBCmds().get_rows())
    with open(os.path.join(os.path.dirname(__file__), csv_file), 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['businessDate', 'symbol', 'newMarketLoanCount', 'totalMarketLoanVal', 'newBilateralLoanCount', 'totalBilateralLoanVal'])
        writer.writerows(data)


if __name__ == "__main__":
    main(sys.argv[1:])
