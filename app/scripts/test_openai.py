import os

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(
  api_key=OPENAI_API_KEY
)

response = client.responses.create(
  model="gpt-5-nano",
  input="write a haiku about ArchIe",
  store=True,
)

print(response.output_text);