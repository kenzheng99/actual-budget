import csv
import sys
from datetime import date
from pathlib import Path

VENMO_BALANCE = "Venmo balance"
OWNER_NAME = "Kenneth Zheng"
PAYEE_NAME = "Venmo Transaction"


def parse_single_stmt(filepath: Path) -> list[dict[str, str]]:
    # input format:
    # - row 0-1: title (skip)
    # - row 2: headers
    # - row 3: blank
    # - row 4: data start
    # - row -1: total (skip)

    with open(filepath, encoding="utf-8") as file:
        csvreader = csv.reader(file)
        # Skip rows 0-1 (title)
        next(csvreader)
        next(csvreader)
        # Read row 2 (headers)
        headers = next(csvreader)
        # Skip row 3 (blank)
        next(csvreader)
        # Read data rows with DictReader
        dictreader = csv.DictReader(file, fieldnames=headers)
        rows = list(dictreader)
        # Skip last row (total)
        rows = rows[:-1] if rows else []

    # output format:
    # - Date: e.g. "2025-12-16T20:40:28"
    # - Payee: "Venmo"
    # - Memo: e.g. "Lunch (Mia Hotsuki)"
    # - Amount: number (+ or -)

    transactions = []
    for txn in rows:
        # skip bank transactions
        if (
            txn.get("Funding Source") != VENMO_BALANCE
            and txn.get("Destination") != VENMO_BALANCE
        ):
            continue

        person = txn["To"] if txn["From"] == OWNER_NAME else txn["From"]
        memo = f"{txn['Note']} ({person})"

        transactions.append(
            {
                "Date": txn["Datetime"],
                "Payee": PAYEE_NAME,
                "Memo": memo,
                "Amount": txn["Amount (total)"],
            }
        )

    print(f"Read {len(transactions)} rows from {filepath}")
    return transactions


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python venmo.py path/to/statements")
        sys.exit(1)

    dir_path = Path(sys.argv[1])
    if not dir_path.exists() or not dir_path.is_dir():
        print(f"Error: directory {dir_path} doesn't exist or is not a directory")
        sys.exit(1)

    statement_files = list(dir_path.glob("VenmoStatement*.csv"))
    if not statement_files:
        print(f"No Venmo statement files found in {dir_path}")
        sys.exit(1)

    all_transactions = []
    for stmt in statement_files:
        all_transactions.extend(parse_single_stmt(stmt))

    if not all_transactions:
        print("No rows to write")
        sys.exit(1)

    all_transactions.sort(key=lambda x: x["Date"])

    output_path = dir_path / f"venmo_for_actual_{date.today()}.csv"
    with open(output_path, "w", encoding="utf-8") as outfile:
        fieldnames = ["Date", "Payee", "Memo", "Amount"]
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in all_transactions:
            writer.writerow(row)

    print(f"Wrote {len(all_transactions)} rows to {output_path}")
