from langchain_text_splitters import TokenTextSplitter
text_splitter = TokenTextSplitter(chunk_size=1024, chunk_overlap=50)

from tika import parser
parsed = parser.from_file("E:/Training_Dataset/Persons.csv", 'http://localhost:9999/tika')

texts = text_splitter.split_text(parsed["content"])
print(texts[0])