## This script should run directly as `python 03_validate_bco.py`
## from the lecture-4 directory with the course environment active.
##
## JSON Schema is a standard for describing the expected structure of a JSON
## document — what keys are required, what types values must have, and so on.
## The `jsonschema` library validates a Python dict against a schema and
## raises a detailed exception when something does not match.

import json
import os
import jsonschema
from jsonschema import validate, ValidationError

## BLOCK 1: Load the BCO ##

script_dir = os.path.dirname(os.path.abspath(__file__))
bco_path = os.path.join(script_dir, "example_bco.json")

with open(bco_path, "r") as bco_file:
    bco = json.load(bco_file)

print("BCO loaded successfully.")

## END BLOCK 1 ##


## BLOCK 2: Define a JSON Schema for the BCO ##
# A JSON Schema is itself a dict with a specific vocabulary.
# "type" constrains the data type, "required" lists mandatory keys,
# and "properties" describes each field's own schema.
#
# This schema covers the top-level BCO structure plus a detailed
# check on the fields most commonly mis-formed in practice.

BCO_SCHEMA = {
    "type": "object",
    "required": [
        "object_id",
        "spec_version",
        "etag",
        "provenance_domain",
        "usability_domain",
        "description_domain",
        "execution_domain",
        "io_domain",
    ],
    "properties": {
        "object_id":    {"type": "string"},
        "spec_version": {"type": "string"},
        "etag":         {"type": "string"},

        # usability_domain MUST be an array of strings (IEEE 2791-2020 §2.1.3).
        # A single descriptive string is a very common mistake.
        "usability_domain": {
            "type": "array",
            "items": {"type": "string"},
            "minItems": 1,
        },

        "provenance_domain": {
            "type": "object",
            "required": ["name", "version", "created", "modified", "contributors", "license"],
            "properties": {
                "name":     {"type": "string"},
                "version":  {"type": "string"},
                "created":  {"type": "string"},
                "modified": {"type": "string"},
                "license":  {"type": "string"},
                "contributors": {
                    "type": "array",
                    "minItems": 1,
                    "items": {
                        "type": "object",
                        "required": ["contribution", "name"],
                        "properties": {
                            "contribution": {"type": "array", "items": {"type": "string"}},
                            "name":         {"type": "string"},
                        },
                    },
                },
            },
        },

        "description_domain": {
            "type": "object",
            "required": ["keywords", "pipeline_steps"],
            "properties": {
                "keywords":      {"type": "array", "items": {"type": "string"}},
                "pipeline_steps": {"type": "array", "minItems": 1},
            },
        },

        "execution_domain": {
            "type": "object",
            "required": ["script", "script_driver", "software_prerequisites",
                         "external_data_endpoints", "environment_variables"],
        },

        "io_domain": {
            "type": "object",
            "required": ["input_subdomain", "output_subdomain"],
        },
    },
}

print("Schema defined.")

## END BLOCK 2 ##


## BLOCK 3: First validation attempt — expect a failure ##
# validate() raises jsonschema.ValidationError on the first problem it finds.
# We catch that exception, read its message, and inspect which field failed.

print("\n--- Validation attempt 1 ---")

try:
    validate(instance=bco, schema=BCO_SCHEMA)
    print("Validation passed! (unexpected)")

except ValidationError as error:
    print(f"Validation FAILED.")
    print(f"  Error message : {error.message}")
    # error.path is a deque showing which key(s) led to the bad value.
    # Joining it gives us a dotted path like "usability_domain".
    field_path = " → ".join(str(part) for part in error.absolute_path)
    print(f"  Field path    : {field_path if field_path else '(top level)'}")
    print(f"  Bad value     : {repr(bco.get('usability_domain'))}")
    print(f"  Expected type : array")

## END BLOCK 3 ##


## BLOCK 4: Diagnose the problem ##
# The IEEE 2791-2020 standard requires usability_domain to be an array of
# strings — a list in Python — so that multiple descriptive sentences can
# be stored independently.  Our example BCO has it as a plain string.

print("\n--- Diagnosis ---")
ud = bco["usability_domain"]
print(f"  Current type  : {type(ud).__name__}")
print(f"  Current value : {repr(ud)}")
print("  Fix: wrap the string in a list so it becomes a one-element array.")

## END BLOCK 4 ##


## BLOCK 5: Fix the data and re-validate ##
# We wrap the existing string in square brackets to make it a list.
# This is the minimal, non-destructive correction — no information is lost.

if isinstance(bco["usability_domain"], str):
    bco["usability_domain"] = [bco["usability_domain"]]

print(f"\n  Fixed type    : {type(bco['usability_domain']).__name__}")
print(f"  Fixed value   : {bco['usability_domain']}")

## END BLOCK 5 ##


## BLOCK 6: Second validation attempt — expect success ##

print("\n--- Validation attempt 2 ---")

try:
    validate(instance=bco, schema=BCO_SCHEMA)
    print("Validation PASSED. The BCO is now schema-compliant.")

except ValidationError as error:
    print(f"Validation still failing: {error.message}")

## END BLOCK 6 ##


## BLOCK 7: Write the corrected BCO back to disk ##
# Once validated, we save the corrected version alongside the original.
# In practice you would overwrite the original or version-control the fix.

corrected_path = os.path.join(script_dir, "example_bco_corrected.json")

with open(corrected_path, "w") as out_file:
    json.dump(bco, out_file, indent=4)

print(f"\nCorrected BCO written to: {corrected_path}")

## END BLOCK 7 ##
