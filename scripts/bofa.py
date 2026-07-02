import argparse
import csv
import sys
from datetime import date, datetime
from pathlib import Path

ACCOUNT_LAST4 = "0449"
POSTED_DATE = "Posted Date"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert BofA statement CSVs for Actual import."
    )
    parser.add_argument(
        "statements_dir",
        nargs="?",
        type=Path,
        default=Path.home() / "Downloads",
        help=f"Directory containing *_{ACCOUNT_LAST4}.csv files (default: ~/Downloads)",
    )
    args = parser.parse_args()

    dir_path = args.statements_dir
    if not dir_path.exists() or not dir_path.is_dir():
        print(f"Error: directory {dir_path} doesn't exist or is not a directory")
        sys.exit(1)

    statement_files = list(dir_path.glob(f"*_{ACCOUNT_LAST4}.csv"))
    if not statement_files:
        print(f"No BofA statements found in {dir_path} for account {ACCOUNT_LAST4}")
        sys.exit(1)

    all_rows = []
    for statement_file in statement_files:
        with open(statement_file, encoding="utf-8", newline="") as infile:
            reader = csv.DictReader(infile)
            rows = list(reader)
            print(f"Read {len(rows)} rows from {statement_file}")
            all_rows.extend(rows)

    if not all_rows:
        print("No rows to write")
        sys.exit(1)

    try:
        all_rows.sort(
            key=lambda x: datetime.strptime(x[POSTED_DATE], "%m/%d/%Y").date()
        )
    except (ValueError, KeyError) as e:
        print(f"Error: Failed to parse '{POSTED_DATE}' field. {e}")
        sys.exit(1)

    out_filename = dir_path / f"bofa_for_actual_{date.today()}.csv"
    with open(out_filename, "w", encoding="utf-8", newline="") as outfile:
        fieldnames = all_rows[0].keys()
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_rows)

    print(f"Wrote {len(all_rows)} rows to {out_filename}")


if __name__ == "__main__":
    main()
