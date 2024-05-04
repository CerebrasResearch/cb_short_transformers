from short_transformers import ShortTransformer
from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForCausalLM

# load from path/hf_hub
model_name = "meta-llama/Meta-Llama-3-8B"

model = ShortTransformer.from_pretrained(model_name, device_map="auto")
tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token

# or use hf model
# model = ShortTransformer.from_model(hf_model)

dataset = load_dataset(
    "iNeil77/pseudo-mini-pile", "c4_realnews", split="train", streaming=True
)

# remove n layers, use hf dataset to find the optimal cut
short_model = model.remove_layers(
    n=5, dataset=dataset, tokenizer=tokenizer, key="content"
)  # (n, dataset, key, limit, batch_size, return_outputs, distance)

# save as hf model
output_path = "short_model"
short_model.save_pretrained(output_path) 

# load again the model using transformers
model = AutoModelForCausalLM.from_pretrained(output_path)