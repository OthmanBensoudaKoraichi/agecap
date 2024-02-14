import pypandoc

def convert_docx_to_html(docx_path, output_html_path):
    output = pypandoc.convert_file(docx_path, 'html', outputfile=output_html_path)
    return output

# Example usage
docx_path = '/Users/othmanbensouda/PycharmProjects/Agecap Automatic Forms/files/devis_agecap.docx'
output_html_path = '/Users/othmanbensouda/PycharmProjects/Agecap Automatic Forms/files/devis_agecap.html'
convert_docx_to_html(docx_path, output_html_path)