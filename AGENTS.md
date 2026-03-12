# AGENTS.md - Agentic Coding Guidelines

## Project Overview

This is a Python learning workspace containing multiple Discord bot projects:
- `py_discordBot/` - Main Discord bot with scheduled messaging
- `class_discord/` - Discord.py tutorial materials
- `gui_lesson/` - GUI learning examples
- `job_file/` - Example scripts and utilities

**Python Version**: 3.12
**Virtual Environment**: `.venv` (use `.venv/bin/python` to run scripts)

---

## Build / Run Commands

### Running Python Scripts
```bash
# Activate venv and run
source .venv/bin/activate
python script.py

# Or run directly with venv Python
.venv/bin/python script.py

# Run specific module
python -m py_discordBot.discode_bot
```

### Running Tests
Currently **no formal test framework** is configured. To add testing:

```bash
# Install pytest
.venv/bin/python -m pip install pytest pytest-asyncio

# Run all tests
pytest

# Run single test file
pytest tests/test_filename.py

# Run single test function
pytest tests/test_filename.py::test_function_name

# Run with verbose output
pytest -v

# Run tests matching pattern
pytest -k "test_pattern"
```

### Type Checking (Optional - Recommended)
```bash
# Install mypy
.venv/bin/python -m pip install mypy

# Type check specific file
mypy filename.py

# Type check with strict mode
mypy --strict filename.py
```

---

## Code Style Guidelines

### Imports

**Standard Order** (per PEP 8):
1. Standard library (`os`, `sys`, `datetime`, etc.)
2. Third-party libraries (`discord`, `dotenv`, `asyncio`)
3. Local project imports

```python
# ✅ Correct
import os
import asyncio
from datetime import datetime

import discord
from dotenv import load_dotenv

from py_discordBot import discode_bot
```

```python
# ❌ Wrong - random order
from dotenv import load_dotenv
import os
import discord
```

**Avoid**:
- Wildcard imports (`from module import *`)
- Importing too many modules in one line (`import os, sys, json`)

---

### Formatting

- **Indentation**: 4 spaces (no tabs)
- **Line Length**: Maximum 100 characters
- **Blank Lines**: 2 blank lines between top-level definitions
- **Spaces around operators**: `a = b` not `a=b`

```python
# ✅ Correct
def function_name(param1, param2):
    """Short description.
    
    Longer description if needed.
    """
    result = param1 + param2
    return result


class MyClass:
    def method(self):
        pass
```

---

### Type Annotations

**Recommended** - Add type hints for better code clarity:

```python
# ✅ Good - with type hints
def calculate_sum(numbers: list[int]) -> int:
    """Calculate sum of numbers."""
    return sum(numbers)

def greet(name: str, times: int = 1) -> str:
    """Greet user multiple times."""
    return ", ".join([f"Hello, {name}!"] * times)

# For complex types
from typing import Optional, List, Dict
async def process_data(items: List[int]) -> Dict[str, int]:
    return {"total": sum(items), "count": len(items)}
```

```python
# ❌ Avoid - no type hints
def calculate_sum(numbers):
    return sum(numbers)
```

---

### Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Functions | snake_case | `send_message()`, `get_user_data()` |
| Variables | snake_case | `user_id`, `message_list` |
| Classes | PascalCase | `DiscordClient`, `ScheduleButton` |
| Constants | UPPER_SNAKE_CASE | `MAX_RETRY`, `DEFAULT_CHANNEL` |
| Modules/Files | snake_case | `discode_bot.py`, `utils.py` |

```python
# ✅ Correct
class ScheduleButton:
    MAX_MESSAGE_LENGTH = 2000
    
    def __init__(self, user_id: int):
        self.user_id = user_id

# ✅ Correct
USER_ID = 123456789
def get_user_name():
    user_name = "example"
    return user_name

# ❌ Wrong
class schedule_button:
    def SendMessage():
        USERID = 123
```

---

### Error Handling

**Always** handle exceptions properly:

```python
# ✅ Good - specific exception handling
try:
    result = await channel.send(message)
except discord.errors.Forbidden:
    print("Cannot send message to this channel")
except discord.errors.HTTPException as e:
    print(f"HTTP error occurred: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
    raise  # Re-raise unexpected errors
```

```python
# ❌ Bad - empty catch
try:
    risky_operation()
except:
    pass

# ❌ Bad - catching too broad
try:
    risky_operation()
except Exception:  # Too broad, hides bugs
    print("Error")
```

**Use context managers** for resource management:
```python
# ✅ Good
with open("file.txt", "r") as f:
    content = f.read()
```

---

### Async/Await Patterns

Discord.py uses async - follow these patterns:

```python
# ✅ Correct - proper async functions
async def fetch_data(url: str) -> dict:
    """Fetch data from URL."""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

# ✅ Correct - running async in sync context
import asyncio

def sync_wrapper():
    asyncio.run(async_function())

# ❌ Wrong - blocking call in async
async def bad_example():
    time.sleep(5)  # Blocks event loop!
    await asyncio.sleep(5)  # Correct
```

---

### Discord.py Specific Guidelines

**Required intents setup**:
```python
intents = discord.Intents.default()
intents.message_content = True  # Required for reading messages
intents.members = True         # Required for member events
```

**Always check bot's own messages**:
```python
@client.event
async def on_message(message):
    if message.author == client.user:
        return  # Prevent infinite loops
    # Process message...
```

**Use views for interactivity**:
```python
from discord.ui import Button, View

class MyView(View):
    @discord.ui.button(label="Click Me", style=discord.ButtonStyle.primary)
    async def button_callback(self, interaction, button):
        await interaction.response.send_message("Clicked!")
```

---

### Docstrings

Use Google-style or simple docstrings:

```python
def function(param1: str, param2: int = 10) -> bool:
    """Short one-line description.
    
    Longer description if needed.
    
    Args:
        param1: Description of param1
        param2: Description of param2 (default: 10)
    
    Returns:
        True if successful, False otherwise
    
    Raises:
        ValueError: If param1 is empty
    """
    if not param1:
        raise ValueError("param1 cannot be empty")
    return True
```

---

### General Best Practices

1. **Never commit secrets** - Use `.env` files, add to `.gitignore`
2. **Use `if __name__ == "__main__":`** for direct script execution
3. **Keep functions small** - One responsibility per function
4. **Use constants** - Magic numbers should be constants
5. **Log appropriately** - Use `print()` for simple scripts, `logging` for complex apps

```python
# ✅ Script entry point
def main():
    """Main function."""
    # Your code here
    pass

if __name__ == "__main__":
    main()
```

---

## File Organization

```
project/
├── .env                    # Environment variables (never commit!)
├── pyproject.toml          # Project config (optional)
├── .venv/                  # Virtual environment
├── py_discordBot/         # Main bot package
│   ├── __init__.py
│   ├── bot.py
│   └── discode_bot.py
├── class_discord/          # Tutorial materials
├── gui_lesson/             # GUI examples
└── tests/                 # Test files (when added)
```

---

## Common Patterns

### Loading Environment Variables
```python
from dotenv import load_dotenv
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(BASE_DIR, ".env")
load_dotenv(dotenv_path)

TOKEN = os.getenv("TOKEN")  # Returns None if not found
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))  # Cast to int
```

### Bot Template
```python
import discord
from dotenv import load_dotenv
import os

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

client.run(os.getenv("TOKEN"))
```

---

## Notes for Agents

- This is a **learning workspace**, not a production project
- No strict linting/formatting enforcement exists
- Prioritize **readability** and **learning value** over strict conventions
- When uncertain, ask user before making major changes
- Always check `.env` files exist before running bot code
