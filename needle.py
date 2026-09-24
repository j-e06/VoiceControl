import needle

from pathlib import Path

import subprocess

notes_path = Path("needle-notes.txt")

@needle.tool
def save_note(text: str):
	with notes_path.open("a", encoding="utf-8") as notes:
		notes.write(text + "\n")
	return {"text": text, "path": str(notes_path)}

@needle.tool

