from crewai import Crew
from agents import Names_Extractor, Addresses_Extractor, Contacts_Extractor, Emails_Extractor
from tasks import Names_Extraction, Addresses_Extraction, Contacts_Extraction, Emails_Extraction

from tika import parser
parsed = parser.from_file('./dataset.txt', 'http://localhost:9999/tika')

from langchain_text_splitters import TokenTextSplitter
text_splitter = TokenTextSplitter(chunk_size=2500, chunk_overlap=50)
texts = text_splitter.split_text(parsed["content"])
print(len(texts))
print(texts[0])

# Assemble the crew with a sequential process
Names_Crew = Crew(
    agents = [Names_Extractor],
    tasks = [Names_Extraction],
)
Names_Result = Names_Crew.kickoff(inputs={'text': texts[0]})
print(Names_Result)


Address_Crew = Crew(
    agents = [Addresses_Extractor],
    tasks = [Addresses_Extraction],
)
Address_Result = Address_Crew.kickoff(inputs={'text': texts[0]})
print(Address_Result)


Contacts_Crew = Crew(
    agents = [Contacts_Extractor],
    tasks = [Contacts_Extraction],
)
Contacts_Result = Contacts_Crew.kickoff(inputs={'text': texts[0]})
print(Contacts_Result)


Email_Crew = Crew(
    agents = [Emails_Extractor],
    tasks = [Emails_Extraction],
)
Email_Result = Email_Crew.kickoff(inputs={'text': texts[0]})
print(Email_Result)



