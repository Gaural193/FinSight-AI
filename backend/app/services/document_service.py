import fitz  # PyMuPDF
from langchain_text_splitters import RecursiveCharacterTextSplitter

class DocumentProcessor:
    def __init__(self):
        # We configure our "slicer" exactly like we did in Lesson 2
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,     # 500 characters per slice
            chunk_overlap=50,   # 50 characters of overlap (the 'glue')
            separators=["\n\n", "\n", ". ", " ", ""]
        )

    def process_pdf_bytes(self, pdf_bytes: bytes) -> list[str]:
        """
        Takes raw PDF bytes, extracts all the text using PyMuPDF,
        and chunks it using LangChain.
        """
        # 1. Open the PDF from raw memory
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        
        full_text = ""
        
        # 2. Extract text from every page
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text = page.get_text()
            if text:
                full_text += text + "\n"
        
        doc.close()
        
        # If the PDF was empty or scanned (image only), we return empty list for now
        if not full_text.strip():
            return []
            
        # 3. Slice the massive text string into chunks
        chunks = self.text_splitter.split_text(full_text)
        
        return chunks

# Create a single instance to be used by our API
document_processor = DocumentProcessor()
