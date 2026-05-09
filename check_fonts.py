import docx

doc = docx.Document("Intenship001.docx")
style = doc.styles['Normal']
font = style.font
print(f"Normal style: Font={font.name}, Size={font.size}")

style = doc.styles['Heading 1']
font = style.font
print(f"Heading 1 style: Font={font.name}, Size={font.size}")
