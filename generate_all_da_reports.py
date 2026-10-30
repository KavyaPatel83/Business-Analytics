"""
generate_all_da_reports.py
Master execution script that generates all three Digital Assignment (DA) reports in PDF format:
1. DA 1: Problem / Idea of the Model -> DA1_Problem_Idea_Report.pdf
2. DA 2: Software / Model Implementation -> DA2_Implementation_Report.pdf
3. DA 3: Final Report and Results -> DA3_Final_Report_And_Results.pdf

Course: Business Analytics (BMGT107L)
Institution: Vellore Institute of Technology (VIT), Chennai
Faculty: BALAJI J
Students: PATEL KAVYA VIPULKUMAR (23BDS1076), SAHIL KUMAR (23BDS1099)
"""

import os
import sys
import time

def run_all():
    print("=" * 70)
    print("VELLORE INSTITUTE OF TECHNOLOGY (VIT) CHENNAI")
    print("BUSINESS ANALYTICS (BMGT107L) - DIGITAL ASSIGNMENTS REPORT SUITE")
    print("Students: Patel Kavya Vipulkumar (23BDS1076) & Sahil Kumar (23BDS1099)")
    print("Faculty: Prof. BALAJI J | Slot: G2 + TG2")
    print("=" * 70)

    start_time = time.time()

    # Step 1: Generate DA 1
    print("\n[1/3] Synthesizing DA 1: Problem / Idea of the Model...")
    from generate_da1_pdf import build_da1_report_pdf
    build_da1_report_pdf()

    # Step 2: Generate DA 2
    print("\n[2/3] Synthesizing DA 2: Software / Model Implementation...")
    from generate_da2_pdf import build_da2_report_pdf
    build_da2_report_pdf()

    # Step 3: Generate DA 3
    print("\n[3/3] Synthesizing DA 3: Final Report and Results...")
    from generate_da3_pdf import build_da3_report_pdf
    build_da3_report_pdf()

    elapsed = time.time() - start_time
    print("\n" + "=" * 70)
    print(f"ALL 3 DA REPORTS SUCCESSFULLY GENERATED IN {elapsed:.2f} SECONDS!")
    print("=" * 70)

    files = [
        ("DA 1: Problem / Idea of the Model", "DA1_Problem_Idea_Report.pdf"),
        ("DA 2: Software / Model Implementation", "DA2_Implementation_Report.pdf"),
        ("DA 3: Final Report and Results", "DA3_Final_Report_And_Results.pdf")
    ]

    import pymupdf
    for title, fname in files:
        if os.path.exists(fname):
            doc = pymupdf.open(fname)
            sz_kb = os.path.getsize(fname) / 1024
            print(f"  * {title}:")
            print(f"      File: {fname}")
            print(f"      Pages: {len(doc)} pages | Size: {sz_kb:.1f} KB\n")

if __name__ == "__main__":
    run_all()

