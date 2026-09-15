## This script should run directly as `python 01_json_basics.py`
## from the lecture-4 directory with the course environment active.

## BLOCK 1: The json module ##
# Python's standard library includes the `json` module for working with
# JSON (JavaScript Object Notation), a widely used data interchange format.
# JSON maps directly onto Python's two most important collection types:
#   JSON object  →  Python dict
#   JSON array   →  Python list

import json

## END BLOCK 1 ##


## BLOCK 2: Building a dict (JSON object) ##
# A dict maps string keys to values of any type.
# JSON objects follow the same rule.

sequencing_run = {
    "run_id": "SRR_DEMO_001",
    "instrument": "Illumina NovaSeq 6000",
    "paired_end": True,
    "read_length": 150,
    "coverage_depth": 30.7,
}

print("Sequencing run dict:")
print(sequencing_run)
print(f"  instrument: {sequencing_run['instrument']}")
print(f"  read_length type: {type(sequencing_run['read_length'])}")

## END BLOCK 2 ##


## BLOCK 3: Building a list (JSON array) ##
# A list holds ordered, heterogeneous values — anything from strings
# to nested dicts. In JSON this becomes an array.

samples = [
    {"sample_id": "S001", "organism": "Homo sapiens",  "tissue": "liver"},
    {"sample_id": "S002", "organism": "Homo sapiens",  "tissue": "kidney"},
    {"sample_id": "S003", "organism": "Mus musculus",  "tissue": "brain"},
]

print(f"\nSample list has {len(samples)} entries.")
for sample in samples:
    print(f"  {sample['sample_id']}: {sample['organism']} ({sample['tissue']})")

## END BLOCK 3 ##


## BLOCK 4: Combining into a nested structure ##
# JSON documents are almost always nested — a top-level object whose
# values are other objects or arrays. Python dicts and lists nest freely.

experiment = {
    "experiment_id": "EXP_2026_001",
    "sequencing_run": sequencing_run,   # dict inside a dict
    "samples": samples,                 # list inside a dict
    "notes": "Pilot cohort for GWU BIOC6223 demo",
}

print(f"\nExperiment top-level keys: {list(experiment.keys())}")
print(f"Samples nested inside experiment: {len(experiment['samples'])}")

## END BLOCK 4 ##


## BLOCK 5: Serializing to a JSON string with json.dumps ##
# json.dumps ("dump to string") converts a Python object to a JSON string.
# The `indent` parameter controls pretty-printing; without it the output
# is a single compact line.

json_string = json.dumps(experiment, indent=4)

print("\nJSON string (first 300 chars):")
print(json_string[:300])

## END BLOCK 5 ##


## BLOCK 6: Deserializing from a JSON string with json.loads ##
# json.loads ("load from string") is the inverse: parses a JSON string
# back into Python objects.  Round-tripping should give us the same data.

recovered = json.loads(json_string)

print(f"\nRound-trip check — run_id: {recovered['sequencing_run']['run_id']}")
print(f"  paired_end type after round-trip: {type(recovered['sequencing_run']['paired_end'])}")
# Note that Python True/False serialize as JSON true/false and come back intact.

## END BLOCK 6 ##


## BLOCK 7: Writing to a file with json.dump and reading back with json.load ##
# json.dump writes directly to a file object — no intermediate string needed.
# json.load reads from a file object.

output_path = "experiment_output.json"

with open(output_path, "w") as out_file:
    json.dump(experiment, out_file, indent=4)

print(f"\nWrote experiment to {output_path}")

with open(output_path, "r") as in_file:
    loaded_experiment = json.load(in_file)

print(f"Read back experiment_id: {loaded_experiment['experiment_id']}")
print(f"First sample organism: {loaded_experiment['samples'][0]['organism']}")

import os
os.unlink(output_path)
print(f"Cleaned up {output_path}")

## END BLOCK 7 ##
