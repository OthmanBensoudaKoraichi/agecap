import datetime
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
import tempfile
from docx2pdf import convert
import os


def insert_into_word_doc(doc_path, list_members, df_premiums,id_devis):
    # Define the doc
    doc = Document(doc_path)

    # Modify df_offer
    doc.tables[0].cell(1, 2).text = id_devis
    doc.tables[0].cell(1, 3).text = datetime.datetime.today().strftime("%d-%m-%Y")
    doc.tables[0].cell(1, 4).text = (
        datetime.datetime.today() + datetime.timedelta(days=30)
    ).strftime("%d-%m-%Y")

    # Center align the text
    for cell_number in range(2, 5):
        for paragraph in doc.tables[0].cell(1, cell_number).paragraphs:
            paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    # Iterate over family members to format and insert data into the second table
    for i, member in enumerate(list_members):
        # Assuming the date of birth is at index 2 in the member tuple
        year, month, day = str(member[2]).split("-")
        date_reformatted = f"{day[:2]}-{month}-{year}"

        # Assuming the relation type is at index 3 in the member tuple
        relation = member[3]

        # Insert the date into the specified cell (column 2)
        cell_date = doc.tables[1].cell(i + 1, 2)
        cell_date.text = date_reformatted
        cell_date.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

        # Insert the relation into the specified cell (column 1)
        cell_relation = doc.tables[1].cell(i + 1, 1)

        # Clear any existing paragraphs in the cell by removing all but the first paragraph
        for para in cell_relation.paragraphs[1:]:
            p = para._element
            p.getparent().remove(p)

        # Modify the text of the first (and now only) paragraph in the cell
        cell_relation.paragraphs[0].text = relation
        cell_relation.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

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

    # Use tempfile to create a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
        doc.save(tmp.name)
        docx_path = tmp.name

    # Convert the docx to pdf
    #pdf_path = docx_path.replace(".docx", ".pdf")
    #convert(docx_path, pdf_path)

    # Make sure to remove the temporary docx file if you no longer need it
    #os.unlink(docx_path)

    #return pdf_path

    return docx_path


# Function to read the file and return its contents
def load_file(file_path):
    with open(file_path, 'rb') as file:
        return file.read()


