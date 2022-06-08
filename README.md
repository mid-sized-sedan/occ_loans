### Overview

Downloads stock loan data from the OCC website (https://www.theocc.com/Market-Data/Market-Data-Reports/Volume-and-Open-Interest/Stock-Loan-Volume) and stores the results in a SQLite database file, with the option to export as a CSV.


### Dependencies
- requests


### Installation
- `git clone https://github.com/mid-sized-sedan/occ_loans.git`
- `cd occ_loans`
- `python -m venv .venv`
- `source ./.venv/bin/activate`
- `pip install requests`


### Supported arguments
```bash
$ python occ_loans.py --help
usage: occ_loans.py [-h] [--report-date REPORT_DATE] [--db-file DB_FILE]
                    [--export-csv | --no-export-csv] [--csv-file CSV_FILE]

options:
  -h, --help            show this help message and exit
  --report-date REPORT_DATE
                        Date to get data for
  --db-file DB_FILE     Database file name
  --export-csv, --no-export-csv
                        Export database as csv (default: False)
  --csv-file CSV_FILE   CSV file name
```

### Example usage
- Basic usage: `python occ_loans.py`
- Export CSV: `python occ_loans.py --export-csv`
