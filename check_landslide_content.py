import docx

doc = docx.Document("Landslide report.docx")
for i, p in enumerate(doc.paragraphs[:30]):
    print(f"[{i}] {p.text[:100]}")
