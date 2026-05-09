import docx

doc = docx.Document("Intenship001.docx")
for i, p in enumerate(doc.paragraphs):
    if "CHAPTER 1" in p.text.upper():
        print(f"CHAPTER 1 found at paragraph {i}: {repr(p.text)}")
        break
