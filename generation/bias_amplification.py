import os
import json
import numpy as np
import matplotlib.pyplot as plt

# Define folders and prompts
prompts = [
    "capability_1", "capability_2", "capability_merged", "descrip_1", "descrip_2", "description_merged",
    "hiring_1", "hiring_2", "hiring_merged", "merged", "neutral_1", "neutral_2", "neutral_3", "neutral_merged"
]

folders = ["base_outputs_no_sett", "base_outputs_temp07", "base_outputs_topk40", "base_outputs_topp09"]

# Load the pretraining data
pretraining_data_path = "/path/to/percentages_data.json"
with open(pretraining_data_path, 'r') as file:
    pretraining_data = json.load(file)

# Function to read the sector mapping from the text file
sector_mapping_file = '/path/to/sector_mapping.txt'

def read_sector_mapping(file_path):
    occupations = {}
    with open(file_path, 'r') as file:
        for line in file:
            occupation, sector = line.strip().split(' = ')
            occupations[occupation] = sector
    return occupations

occupations_to_sector = read_sector_mapping(sector_mapping_file)

# Function to calculate amplification for specified occupations
def calculate_amplification(generation_data, training_data):
    amplification = {}
    for occupation, data in generation_data.items():
        if occupation in training_data:
            gen_female_percentage = data.get("female", 0)
            train_female_percentage = training_data[occupation].get("women", 0)
            amplification[occupation] = gen_female_percentage - train_female_percentage
    return amplification

# Function to plot and save bar charts with differentiation for amplification and de-amplification
def plot_amplification_by_sector(amplification_data, output_path):
    sector_amplification = {}

    # Aggregate amplification by sectors
    for occupation, amplification in amplification_data.items():
        sector = occupations_to_sector.get(occupation)
        if sector:
            if sector not in sector_amplification:
                sector_amplification[sector] = []
            sector_amplification[sector].append(amplification)

    # Calculate average amplification per sector
    avg_sector_amplification = {sector: np.mean(values) for sector, values in sector_amplification.items()}

    # Split positive and negative amplifications for different colors
    sectors = list(avg_sector_amplification.keys())
    avg_amplifications = list(avg_sector_amplification.values())
    colors = ['orange' if x >= 0 else 'blue' for x in avg_amplifications]

    plt.figure(figsize=(10, 6))
    bars = plt.barh(sectors, avg_amplifications, color=colors)

    # Add labels for positive and negative bars
    for bar, amplification in zip(bars, avg_amplifications):
        plt.text(bar.get_width() if amplification < 0 else bar.get_width(),
                 bar.get_y() + bar.get_height() / 2,
                 f'{amplification:.2f}',
                 va='center', ha='right' if amplification < 0 else 'left',
                 color='black')

    plt.xlabel('Average Amplification')
    plt.ylabel('Sector')
    plt.title('Average Amplification by Sector')
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

# Iterate through each folder and prompt
for folder in folders:
    amplification_folder = os.path.join(folder, "amplification")
    os.makedirs(amplification_folder, exist_ok=True)

    amplification_results = {}
    for prompt in prompts:
        prompt_file = os.path.join(folder, "percentage", f"percentage_{prompt}.json")
        if not os.path.isfile(prompt_file):
            continue

        with open(prompt_file, 'r') as file:
            generation_data = json.load(file)

        amplification = calculate_amplification(generation_data, pretraining_data)

        # Save individual amplification file
        amplification_file_path = os.path.join(amplification_folder, f"{prompt}_amplification.json")
        with open(amplification_file_path, 'w') as file:
            json.dump(amplification, file, indent=4)

        # Calculate and store average amplification
        avg_amplification = np.mean(list(amplification.values())) if amplification else 0
        amplification_results[prompt] = avg_amplification

        # Plot and save amplification by sector
        plot_output_path = os.path.join(amplification_folder, f"{prompt}_amplification_by_sector.png")
        plot_amplification_by_sector(amplification, plot_output_path)

    # Save average amplification results
    avg_amplification_file = os.path.join(amplification_folder, "average_amplification.txt")
    with open(avg_amplification_file, 'w') as file:
        for prompt, avg_amp in amplification_results.items():
            file.write(f"{prompt}: {avg_amp}\n")
