import os
import json
import multiprocessing as mp
from nltk.tokenize import sent_tokenize, word_tokenize
from tqdm import tqdm
import stanza

# Download Stanza resources for the English language
stanza.download('en')

# Initialize Stanza pipeline with coreference resolution
nlp = stanza.Pipeline(lang='en', processors='tokenize,ner,pos,lemma,depparse,coref')


# Tokenization function
def tokenize_document(doc: str) -> list:
    return sent_tokenize(doc)


def tokenize_documents(corpus: list) -> list[list[str]]:
    with mp.Pool() as pool:
        tokenized_corpus = list(tqdm(pool.imap(tokenize_document, corpus), total=len(corpus)))
    return tokenized_corpus


def batch_process_coref(sentences, batch_size=5):
    batches = [sentences[i:i + batch_size] for i in range(0, len(sentences), batch_size)]
    processed_sentences = []

    for batch in tqdm(batches, desc="Processing Batches"):
        docs = nlp(batch)
        processed_sentences.extend(docs.sentences)

    return processed_sentences


def process_file(filepath: str, occupation: str, female_terms, male_terms, batch_size=5) -> tuple:
    female_counter = 0
    male_counter = 0
    both_counter = 0
    documents = []

    with open(filepath, 'r') as file:
        data = json.load(file)
        corpus = [(doc["_source"]["text"], doc["_index"]) for doc in data if
                  "text" in doc["_source"] and "_index" in doc]

        # Tokenize documents
        tokenized_corpus = tokenize_documents([doc[0] for doc in corpus])

        for i, (text, index) in enumerate(corpus):
            sentences_list = tokenized_corpus[i]
            relevant_sentences = []

            # Process sentences in batches for coreference resolution
            processed_sentences = batch_process_coref(sentences_list, batch_size=batch_size)

            for sentence_obj in processed_sentences:
                sentence = sentence_obj.text
                if occupation.lower() in sentence.lower():
                    sentence_tok = [word.lower() for word in word_tokenize(sentence)]
                    has_female = any(word in female_terms for word in sentence_tok)
                    has_male = any(word in male_terms for word in sentence_tok)

                    if has_female or has_male:
                        coref_chains = sentence_obj.coref_chains

                        occupation_mentioned = False
                        for chain in coref_chains:
                            for mention in chain:
                                if occupation.lower() in mention.text.lower():
                                    occupation_mentioned = True
                                    break
                            if occupation_mentioned:
                                break

                        if occupation_mentioned:
                            relevant_sentences.append(sentence)
                            if has_female and has_male:
                                both_counter += 1
                            elif has_female:
                                female_counter += 1
                            elif has_male:
                                male_counter += 1

            if relevant_sentences:
                documents.append({"_index": index, "sentences": relevant_sentences})

    return female_counter, male_counter, both_counter, documents


if __name__ == '__main__':
    input_directory = "/path/to/input_directory"
    output_directory = "/path/to/output_directory"

    female_terms = ['miss', 'mrs.', 'aunt', 'daughter', 'female', 'girl', 'granddaughter', 'grandmother', 'her', 'hers',
                    'herself', 'mother', 'niece', 'she', 'sister', 'wife', 'woman']
    male_terms = ['mr.', 'boy', 'brother', 'father', 'grandfather', 'grandson', 'he', 'him', 'himself', 'his',
                  'husband', 'male', 'man', 'nephew', 'son', 'uncle']

    for filename in tqdm(os.listdir(input_directory)):
        if filename.endswith(".json"):
            filepath = os.path.join(input_directory, filename)
            occupation = filename[:-5]

            female_counter, male_counter, both_counter, documents = process_file(filepath, occupation, female_terms,
                                                                                 male_terms, batch_size=5)

            # Save sentences to a JSON file
            sentences_filepath = os.path.join(output_directory, f"{occupation}_sentences.json")
            with open(sentences_filepath, 'w') as sentences_file:
                json.dump(documents, sentences_file, indent=4)

            # Write counters and sentence count to a text file
            output_filename = os.path.join(output_directory, f"{occupation}_stats.txt")
            with open(output_filename, 'w') as output_file:
                output_file.write(f"occupation = {occupation}\n")
                output_file.write(f"female_count = {female_counter}\n")
                output_file.write(f"male_count = {male_counter}\n")
                output_file.write(f"both_count = {both_counter}\n")
                output_file.write("\n")
