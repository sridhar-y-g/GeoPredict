import docx

doc = docx.Document("Intenship001.docx")
print(f"Number of sections: {len(doc.sections)}")
for i, section in enumerate(doc.sections):
    print(f"Section {i} start: {section.start_type}")
