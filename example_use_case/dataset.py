
from datasets import Dataset

# make trainset and testset as list of {"instruction": "my_intent", "output": "my_output"}
trainset = Dataset.from_list([{"instruction": "my_intent", "output": "my_output"}])
testset = Dataset.from_list([{"instruction": "my_intent", "output": "my_output"}])
