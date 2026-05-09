import docx

doc = docx.Document("Intenship001.docx")
for i in range(10):
    p = doc.paragraphs[i]
    print(f"[{i}] {p.style.name}: {repr(p.text)}")
