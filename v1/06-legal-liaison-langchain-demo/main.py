from app import text_summarization, read_and_formally_summarize_text, summarize_pdf

print("Reading and summarizing document...\n")
formal_summary = summarize_pdf("doc.pdf")
print("\n\n [Simple Summary]")
summary = ""
for text_summary in formal_summary:
    summary = summary + text_summary[4] + "\n"
summary = text_summarization(summary)
print(summary)

