import json
from dotenv import load_dotenv
from google import genai
from declarations import ask_declaration, ask

load_dotenv()

client = genai.Client()

interaction = client.interactions.create(
    model="gemini-3.8-flash",
    input="Code: `x = 1 + 1`. Question: What is the value of x?",
    tools=[ask_declaration],
)

fc_step = next((s for s in interaction.steps if s.type == "function_call"), None)
if fc_step and fc_step.name == "ask":
    result = ask(**fc_step.arguments)
    print(f"Function execution result: {result}")

    final_interaction = client.interactions.create(
        model="gemini-3.8-flash",
        input=[
            {
                "type": "function_result",
                "name": fc_step.name,
                "call_id": fc_step.id,
                "result": [{"type": "text", "text": json.dumps(result)}],
            }
        ],
        tools=[ask_declaration],
        previous_interaction_id=interaction.id,
    )

    print(final_interaction.output_text)
else:
    print(interaction.output_text)