import argparse
import json
from dotenv import load_dotenv
from google import genai
from declarations import read_file_declaration, read_file

def main():
    parser = argparse.ArgumentParser(prog="gemcli", description="gemini cli")
    ask = parser.add_subparsers(required=True).add_parser("ask")
    ask.add_argument("file_path")
    ask.add_argument("question")
    args = parser.parse_args()

    load_dotenv()
    client = genai.Client()
    model = "gemini-3.5-flash-lite"

    interaction = client.interactions.create(
        model=model,
        input=f"File: {args.file_path}\nQuestion: {args.question}",
        tools=[read_file_declaration],
    )

    fc = next((s for s in interaction.steps if s.type == "function_call" and s.name == "read_file"), None)
    if fc:
        interaction = client.interactions.create(
            model=model,
            input=[{
                "type": "function_result",
                "name": fc.name,
                "call_id": fc.id,
                "result": [{"type": "text", "text": json.dumps(read_file(**fc.arguments))}],
            }],
            tools=[read_file_declaration],
            previous_interaction_id=interaction.id,
        )

    print(interaction.output_text)


if __name__ == "__main__":
    main()