from transformers import pipeline

generator = pipeline("text-generation", model="gpt2")


# Your prompt
prompt = "Explain step by step how to use GPT-3.5 in Python."

# Generate text
result = generator(
    prompt,
    max_length=400,     # longer output
    truncation=True,    # avoid warnings
    do_sample=True,     # makes output less repetitive
    temperature=0.7,    # creative but coherent
    top_k=50,
    top_p=0.95
)
 # adjust max_length if you want longer answers

# Print output
print(result[0]["generated_text"])
