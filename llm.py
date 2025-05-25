from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

MODEL_NAME = "trillionlabs/Trillion-7B-preview"
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, torch_dtype=torch.bfloat16).to(device)

def is_tech_industry(text):
    prompt = f"""Rate this job category for relevancy to programming applicants:
Category: {text}
Relevant? (Yes/No):"""
    inputs = tokenizer(prompt, return_tensors="pt").to(device)
    output = model.generate(
        inputs.input_ids,
        max_new_tokens=2,
        do_sample=False,
        pad_token_id=tokenizer.eos_token_id,
        eos_token_id=tokenizer.eos_token_id,
        num_beams=2,
        early_stopping=True)
    response = tokenizer.decode(output[0], skip_special_tokens=True)
    return "Yes" if "Yes" in response.replace(prompt, "") else "No"

if __name__ == "__main__":
    test_industries = [
        ("Software engineering", "Yes"),
        ("Daycare", "No"), 
        ("Petroleum engineering", "Yes")
        ("Preschool teaching", "No")]

    print("Industry: Prediction (Expected)")
    for industry, expected in test_industries:
        prediction = is_tech_industry(industry)
        print(f"{industry}: {prediction} ({expected})")

