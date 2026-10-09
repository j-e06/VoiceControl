import json
from pathlib import Path

import needle
from jsonschema import validate, ValidationError, Draft202012Validator
from tools.testing_tools import blink_led


class ToolExecutor:
    def __init__(self):
        self.BASE_DIR = Path(__file__).resolve().parent
        with open(self.BASE_DIR / "tools.json", encoding="utf-8") as f:
            tool_schemas = json.load(f)
        print("Loaded schemas:", json.dumps(tool_schemas, indent=2))
        for tool in tool_schemas:
            Draft202012Validator.check_schema(tool["parameters"])
        self.SCHEMAS = {tool["name"]: tool for tool in tool_schemas}
        # tool names to function mapping
        self.TOOL_HANDLERS = {
            "blink_led": blink_led
        }

        # make sure tools match, both in .json & .py
        if set(self.SCHEMAS) != set(self.TOOL_HANDLERS):
            raise ValueError("tools.json and handlers do not match")

        self.agent = needle.Needle(tools=tool_schemas)

    def run_command(self,command: str):
        # we don't need history for each commands rn, they're seperated
        self.agent.reset()

        response = self.agent.complete(command)

        calls = response.get("function_calls", [])
        confidence = response.get("confidence")

        print("Confidence:", confidence)
        print("Tool calls:", calls)

        if not calls:
            print("No matching tool found.")
            return []

        # confidence threshold, not smart to go lower tbh
        if confidence is not None and confidence < 0.7:
            print("Uncertain tool call; not executing.")
            return []

        results = []

        for call in calls:
            name = call["name"]
            arguments = call["arguments"]

            handler = self.TOOL_HANDLERS.get(name)
            schema = self.SCHEMAS.get(name)

            if handler is None or schema is None:
                print("Unknown tool:", name)
                continue

            # validate then exec
            parameters = {
                **schema["parameters"],
                "additionalProperties": False
            }

            try:
                validate(arguments, parameters)
                output = handler(**arguments)

                results.append({
                    "tool": name,
                    "result": output
                })

            except (ValidationError, TypeError, ValueError) as e:
                print(f"Invalid arguments for {name}: {e}")

            except Exception as e:
                print(f"Tool {name} failed: {e}")

        return results