from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client()

with open("test.py", "r") as file:
    content = file.read()

prompt_instructions = "From the code below, change the values of a and b so that the" \
" first condition activates. The output should ONLY contain the code with the intended" \
" section altered, do not return anything else with your response. It should not even" \
" contain ```python, just output plain text"

prompt = prompt_instructions + "\n" + content;

response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents=prompt,
)

with open("test.py", "w", encoding="utf-8") as f:
    f.write(response.text)
