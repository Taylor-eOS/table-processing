from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

MODEL_NAME = "trillionlabs/Trillion-7B-preview"
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, torch_dtype=torch.bfloat16).to(device)

def get_advice(text):
    prompt = f"Determine if the industry `{text}` is relevant for someone with skills in the area programming. Answer only with `Yes` or `No`."
    inputs = tokenizer(prompt, return_tensors="pt").to(device)
    
    output = model.generate(
        inputs.input_ids,
        max_new_tokens=4,
        temperature=0.01,
        pad_token_id=tokenizer.eos_token_id,
        eos_token_id=tokenizer.eos_token_id,
        do_sample=False)
    
    full_response = tokenizer.decode(output[0], skip_special_tokens=True)
    return full_response.replace(prompt, "").strip().split('\n')[0].split('.')[0]

if __name__ == "__main__":
    print(get_advice("Health care"))

