from docx import Document

doc = Document("ELP-Form.docx")

doc.tables[0].add_row()
doc.tables[0].rows[1].cells[0].add_paragraph("shit")

doc.save("test.docx")