import os
import sys
import pandas as pd
from Utils.get_financial_data import get_financial_data

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)  

def main():
    companies = [
    "HON",          # Honeywell (US)
        "CW",           # Curtiss-Wright (US)
        "PH",           # Parker Hannifin (US)
        "AME",          # AMETEK (US)
        "BA.L",         # BAE Systems (UK)
        "RTX",          # RTX (Raytheon) (US)
        "NOC",          # Northrop Grumman (US)
        "LHX",          # L3Harris Technologies (US)
        "HO.PA",        # Thales (France)
        "SAAB-B.ST",    # Saab (Sweden)
        "RHM.DE",       # Rheinmetall (Germany)
        "TATT"          # TAT Technologies (US/Isr
    ]

    results = []

    print("=" * 80)
    print("FETCHING FINANCIAL DATA WITH DYNAMIC CURRENCY CONVERSION TO INR")
    print("=" * 80)

    for company in companies:
        print(f"Processing {company}...")
        results.append(get_financial_data(company))

    # Create DataFrame
    df = pd.DataFrame(results)

    # Display results
    print("\n" + "=" * 80)
    print("FINANCIAL DATA SUMMARY (All monetary values in INR Millions)")
    print("=" * 80)
    print(df.to_string(index=False))

# if __name__ == "__main__":
#     main()