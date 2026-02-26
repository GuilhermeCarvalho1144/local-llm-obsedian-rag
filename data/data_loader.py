from llama_index.readers.file import PDFReader, MarkdownReader
from llama_index.core.node_parser import SentenceSplitter
from FlagEmbedding import FlagAutoModel

model = FlagAutoModel.from_finetuned("BAAI/bge-m3", device="cuda:0")

spliter = SentenceSplitter(
    chunk_size=1000,
    chunk_overlap=200,
)


def load_and_chunk_pdf(path: str):
    docs = PDFReader().load_data(file=path)
    texts = [doc.text for doc in docs if getattr(doc, "text", None)]
    chunks = []
    for text in texts:
        chunks.extend(spliter.split_text(text))
    return chunks


def load_and_chunk_markdown(path: str):
    docs = MarkdownReader().load_data(file=path)
    texts = [doc.text for doc in docs if getattr(doc, "text", None)]
    chunks = []
    for text in texts:
        chunks.extend(spliter.split_text(text))
    return chunks


def embed_chunks(chunks):
    embeddings = model.encode(chunks)
    return embeddings
