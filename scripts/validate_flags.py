import json
import os
import sys
from jsonschema import validate, ValidationError

# JSON Schema for feature flags
SCHEMA = {
    "type": "object",
    "patternProperties": {
        "^[a-zA-Z0-9_\\-]+$": {
            "type": "object",
            "properties": {
                "enabled": { "type": "boolean" },
                "description": { "type": "string" }
            },
            "required": ["enabled"],
            "additionalProperties": False
        }
    },
    "additionalProperties": False
}

def validate_file(path):
    try:
        with open(path, "r") as f:
            data = json.load(f)
            validate(instance=data, schema=SCHEMA)
        print(f"✅ Valid: {path}")
        return True
    except (json.JSONDecodeError, ValidationError) as e:
        print(f"❌ Invalid: {path}\n   ↳ {e}")
        return False

def main():
    success = True
    for root, _, files in os.walk("flags"):
        for file in files:
            if file.endswith(".json"):
                full_path = os.path.join(root, file)
                if not validate_file(full_path):
                    success = False
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
