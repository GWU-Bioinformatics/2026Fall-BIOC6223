## Homework 4 — BioCompute Objects in Python
##
## This script should run directly as `python 04_homework.py`
## from the lecture-4 directory with the course environment active.
##
## Read through every block carefully. Some blocks work correctly.
## One block contains a bug. The questions will ask you to explain,
## trace, and fix what you find.

import json
import os

## BLOCK 1: Load the homework BCO ##
# This block is correct — run it to confirm the file loads without errors.

script_dir = os.path.dirname(os.path.abspath(__file__))
bco_path = os.path.join(script_dir, "04_homework_bco.json")

with open(bco_path, "r") as bco_file:
    bco = json.load(bco_file)

print(f"BCO loaded: {bco_path}")
print(f"Top-level keys: {list(bco.keys())}")

## END BLOCK 1 ##


## BLOCK 2: Provenance domain and contributors ##
# This block is correct.

prov = bco["provenance_domain"]

print(f"\n--- Provenance Domain ---")
print(f"  Name:    {prov['name']}")
print(f"  Version: {prov['version']}")
print(f"  License: {prov['license']}")

print(f"  Contributors ({len(prov['contributors'])}):")
for contributor in prov["contributors"]:
    contributions = ", ".join(contributor["contribution"])
    print(f"    {contributor['name']} <{contributor['email']}> — {contributions}")

## END BLOCK 2 ##


## BLOCK 3: Execution domain ##
# This block is correct. After reading it, answer Q5 by adding one line
# in the space marked below.

exec_d = bco["execution_domain"]

print(f"\n--- Execution Domain ---")
print(f"  Script driver: {exec_d['script_driver']}")
print(f"  Software prerequisites:")
for sw in exec_d["software_prerequisites"]:
    print(f"    {sw['name']} v{sw['version']}")

## ADD YOUR LINE HERE — print only the version string of the first software
## prerequisite (index 0). Use exec_d["software_prerequisites"] to access it.

## END BLOCK 3 ##


## BLOCK 4: Pipeline steps ##
# This block contains a bug. Running it will raise an error.
# Q4 asks you to identify the error, explain why it occurs,
# and show the corrected line.

desc = bco["description_domain"]

print(f"\n--- Pipeline Steps ---")
for step in desc["pipeline_steps"]:
    print(f"\n  Step {step['step_number']}: {step['name']}")
    print(f"    Inputs: {[i['filename'] for i in step['input']]}")   # <-- bug is here
    print(f"    Outputs: {[o['filename'] for o in step['output_list']]}")

## END BLOCK 4 ##
