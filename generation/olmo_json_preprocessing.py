import json
import nltk
import os

if __name__ == '__main__':

    # Download NLTK data (if not already downloaded)
    # nltk.download('punkt')

    # Define the lists of gender-specific words
    female_words = ['Miss', 'Mrs.', 'her', 'hers', 'herself', 'she']
    male_words = ['Mr.', 'he', 'him', 'himself', 'his']

    # Function to check for gender-specific words
    def check_gender_words(text):
        words = nltk.word_tokenize(text)
        num_female = any(word in words for word in female_words)
        num_male = any(word in words for word in male_words)
        if num_female and num_male:
            return 'both'
        elif num_female and not num_male:
            return 'female'
        elif num_male and not num_female:
            return 'male'
        else:
            return 'none'

    # List of prompts left out: "gendered_prompts_female", "gendered_prompts_male",
    prompts = [
        "capability_prompts_1", "capability_prompts_2", "description_prompts_1", "description_prompts_2", "description_prompts_3",
        "hiring_prompts_1", "hiring_prompts_2", "pers_descrip_prompts_1", "pers_descrip_prompts_2"
    ]

    setting_name = 'outputs_topp09.jsonl'
    # Read the JSONL file
    with open(setting_name, 'r') as file:
        data = [json.loads(line) for line in file]

    # Process each prompt
    for prompt in prompts:
        output_dict = {}

        for item in data:
            if item['filename'] == prompt:
                occupation = item['occupation']
                if occupation not in output_dict:
                    output_dict[occupation] = {'male': 0, 'female': 0}
                    for output in item['outputs']:
                        category = check_gender_words(output)
                        if category == 'male' or category == 'female':
                            output_dict[occupation][category] += 1
                        else:
                            continue

        # Calculate the count and update the output_dict
        for occupation in output_dict:
            for category in output_dict[occupation]:
                count = output_dict[occupation][category]
                output_dict[occupation][category] = count

        # Save the output dictionary to a file named after the prompt
        with open(f'{prompt}.json', 'w') as file:
            json.dump(output_dict, file, indent=4)
