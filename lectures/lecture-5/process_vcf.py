## BLOCK 1 ##
import os

VCF_PATH = os.path.join(os.path.dirname(__file__), "synthetic_variants.vcf")

with open(VCF_PATH, "r") as fh:
    raw_lines = fh.readlines()
## END BLOCK 1 ##


## BLOCK 2 ##
# VCF files have three kinds of lines:
#   ##  meta-information headers (file format, filters, column definitions)
#   #CHROM  the single column-name header
#   data rows (one per variant)

meta_lines = []
column_header = None
data_lines = []

for line in raw_lines:
    line = line.rstrip("\n")
    if line.startswith("##"):
        meta_lines.append(line)
    elif line.startswith("#CHROM"):
        column_header = line
    else:
        if line:
            data_lines.append(line)

print(f"Meta-information lines : {len(meta_lines)}")
print(f"Data rows              : {len(data_lines)}")
## END BLOCK 2 ##


## BLOCK 3 ##
# The column-name header has a leading "#" that we strip before splitting
column_names = column_header.lstrip("#").split("\t")
print("VCF columns:", column_names)
## END BLOCK 3 ##


## BLOCK 4 ##
def parse_info(info_str):
    result = {}
    for field in info_str.split(";"):
        key, value = field.split("=")
        result[key] = value
    return result

def parse_variant(line, column_names):
    fields = line.split("\t")
    variant = dict(zip(column_names, fields))

    variant["QUAL"] = float(variant["QUAL"])
    variant["INFO"] = parse_info(variant["INFO"])

    # Split FORMAT keys and sample values together so they stay paired
    format_keys = variant["FORMAT"].split(":")
    sample_values = variant["SAMPLE01"].split(":")
    variant["SAMPLE01"] = dict(zip(format_keys, sample_values))

    return variant

# Parse all data rows
variants = [parse_variant(line, column_names) for line in data_lines]

# Inspect the first variant
print(variants[0])
## END BLOCK 4 ##


## BLOCK 5 ##
# Filter to PASS variants only
pass_variants = [v for v in variants if v["FILTER"] == "PASS"]
print(f"Total variants : {len(variants)}")
print(f"PASS variants  : {len(pass_variants)}")

for v in pass_variants:
    chrom = v["CHROM"]
    pos   = v["POS"]
    ref   = v["REF"]
    alt   = v["ALT"]
    qual  = v["QUAL"]
    gt    = v["SAMPLE01"]["GT"]
    print(f"  {chrom}:{pos}  {ref}>{alt}  QUAL={qual}  GT={gt}")
## END BLOCK 5 ##


## BLOCK 6 ##
# SNPs have equal-length REF and ALT; indels do not
def variant_type(ref, alt):
    if len(ref) == 1 and len(alt) == 1:
        return "SNP"
    elif len(ref) > len(alt):
        return "DEL"
    else:
        return "INS"

print("\nVariant type breakdown (PASS only):")
for v in pass_variants:
    vtype = variant_type(v["REF"], v["ALT"])
    print(f"  {v['POS']:>4}  {v['REF']:<4} > {v['ALT']:<4}  {vtype}")
## END BLOCK 6 ##
