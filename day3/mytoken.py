import os

from dotenv import load_dotenv
from groq import Groq


load_dotenv()

my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("API key kaha hai bhai")

client = Groq(api_key=my_api_key)


# We will give 3 different prompts
prompt1 = "Hi!"
prompt2 = "Explain time traveling in detail."
prompt3 = "Write a 500-word essay on AI engineering and its scope in the technical field."

prompts = [prompt1, prompt2, prompt3]


for prompt in prompts:

    messages = [
        {
            "role": "system",
            "content": "You are a helpful and knowledgeable AI assistant."
        },
        {
            "role": "user",
            "content": prompt
        }
    ]

    completion = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=messages,
        temperature=1,
        max_completion_tokens=2048,
        top_p=1,
        reasoning_effort="medium",
        stream=False,
    )

    usage = completion.usage

    print(
        f"\nPrompt: {prompt}"
        f"\nTokens used: {usage.total_tokens}"
        f"\nPrompt tokens: {usage.prompt_tokens}"
        f"\nCompletion tokens: {usage.completion_tokens}"
    )

    print("\n--- RESPONSE ---")

    print(completion.choices[0].message.content)
