import os
from vllm import LLM, SamplingParams
import json
import random

llm = LLM(model="allenai/OLMo-7B-hf",
          download_dir="/path/to/cache",
          tensor_parallel_size=4,
          gpu_memory_utilization=0.85,
          trust_remote_code=True)

prompts = []
for file in os.listdir("/path/to/base_prompts"):
    with open(f"/path/to/base_prompts/{file}", "r") as f:
        raw_prompts = f.read().splitlines()
    for p in raw_prompts:
        founded_occs = []
        for occ in occs:
            if occ in p:
                founded_occs.append(occ)
        if len(founded_occs) != 1:
            founded_occ = founded_occs[0]
            for occ in founded_occs:
                if len(occ) > len(founded_occ):
                    founded_occ = occ
        else:
            founded_occ = founded_occs[0]
        prompts.append({"filename": file.split(".")[0], "prompt": p, "occupation": founded_occ, "outputs": []})

tokenizer = llm.get_tokenizer()

conversations = []
for p in prompts:
    conversations.append(p["prompt"])

def generate(temperature=1.0, top_p=1.0, top_k=-1):
    sampling_params = SamplingParams(temperature=temperature, max_tokens=512, top_p=top_p, top_k=top_k, n=50)
    llm_output = llm.generate(conversations, sampling_params)
    prompts_temp = prompts.copy()
    for idx, outputs in enumerate(llm_output):
        prompts_temp[idx]["output"] = [o.text for o in outputs.outputs]
    return prompts_temp

generated_outputs = generate(temperature=0.7)

with open("/path/to/output/base_outputs_temp07.json", "w") as f:
    json.dump(generated_outputs, f)

generated_outputs = generate(temperature=1.0, top_p=0.9)

with open("/path/to/output/base_outputs_topp09.json", "w") as f:
    json.dump(generated_outputs, f)

generated_outputs = generate(temperature=1.0, top_p=1.0, top_k=40)

with open("/path/to/output/base_outputs_topk40.json", "w") as f:
    json.dump(generated_outputs, f)

generated_outputs = generate(temperature=1.0, top_p=1.0, top_k=-1)

with open("/path/to/output/base_outputs_no_sett.json", "w") as f:
    json.dump(generated_outputs, f)
