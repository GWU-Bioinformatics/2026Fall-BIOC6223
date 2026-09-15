## This script should run directly as `python 02_read_bco.py`
## from the lecture-4 directory with the course environment active.
##
## A BioCompute Object (BCO) is an IEEE 2791-2020 standard JSON document
## that captures the provenance, inputs, outputs, and execution details
## of a bioinformatics pipeline — making computational results reproducible
## and reviewable by regulators, collaborators, and journals.

import json
import os

## BLOCK 1: Locating the example BCO ##
# Using __file__ (the path to this script) lets the script find
# example_bco.json regardless of which directory you run it from.

script_dir = os.path.dirname(os.path.abspath(__file__))
bco_path = os.path.join(script_dir, "example_bco.json")

print(f"Loading BCO from: {bco_path}")

## END BLOCK 1 ##


## BLOCK 2: Reading the BCO ##
# json.load parses the file directly into nested Python dicts and lists.
# After this line, `bco` is a plain Python dict — no special BCO class needed.

with open(bco_path, "r") as bco_file:
    bco = json.load(bco_file)

print(f"\nTop-level keys in the BCO:")
for key in bco.keys():
    print(f"  {key}")

## END BLOCK 2 ##


## BLOCK 3: Accessing the provenance domain ##
# The provenance_domain records who created the BCO, when, and under
# what license.  It is a nested dict, so we access it with two key lookups.

prov = bco["provenance_domain"]

print(f"\n--- Provenance Domain ---")
print(f"  Name:     {prov['name']}")
print(f"  Version:  {prov['version']}")
print(f"  Created:  {prov['created']}")
print(f"  License:  {prov['license']}")

# Contributors is a list of dicts — one entry per contributor.
print(f"  Contributors ({len(prov['contributors'])}):")
for contributor in prov["contributors"]:
    contributions = ", ".join(contributor["contribution"])
    print(f"    {contributor['name']} <{contributor['email']}> — {contributions}")

## END BLOCK 3 ##


## BLOCK 4: Accessing the usability domain ##
# The usability_domain is a human-readable summary of what the BCO does.
# Per the IEEE 2791 standard, it should be an array of strings.

print(f"\n--- Usability Domain ---")
print(f"  Value:    {bco['usability_domain']}")
print(f"  Type:     {type(bco['usability_domain'])}")

## END BLOCK 4 ##


## BLOCK 5: Walking the pipeline steps ##
# The description_domain.pipeline_steps list describes each processing step.
# Each step records its inputs, outputs, software version, and description.

desc = bco["description_domain"]
print(f"\n--- Description Domain ---")
print(f"  Keywords: {', '.join(desc['keywords'])}")
print(f"  Pipeline steps ({len(desc['pipeline_steps'])}):")

for step in desc["pipeline_steps"]:
    print(f"\n  Step {step['step_number']}: {step['name']} (v{step['version']})")
    print(f"    {step['description']}")
    print(f"    Inputs:  {[i['filename'] for i in step['input_list']]}")
    print(f"    Outputs: {[o['filename'] for o in step['output_list']]}")

## END BLOCK 5 ##


## BLOCK 6: Inspecting the execution domain ##
# The execution_domain records the software stack, external databases,
# and environment variables required to reproduce the run.

exec_d = bco["execution_domain"]
print(f"\n--- Execution Domain ---")
print(f"  Script driver: {exec_d['script_driver']}")
print(f"  Software prerequisites:")
for sw in exec_d["software_prerequisites"]:
    print(f"    {sw['name']} v{sw['version']}")
print(f"  External data endpoints:")
for ep in exec_d["external_data_endpoints"]:
    print(f"    {ep['name']} — {ep['url']}")
print(f"  Environment variables: {exec_d['environment_variables']}")

## END BLOCK 6 ##


## BLOCK 7: Pretty-printing the full BCO ##
# json.dumps with indent=2 produces a human-readable representation
# of the entire nested structure — useful for inspection and debugging.

print(f"\n--- Full BCO (pretty-printed) ---")
print(json.dumps(bco, indent=2))

## END BLOCK 7 ##
