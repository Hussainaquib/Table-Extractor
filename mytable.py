import os
import tkinter as tk
from tkinter import filedialog
import pandas as pd
from img2table.document import Image as Img2TableImage
from img2table.document import PDF
from img2table.ocr import PaddleOCR

# Function to select a file locally
def select_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Select a JPG, PNG, or PDF file",
        filetypes=[("Image or PDF files", "*.jpg *.jpeg *.png *.pdf")]
    )
    return file_path

# Select file
file_path = select_file()
if not file_path:
    print(" No file selected.")
    exit()

print(" Selected:", file_path)

# Initialize OCR
ocr = PaddleOCR(lang="en")

# Detect file type
if file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
    print(" Detected image file")
    doc = Img2TableImage(file_path)
    tables = doc.extract_tables(
        ocr=ocr,
        implicit_rows=True,
        implicit_columns=True,
        borderless_tables=True,
        min_confidence=50
    )

    for i, table in enumerate(tables):
        print(f"\n--- Table {i+1} ---")
        print(table.df)
        table.df.to_csv(f"extracted_table_{i+1}.csv", index=False)
        print(f" Saved: extracted_table_{i+1}.csv")

elif file_path.lower().endswith('.pdf'):
    print(" Detected PDF file")
    pdf_doc = PDF(file_path)
    pdf_tables = pdf_doc.extract_tables(
        ocr=ocr,
        implicit_rows=True,
        implicit_columns=True,
        borderless_tables=True,
        min_confidence=50
    )

    for page_num, page_tables in pdf_tables.items():
        print(f"\n=== Page {page_num+1} ===")
        for i, table in enumerate(page_tables):
            print(f"\n--- Table {i+1} ---")
            print(table.df)
            table.df.to_csv(f"extracted_page{page_num+1}_table{i+1}.csv", index=False)
            print(f" Saved: extracted_page{page_num+1}_table{i+1}.csv")

else:
    print(" Unsupported file type. Please upload a JPG, PNG, or PDF.")
