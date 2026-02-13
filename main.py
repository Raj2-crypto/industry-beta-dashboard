import pandas as pd
import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)
from Utils.get_financial_data import get_financial_data
from Utils.calc_unlevered_betas import calc_unlevered_betas 


# COMPANIES = [
#     "AIR","AVAV","ASLE","AIRI","AIRO","AERG","ACHR","ATRO","ATI","AXON",
#     "BETA","BUKS","BWXT","BYRN","CDRE","CRS","2507.HK","CVU","CW","DCO",
#     "BRQL","ETCC","EVEX","FLY","GD","GE","HEI","HLEO","HXL","HWM",
#     "HII","ISSC","IRBL","LUNR","KRMN","KTOS","LHX","DRS","LOAR",
#     "LMT","MRCY","MNTS","MOG.A","MNDP","BLIS","NPK","NOC","OPXS","PKE",
#     "PSSR","PMBY","VNUE.D","RDW","RKLB","RTX","SPAI","SAFS","SATL","SRBT",
#     "SIDU","SIF","SARO","FJET","SKFG","TXT","BA","TDG","UMAV","UATG",
#     "UITA","VVX","SPCE","VTSI","VWAV","VOYG","VSEC","WWD","XNNH.Q","XERI"
# ]


def run_industry_analysis(companies):
    results = []

    for company in companies:
        data = get_financial_data(company)

        if data is not None:
            results.append(data)

    df = pd.DataFrame(results)
    summary = calc_unlevered_betas(df)

    return df, summary




# if __name__ == "__main__":
#     print("=" * 80)
#     print("FETCHING FINANCIAL DATA WITH DYNAMIC CURRENCY CONVERSION TO INR")
#     print("=" * 80)

#     results = []
#     for company in COMPANIES:
#         print(f"Processing {company}...")
#         results.append(get_financial_data(company))

#     df = pd.DataFrame(results)

#     print("\n" + "=" * 80)
#     print("FINANCIAL DATA SUMMARY (All monetary values in INR Millions)")
#     print("=" * 80)
#     print(df.to_string(index=False))

#     summary = calc_unlevered_betas(df)

#     print("\n" + "=" * 80)
#     print("CAPITAL STRUCTURE & BETA SUMMARY")
#     print("=" * 80)
#     for k, v in summary.items():
#         print(f"{k}: {v}")
