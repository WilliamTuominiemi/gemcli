from pathlib import Path

read_file_declaration = {
    "type": "function",
    "name": "read_file",
    "description": "Reads the contents of a file from disk",
    "parameters": {
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "Path to the file to read",
            },
        },
        "required": ["file_path"],
    },
}


def read_file(file_path: str) -> dict:
    return {"content": Path(file_path).read_text(encoding="utf-8")}
