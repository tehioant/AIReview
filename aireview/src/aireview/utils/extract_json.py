
import json
import logging
import re
from typing import List

logger = logging.getLogger(__name__)

def extract_json(text: str) -> List[dict]:
    try:
        # Modify the regex pattern to support multi-line JSON objects and arrays of objects
        json_pattern = r'\{(?:[^{}]|(?:\{[^{}]*\}))*\}|\[(?:[^\[\]]|(?:\[.*?\]))*?\]'
        matches = re.findall(json_pattern, text, re.DOTALL)
        if not matches:
            logger.error("No JSON found in text")

        # Load and flatten JSON objects and lists of objects into a list of dictionaries
        json_objects = []
        for match in matches:
            try:
                obj = json.loads(match)
                if isinstance(obj, dict):
                    json_objects.append(obj)
                elif isinstance(obj, list):
                    # Assume the list contains dictionaries and extend the result
                    json_objects.extend(item for item in obj if isinstance(item, dict))
            except json.JSONDecodeError:
                # Continue on JSON decode error, as some matches might not be complete JSON
                pass

        if not json_objects:
            logger.error("Invalid JSON formats found in text")

        return json_objects
    except Exception as e:
        logger.error(f"Error processing text: {e}")

# Example usage
# response_text = 'Your input JSON or text containing JSON'
# print(extract_json(response_text))