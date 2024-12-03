from pydantic import BaseModel
from crewai import Task
from agents import Names_Extractor, Addresses_Extractor, Contacts_Extractor, Emails_Extractor, SSNs_Extractor 

class Names(BaseModel):
    Names: list = []

class Addresses(BaseModel):
    Addresses: list = []

class PhoneNumbers(BaseModel):
    Contacts: list = []

class Emails(BaseModel):
    Emails: list = []

class SSNs(BaseModel):
    SSNs: list = []

class Passports(BaseModel):
    Passports: list = []

class Driverlicenses(BaseModel):
    Driverlicenses: list = []

Names_Extraction = Task(
    description = "[TEXT STARTS]\n{text}\n[TEXT ENDS]",
    agent = Names_Extractor,
    expected_output = (
        "Provide a JSON object with the key `Names`, containing a list of unique human names extracted from the text. "
        "If no names are found, then the list should be empty."
    ),
    output_json=Names,
)

Addresses_Extraction = Task(
    description="[TEXT STARTS]\n{text}\n[TEXT ENDS]",
    agent=Addresses_Extractor,
    expected_output=(
        "Provide JSON object with the key `Addresses`, containing a list of unique physical location Addresses extracted from text. "
        "If no addresses are found, then the list should be empty."
    ),
    output_json=Addresses,
)

Contacts_Extraction = Task(
    description="[TEXT STARTS]\n{text}\n[TEXT ENDS]",
    agent=Contacts_Extractor,
    expected_output=(
        "Provide JSON object with the key `PhoneNumbers`, containing a list of unique Phone Numbers extracted from text. "
        "phone numbers may be with or without country code, If no phone numbers are found, then the list should be empty."
    ),
    output_json=PhoneNumbers,
)

Emails_Extraction = Task(
    description="[TEXT STARTS]\n{text}\n[TEXT ENDS]",
    agent=Emails_Extractor,
    expected_output=(
        "Provide JSON object with the key `Emails`, containing a list of unique Email Addresses extracted from text. "
        "If no email addresses are found, then the list should be empty."
    ),
    output_json=Emails,
)

