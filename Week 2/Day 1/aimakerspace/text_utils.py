import os
import PyPDF2
from typing import List

class TextFileLoader:
    def __init__(self, path: str, encoding: str = "utf-8"):
        self.documents = []
        self.path = path
        self.encoding = encoding

    def load(self):
        if os.path.isdir(self.path):
            self.load_directory()
        elif os.path.isfile(self.path):
            if self.path.endswith(".txt"):
                self.load_text_file()
            elif self.path.endswith(".pdf"):
                self.load_pdf_file()
            else:
                raise ValueError("Provided file is neither a .txt nor a .pdf file.")
        else:
            raise ValueError("Provided path is not a valid directory or file.")

    def load_text_file(self):
        with open(self.path, "r", encoding=self.encoding) as f:
            self.documents.append(f.read())

    def load_pdf_file(self):
        with open(self.path, "rb") as f:
            pdf_reader = PyPDF2.PdfReader(f)
            pdf_text = []
            for page in pdf_reader.pages:
                pdf_text.append(page.extract_text())
            self.documents.append(' '.join(pdf_text))

    def load_directory(self):
        for root, _, files in os.walk(self.path):
            for file in files:
                if file.endswith(".txt"):
                    with open(os.path.join(root, file), "r", encoding=self.encoding) as f:
                        self.documents.append(f.read())
                elif file.endswith(".pdf"):
                    with open(os.path.join(root, file), "rb") as f:
                        pdf_reader = PyPDF2.PdfReader(f)
                        pdf_text = []
                        for page in pdf_reader.pages:
                            pdf_text.append(page.extract_text())
                        self.documents.append(' '.join(pdf_text))

    def load_documents(self):
        self.load()
        return self.documents

class CharacterTextSplitter:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        assert chunk_size > chunk_overlap, "Chunk size must be greater than chunk overlap"
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split(self, text: str) -> List[str]:
        chunks = []
        start = 0
        while start < len(text):
            end = start + self.chunk_size
            if end < len(text):  # Make sure we're not at the end of the text
                while end > start and text[end] not in ' \t\n':  # Adjust end to the nearest whitespace
                    end -= 1
            chunks.append(text[start:end])
            start = end - self.chunk_overlap  # Move start up by chunk size minus overlap
        return chunks

    def split_texts(self, texts: List[str]) -> List[str]:
        chunks = []
        for text in texts:
            chunks.extend(self.split(text))
        return chunks

if __name__ == "__main__":
    loader = TextFileLoader("data/sample_data")
    loader.load()
    splitter = CharacterTextSplitter()
    chunks = splitter.split_texts(loader.documents)
    print(len(chunks))
    print(chunks[0])
    print("--------")
    print(chunks[1])
    print("--------")
    print(chunks[-2])
    print("--------")
    print(chunks[-1])
