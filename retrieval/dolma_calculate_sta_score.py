import os
import numpy as np
import pandas as pd
import json

# Path to the Excel file containing gender percentage mapping
excel_file_path = "/path/to/gender_us_percentage_mapping.xlsx"

# Path to the directory containing the .txt files
directory_path = "/path/to/corpus"

# Read the real-life gender distribution data from the Excel file
real_life_data = pd.read_excel(excel_file_path)
occupation_data = real_life_data[['Occupation', 'Women', 'Men']]
# Convert occupation data to a dictionary for easy access
occupation_gender_distribution = occupation_data.set_index('Occupation').to_dict(orient='index')

if __name__ == '__main__':

    # Function to calculate Total Variation Distance (TVD)
    def tvd(P_obs, P_ref):
        return 0.5 * np.sum(np.abs(P_obs - P_ref))

    # Initialize a dictionary to store stereotypical associations for each occupation
    stereotypical_associations_dict = {}

    # Iterate through files in the directory
    for filename in os.listdir(directory_path):
        if filename.endswith("_stats.txt"):
            occupation = filename.split("_stats.txt")[0]

            file_path = os.path.join(directory_path, filename)

            # Read the file and extract counts
            with open(file_path, 'r') as file:
                lines = file.readlines()
                female_count = int(lines[1].split('=')[1].strip())
                male_count = int(lines[2].split('=')[1].strip())

                # Create co-occurrence vector C^t
                C_t = np.array([female_count, male_count])

                # Get real-life gender distribution data for the occupation
                occupation_gender_dist = occupation_gender_distribution.get(occupation.lower())

                if occupation_gender_dist:
                    # Extract women and men counts from real-life data
                    female_count = occupation_gender_dist['Women']
                    male_count = occupation_gender_dist['Men']

                    P_ref = np.array([female_count, male_count])

                    epsilon = 1e-5

                    # Create co-occurrence vector C^t
                    C_t = np.array([female_count, male_count])

                    # Calculate observed probability distribution P_obs^t
                    P_obs_t = (C_t + epsilon) / (np.sum(C_t) + 2 * epsilon)

                    # Calculate stereotypical association for this occupation
                    stereotypical_association_t = tvd(P_obs_t, P_ref)

                    # Store the result in the dictionary
                    stereotypical_associations_dict[occupation] = stereotypical_association_t

    # Calculate the overall stereotypical association
    overall_stereotypical_association = np.mean(list(stereotypical_associations_dict.values()))

    # Output the overall stereotypical association
    print(f"Overall Stereotypical Association: {overall_stereotypical_association}")

    # Save the stereotypical associations dictionary as a JSON file
    with open('stereotypical_associations_ref_real_world.json', 'w') as json_file:
        json.dump(stereotypical_associations_dict, json_file, indent=4)
