## BLOCK 1 ##
import os

# Adjust this path appropriately if you would like to
# run the script locally
BIOC_DIR = "~/gwu-src/courses/2026Spring-BIOC-6225/lecture-3/"
SAMPLE_NAME = "sythetic_genome_small_example.vcf"
full_sample_path = os.path.join(os.path.expanduser(BIOC_DIR), SAMPLE_NAME)
## END BLOCK 1 ##

## BLOCK 2 ##
with open(full_sample_path, "r") as sample_pointer:
    small_genome_data = sample_pointer.readlines()
## BLOCK 2 ##

## BLOCK 3 ##
def process_genome_line(line):
    values = line.split(",")
    # Strip the trailing newline ("\n") from the last member of the list
    values[-1] = values[-1].rstrip("\n")
    if values[0] == "rsid":
        # We don't want the headers in the data
        # so return a None as signal that no processing
        # occurred
        return None
    if len(values) != 3:
        # Empty lines are legal in this example file
        return None
    return_item = {
        "rsid": values[0],
        "gene_name": values[1],
        # Python allows "casting" (or for Boolean, "truthiness-ing")
        # of variables into boolean. e.g., 0 -> False, 1 -> True
        # Python also reads all values from a file as strings
        # So, first cast the string into an integer
        "present": bool(int(values[2])),
    }
    return return_item
## END BLOCK 3 ##

## BLOCK 4 ##
class VariantParser:

    # NB that Python allows "type hinting": the
    # genome_data list type is not enforced, 
    # but is useful to a person reading the script
    def __init__(self, genome_data: list):
        self.raw_data = genome_data
    
    def parse_and_report_information(self):
        snp_presence = {"present": {}, "not present": {}}
        for line in self.raw_data:
            line_info = process_genome_line(line)
            if line_info is None:
                continue
            if line_info["present"]:
                snp_presence["present"][line_info["rsid"]] = line_info["gene_name"]
            else:
                snp_presence["not present"][line_info["rsid"]] = line_info["gene_name"]
        for output_type in ["present", "not present"]:
            # Python allows for some formatting of strings within the print function call 
            print("*"*20+f"{'SNP is ' + output_type:^40}"+"*"*20)
            print(snp_presence[output_type])
            print("*"*80)

parser = VariantParser(small_genome_data)
parser.parse_and_report_information()
## BLOCK 4 ##
