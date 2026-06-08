import os
import json

def calculate_ratios(female_count, male_count, both_count):
    total_count = female_count + male_count
    female_total = round((female_count / total_count) * 100, 3)
    male_total = round((male_count / total_count) * 100, 3)
    just_female = female_count - both_count
    just_male = male_count - both_count
    female_only = round((just_female / (just_female + just_male)) * 100, 3)
    male_only = round((just_male / (just_female + just_male)) * 100, 3)
    return {
        "female_total": female_total,
        "male_total": male_total,
        "female_only": female_only,
        "male_only": male_only
    }

def process_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        occupation = lines[0].strip().split('=')[1].strip()
        female_count = int(lines[1].strip().split('=')[1].strip())
        male_count = int(lines[2].strip().split('=')[1].strip())
        both_count = int(lines[3].strip().split('=')[1].strip())

        ratios = calculate_ratios(female_count, male_count, both_count)
        return occupation, ratios

def main(folder_path, output_file):
    data = {}
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            occupation, ratios = process_file(file_path)
            data[occupation] = ratios

    with open(output_file, 'w') as outfile:
        json.dump(data, outfile, indent=4)

if __name__ == "__main__":
    folder_path = "/path/to/filtered_corpus"
    output_file = "gender_occ_ratio.json"
    main(folder_path, output_file)
