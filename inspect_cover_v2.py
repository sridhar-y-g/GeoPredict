import docx

doc = docx.Document("Intenship001.docx")
for i, p in enumerate(doc.paragraphs[:10]):
    print(f"[{i}] {p.style.name}: {repr(p.text)}")
