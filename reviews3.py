from transformers import pipeline
import torch

model_id = "fine-tuned-model"
pipe = pipeline(
    "text-generation",
    model=model_id,
    device_map="auto",
)
messages = [
    {"role": "system", "content": """You are an advanced AI assistant created to perform sentiment analysis on reviews of college professors. I need you to analyze each review you receive and provide your analysis using the following csv format:
[teaching_sentiment, difficulty_sentiment]
teaching_sentiment = A floating-point representation of the sentiment of the review regarding the quality and effectiveness of teaching, rounded to two decimal places. Scale ranges from -1.0 (negative) to 1.0 (positive), where 0.0 represents neutral sentiment.
difficulty_sentiment = A floating-point representation of the sentiment of the review regarding how easy the class is, rounded to two decimal places. Scale ranges from -1.0 (difficult) to 1.0 (easy), where 0.0 represents neutral sentiment.
Always respond with the values for teaching_sentiment and difficulty_sentiment seperated by a comma. Do not include any other text or messages in your response.  Exclude markdown."""},
    {"role": "user", "content": "Dr. Jo Moma is a great professor! Very difficult exams and lots of homework, but doable if you study. Would reccomend!"},
]
outputs = pipe(
    messages,
    max_new_tokens=128,
    do_sample=True
)
print(outputs[0]["generated_text"][-1])
