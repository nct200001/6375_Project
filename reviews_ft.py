from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments
import torch
from datasets import load_dataset

model_id = "meta-llama/Llama-3.2-1B-Instruct"
model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=torch.float32, device_map="auto")
tokenizer = AutoTokenizer.from_pretrained(model_id)
tokenizer.pad_token = tokenizer.eos_token

dataset = load_dataset("csv", data_files="processed_reviews_2.csv", delimiter='|', split="train")
print(dataset[0])

def apply_chat_template(example):
    messages = [
        {"role": "system", "content": """You are an advanced AI assistant created to perform sentiment analysis on reviews of college professors. I need you to analyze each review you receive and provide your analysis using the following csv format:
[teaching_sentiment, difficulty_sentiment]
teaching_sentiment = A floating-point representation of the sentiment of the review regarding the quality and effectiveness of teaching, rounded to two decimal places. Scale ranges from -1.0 (negative) to 1.0 (positive), where 0.0 represents neutral sentiment.
difficulty_sentiment = A floating-point representation of the sentiment of the review regarding how easy the class is, rounded to two decimal places. Scale ranges from -1.0 (difficult) to 1.0 (easy), where 0.0 represents neutral sentiment.
Always respond with the values for teaching_sentiment and difficulty_sentiment seperated by a comma. Do not include any other text or messages in your response.  Exclude markdown."""},
        {"role": "user", "content": example['question']},
        {"role": "assistant", "content": example['answer']}
    ]
    prompt = tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )
    return {"prompt": prompt}

new_dataset = dataset.map(apply_chat_template)
new_dataset = new_dataset.train_test_split(0.05) # save 5% for testing

def tokenize_function(example):
    tokens = tokenizer(example['prompt'], padding="max_length", truncation=True, max_length=128)
    tokens['labels'] = [
        -100 if token == tokenizer.pad_token_id else token for token in tokens['input_ids']
    ]
    return tokens

tokenized_dataset = new_dataset.map(tokenize_function)
tokenized_dataset = tokenized_dataset.remove_columns(['question', 'answer', 'prompt'])

model.train()
training_args = TrainingArguments(
    output_dir="./results",
    eval_strategy="steps",
    eval_steps=40,
    logging_steps=40,
    save_strategy="epoch",
    per_device_train_batch_size=2,
    per_device_eval_batch_size=2,
    num_train_epochs=5,
    fp16=False,
    report_to="none",
    log_level="info",
    learning_rate=1e-5,
    max_grad_norm=2
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset["train"],
    eval_dataset=tokenized_dataset["test"],
    tokenizer=tokenizer)

trainer.train()

trainer.save_model("./fine-tuned-model")
tokenizer.save_pretrained("./fine-tuned-model")
