
from jsonschema import validate, ValidationError

def validate_json(response_json, expected_scheme):
    try:
        validate(instance=response_json, schema=expected_scheme)
        return True
    except ValidationError as e:
        print(f"Schema Validation Failed:\n{e.message}")
        return False
    
# ✅ This will return True or False after validating the structure.