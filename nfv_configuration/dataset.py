import json, os
from datasets import load_dataset, Dataset
from sklearn.model_selection import train_test_split

# convert datset to the format of {"instruction": "intent", "output": "output"}
def normalize_dataset(ds):
    ds_norm = []
    for x in ds:
        for intent in x["intents"][:1]:
            ds_norm.append({
                "instruction": intent,
                "output": json.dumps(x["output"])
            })
    return Dataset.from_list(ds_norm)

file_dir = os.path.dirname(__file__)
dataset_file_path = os.path.join(file_dir, "dataset.json")
examples_file_path = os.path.join(file_dir, "examples.json")
with open(dataset_file_path) as dataset_file:
    nfv_conf_ds = json.load(dataset_file)
with open(examples_file_path) as examples_file:
    examples = json.load(examples_file)

# trainset, testset = train_test_split(nfv_conf_ds, test_size=0.5, random_state=42)


trainset = normalize_dataset(examples)
testset = normalize_dataset(nfv_conf_ds)
