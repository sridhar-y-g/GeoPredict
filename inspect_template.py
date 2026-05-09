import docx

def detailed_inspect(file_path, limit=30):
    doc = docx.Document(file_path)
    print(f"\n--- DETAILED INSPECTION OF {file_path} ---")
    for i, p in enumerate(doc.paragraphs[:limit]):
        print(f"[{i}] Style: {p.style.name} | Text: {repr(p.text[:100])}")
        if p.runs:
            r = p.runs[0]
            print(f"  - Font={r.font.name}, Size={r.font.size}, Bold={r.font.bold}")

detailed_inspect("Intenship001.docx")
