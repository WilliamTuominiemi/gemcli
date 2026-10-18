# Gemcli

## Prerequisites

- Python 3.10+
- [Gemini API key](https://aistudio.google.com/)

## Setup & installation

### 1. Create and activate virtual environment

`python -m venv .venv`

Turn on: `.venv\Scripts\Activate.ps1`

Turn off: `deactivate`

### 2. Configure environment variables

Add to your .env file

```env
GEMINI_API_KEY="api_key"
```

### 3. Install package

`pip install -e .`

## Usage

```
gemcli ask "test.py" "what datatype is variable a"
```