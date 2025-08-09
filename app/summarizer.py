# from transformers import T5Tokenizer, T5ForConditionalGeneration
# import torch

# tokenizer = T5Tokenizer.from_pretrained("t5-small")
# model = T5ForConditionalGeneration.from_pretrained("t5-small")

# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# model = model.to(device)

# def summarize_text(text, max_input_length=512, max_output_length=150):
#     # Preprocess text
#     cleaned_text = "summarize: " + text.strip()

#     inputs = tokenizer.encode(cleaned_text, return_tensors="pt", max_length=max_input_length, truncation=True)
#     inputs = inputs.to(device)

#     summary_ids = model.generate(
#         inputs,
#         max_length=max_output_length,
#         num_beams=4,
#         early_stopping=True
#     )

#     output = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

#     # Add proper spacing
#     return ' '.join(output.split())

from transformers import T5Tokenizer, T5ForConditionalGeneration
import torch
from re import sub

# Load model + tokenizer
tokenizer = T5Tokenizer.from_pretrained("t5-small")
model = T5ForConditionalGeneration.from_pretrained("t5-small")
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)

def clean_text(text):
    return sub(r'\s+', ' ', text).strip()

def summarize_text(text):
    text = clean_text(text)
    input_text = "summarize: " + text
    inputs = tokenizer.encode(input_text, return_tensors="pt", max_length=512, truncation=True)
    inputs = inputs.to(device)
    summary_ids = model.generate(inputs, max_length=150, min_length=40, length_penalty=2.0, num_beams=4, early_stopping=True)
    return tokenizer.decode(summary_ids[0], skip_special_tokens=True)

# New function to simplify the medical summary
def simplify_summary(summary):
    prompt = f"Explain this medical summary to a patient in simple language with no medical knowledge: {summary}"
    
    inputs = tokenizer.encode(prompt, return_tensors="pt", max_length=512, truncation=True)
    inputs = inputs.to(device)
    
    output = model.generate(
        inputs,
        max_length=180,
        num_beams=4,
        early_stopping=True
    )

    return tokenizer.decode(output[0], skip_special_tokens=True)

