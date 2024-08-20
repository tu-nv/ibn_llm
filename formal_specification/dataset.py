from datasets import load_dataset

# convert dataset to format that can be used by langchain
def convert_dataset(x):
    return {"instruction": x["human_language"], "output": x["expected"]}

netconfeval_ds = load_dataset("NetConfEval/NetConfEval", "Formal Specification Translation")
netconfeval_ds = netconfeval_ds['train'].filter(lambda x: x["batch_size"] <= 10).map(convert_dataset).train_test_split(test_size=0.5, seed=42)
trainset = netconfeval_ds['train']
testset = netconfeval_ds['test']
