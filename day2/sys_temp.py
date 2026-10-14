
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("API key kaha hai bhai")

client = Groq(api_key=my_api_key)

prompt = " You have to create a brand name for our clothing brand for wesren clothing brand in pakistan. The brand name should be unique, catchy, and memorable. It should also reflect the values and mission of our brand. Please provide a list of 10 potential brand names."

completion = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[
        {
            "role": "system",
            "content": "You are senior brand marketer and desighner. You have to create a brand identity for a new startup."
        },
        {
            "role": "user",
            "content": prompt
        }
    ],
    temperature=2,
    max_completion_tokens=2048,
    top_p=1,
    reasoning_effort="medium",
    stream=True,
)

for chunk in completion:
    print(chunk.choices[0].delta.content or "", end="")