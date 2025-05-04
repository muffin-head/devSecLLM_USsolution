import json

input_file = 'labels.jsonl'
output_file = 'policy_labels.jsonl'

# To track unique entries
unique_entries = {}
duplicate_count = 0

with open(input_file, 'r', encoding='utf-8') as infile:
    for line in infile:
        line = line.strip().rstrip(',')
        if line:  # ignore empty lines
            try:
                obj = json.loads(line)
                obj_str = json.dumps(obj, sort_keys=True)  # hashable representation
                if obj_str not in unique_entries:
                    unique_entries[obj_str] = obj
                else:
                    duplicate_count += 1
            except json.JSONDecodeError as e:
                print(f"Skipping invalid line: {line}\nError: {e}")

# Write only unique entries
with open(output_file, 'w', encoding='utf-8') as outfile:
    for item in unique_entries.values():
        json.dump(item, outfile, ensure_ascii=False)
        outfile.write('\n')

print(f"Cleaned data saved to: {output_file}")
print(f"Number of duplicate entries removed: {duplicate_count}")
