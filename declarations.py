ask_declaration = {
    "type": "function",
    "name": "ask",
    "description": "Answers a question about code",
    "parameters": {
        "type": "object",
        "properties": {
            "code": {
                "type": "string",
                "description": "The input code"
            },
            "question": {
                "type": "string",
                "description": "The question that is asked about the code"
            }
        },
        "required": ["code", "question"],
    }
}

def ask(code: str, question: str) -> dict:
    return {"code": code, "question": question}