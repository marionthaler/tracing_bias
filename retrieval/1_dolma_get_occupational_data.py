from collections import defaultdict
from typing import Any, Dict, Generator, Iterable, List, Optional, Union

import matplotlib.pyplot as plt
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError
import json

import sys
import argparse
import os

# Parse arguments for a profession name
parser = argparse.ArgumentParser(description='Get documents for a profession')
parser.add_argument('--profession', type=str, help='Profession name')
args = parser.parse_args()
profession = args.profession
print("Profession:", profession)

target_file = f"/path/to/target/directory/{profession}.json"

if os.path.exists(target_file):
    print("File already exists. Exiting.")
    sys.exit(0)

sys.path.append('/path/to/custom/modules')

from custom_module import es_init, get_indices

es = es_init(config="/path/to/config/es_config.yml", timeout=60)

from custom_module import count_documents_containing_phrases, get_documents_containing_phrases
from tqdm import tqdm

index_name = "index_name_v1.5_2023-11-02"
it = get_documents_containing_phrases(index_name, [profession], all_phrases=True, return_all_hits=True, sort_field="document_id")
limit = 100_000

docs = []
for el in tqdm(it):
    docs.append(el)
    if len(docs) > limit:
        break

with open(target_file, "w") as f:
    json.dump(docs, f, indent=2)
