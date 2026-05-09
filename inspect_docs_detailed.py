import docx

def detailed_inspect(file_path, limit=50):
    doc = docx.Document(file_path)
    print(f"\n--- DETAILED INSPECTION OF {file_path} ---")
    for i, p in enumerate(doc.paragraphs[:limit]):
        print(f"[{i}] Style: {p.style.name} | Text: {repr(p.text[:100])}")
        for r in p.runs[:3]: # first 3 runs
            print(f"  - Run: Font={r.font.name}, Size={r.font.size}, Bold={r.font.bold}, Italic={r.font.italic}, Text={repr(r.text[:50])}")

detailed_inspect("Intenship001.docx")
detailed_inspect("Landslide report.docx")
