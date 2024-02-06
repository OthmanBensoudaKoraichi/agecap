import streamlit as st
import datetime
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH


def insert_into_word_doc(doc_path,list_members,df_premiums):
    # Define the doc
    doc = Document(doc_path)

    # Modify df_offer
    doc.tables[0].cell(1, 3).text = datetime.datetime.today().strftime("%d-%m-%Y")
    doc.tables[0].cell(1, 4).text = (datetime.datetime.today() + datetime.timedelta(days=30)).strftime("%d-%m-%Y")

    # Center align the text
    for cell_number in range(3,5):
        for paragraph in doc.tables[0].cell(1, cell_number).paragraphs:
            paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER


    # Format correctly
    for i, member in enumerate(list_members):
        # Extract the date from the current member
        year, month, day = str(member[2]).split('-')  # Assuming the date is at index 2
        date_reformatted = f"{day[:2]}-{month}-{year}"

        # Access the specific cell
        cell = doc.tables[1].cell(i + 1, 1)

        # Clear any existing paragraphs in the cell by removing all but the first paragraph
        for para in cell.paragraphs[1:]:
            p = para._element
            p.getparent().remove(p)

        # Modify the text of the first (and now only) paragraph in the cell
        cell.paragraphs[0].text = date_reformatted

        # Center align the first paragraph
        cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Modify df_premiums
    for i in range(df_premiums.shape[0]):  # df.shape[0] gives the number of rows
        for j in range(df_premiums.shape[1]):  # df.shape[1] gives the number of columns
            cell_value = str(df_premiums.iloc[i, j])
            cell = doc.tables[2].cell(i + 2, j + 1)
            cell.text = cell_value

            # Center align the text in the cell
            paragraphs = cell.paragraphs
            for paragraph in paragraphs:
                paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.save("test_doc.docx")

    return


def create_download_button(pdf_path):
    with open(pdf_path, "rb") as file:
        st.download_button(
            label="Download PDF",
            data=file,
            file_name="document.pdf",
            mime="application/octet-stream"
        )