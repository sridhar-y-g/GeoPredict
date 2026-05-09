import docx

def dump_paragraphs(path, name, start, end):
    print(f"\n{'='*80}")
    print(f"Paragraphs {start}-{end} of: {name}")
    print(f"{'='*80}")
    doc = docx.Document(path)
    for i, p in enumerate(doc.paragraphs):
        if i < start: continue
        if i > end: break
        text = p.text
        align = p.alignment
        print(f"[P{i}] Style={p.style.name} | Align={align} | Text={repr(text[:100])}")
        for j, run in enumerate(p.runs[:2]):
            print(f"  R{j}: Font={run.font.name} Sz={run.font.size} Bold={run.font.bold} Text={repr(run.text[:60])}")

dump_paragraphs("Intenship001.docx", "FRIEND'S REPORT", 0, 5)
dump_paragraphs("Landslide report.docx", "LANDSLIDE REPORT (SOURCE)", 0, 5)
dump_paragraphs("Internship_Cover_Pages_template (Final).docx", "COVER PAGES TEMPLATE", 0, 50)
