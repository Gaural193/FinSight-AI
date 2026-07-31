"""
Lesson 2: Document Chunking (How to eat an elephant)
----------------------------------------------------
AI models have a limit on how much text they can read at once (the "Context Window").
If we have a 100-page report, we must slice it into smaller pieces called "Chunks".

The Danger: If we slice randomly every 100 words, we might cut a sentence in half!
"The company's revenue increased by [SLICE] 10% because of new sales."
If the AI only sees "10% because of new sales.", it loses the context (revenue).

The Solution: OVERLAPPING CHUNKS.
We slice the text, but we let each slice overlap the previous one by a few words.
This acts like "glue" so the context is never lost.

Prerequisites:
pip install langchain-text-splitters
"""

from langchain_text_splitters import RecursiveCharacterTextSplitter

# 1. Our dummy "Financial Report" (Imagine this is a massive PDF)
financial_report = """
Apple Inc. reported its Q3 earnings today. The overall revenue grew by 5% year-over-year. 
This growth was primarily driven by strong iPhone sales in emerging markets. 

However, Mac sales declined by 2% due to supply chain constraints. 
Management expects these constraints to resolve by next quarter.
The CEO mentioned that AI investments will increase by $1 billion next year.
"""

print("--- ORIGINAL REPORT ---\n")
print(financial_report.strip())
print("\n" + "-" * 30 + "\n")

# 2. Set up our "Slicer" (Text Splitter)
# chunk_size: How many characters per slice? (We use a tiny number here for demonstration)
# chunk_overlap: How many characters of "glue" between slices?
splitter = RecursiveCharacterTextSplitter(
    chunk_size=100, 
    chunk_overlap=20,
    separators=["\n\n", "\n", ". ", " ", ""] # Try to split at paragraphs first, then sentences, then words
)

# 3. Perform the chunking!
chunks = splitter.split_text(financial_report)

# 4. Let's look at the results
print(f"We sliced the report into {len(chunks)} chunks!\n")

for i, chunk in enumerate(chunks):
    print(f"--- CHUNK {i + 1} ---")
    print(chunk)
    print(f"(Length: {len(chunk)} characters)\n")

print("--- OBSERVATION ---")
print("Notice how the end of one chunk often repeats at the beginning of the next chunk?")
print("That is the 'Overlap'. It ensures that if a sentence is split, the AI still has the full context!")
