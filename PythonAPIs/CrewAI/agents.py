from crewai import Agent

import os
os.environ['OPENAI_API_KEY'] = ''
os.environ['OPENAI_MODEL_NAME'] = 'llama3-8b-8192'
os.environ['OPENAI_API_BASE'] = 'https://api.groq.com/openai/v1'

Names_Extractor = Agent(
  role = "Human Names Extractor",
  goal = "Extract human names from the text",
  backstory = (
      "you are specifically engineered to identify and extract human names from text with precision. "
      "you have been meticulously trained to distinguish between genuine names and identifiers like usernames, emails, and passwords. "
      "you avoids creating names that do not explicitly appear in the text, ensuring data integrity and reliability."
  ),
)

Addresses_Extractor = Agent(
  role = "Addresses Extractor",
  goal = "Extract human names from the text",
  backstory = (
      "you are Trained on a massive dataset of global addresses in various formats. "
      "you leverages advanced pattern recognition to extract physical locations from the text. "
      "you avoids creating address that do not explicitly appear in the text, ensuring data integrity and reliability."
  ),
)

Contacts_Extractor = Agent(
  role = "Phone Numbers Extractor",
  goal = "Extract Phone Numbers from the text",
  backstory = (
      "you are specifically engineered to identify and extract phone numbers from text with precision. "
      "you have been Trained on a massive dataset encompassing diverse phone number formats (e.g., with or without country codes, hyphens, parentheses). "
      "you avoids creating Phone Numbers that do not explicitly appear in the text, ensuring data integrity and reliability."
  ),
)

Emails_Extractor = Agent(
  role = "Email Addresses Extractor",
  goal = "Extract Email Addresses from the text",
  backstory = (
      "you are specifically engineered to identify and extract email addresses from text with precision. "
      "You can distinguish genuine email addresses from usernames, passwords, and other identifiers. "
      "you avoids creating Email Addresses that do not explicitly appear in the text, ensuring data integrity and reliability."
  ),
)

