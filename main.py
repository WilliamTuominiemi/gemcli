import argparse
import difflib
import json
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from rich.console import Console
from declarations import read_file_declaration, read_file

MODEL = "gemini-3.5-flash-lite"


def ask(client, args):
    interaction = client.interactions.create(
        model=MODEL,
        input=f"File: {args.file_path}\nQuestion: {args.question}",
        tools=[read_file_declaration],
    )

    fc = next((s for s in interaction.steps if s.type == "function_call" and s.name == "read_file"), None)
    if fc:
        interaction = client.interactions.create(
            model=MODEL,
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


def edit(client, args):
    path = Path(args.file_path)
    old = read_file(args.file_path)["content"]
    interaction = client.interactions.create(
        model=MODEL,
        input=(
            f"Apply this instruction to the file below: {args.instruction}\n"
            "Reply with ONLY the complete new file content: no explanations, no markdown fences.\n\n"
            f"File: {args.file_path}\n{old}"
        ),
    )
    new = interaction.output_text
    lines = new.strip().splitlines()
    if lines and lines[0].startswith("```") and lines[-1].startswith("```"):
        lines = lines[1:-1]
    new = "\n".join(lines) + "\n"

    console = Console(highlight=False)
    diff = [
        line for line in list(difflib.unified_diff(old.splitlines(), new.splitlines(), n=0, lineterm=""))[2:]
        if not line.startswith("@@")
    ]
    if not diff:
        console.print("No changes proposed.")
        return

    for line in diff:
        console.print(line, style="green" if line.startswith("+") else "red", markup=False)

    if console.input("Apply changes? (y/N) ").strip().lower() in ("y", "yes"):
        path.write_text(new, encoding="utf-8")
        console.print("Changes applied.", style="green")
    else:
        console.print("Aborted, file unchanged.", style="yellow")


def main():
    parser = argparse.ArgumentParser(prog="gemcli", description="gemini cli")
    sub = parser.add_subparsers(required=True)

    ask_p = sub.add_parser("ask")
    ask_p.add_argument("file_path")
    ask_p.add_argument("question")
    ask_p.set_defaults(func=ask)

    edit_p = sub.add_parser("edit")
    edit_p.add_argument("file_path")
    edit_p.add_argument("instruction")
    edit_p.set_defaults(func=edit)

    args = parser.parse_args()

    load_dotenv()
    args.func(genai.Client(), args)


if __name__ == "__main__":
    main()