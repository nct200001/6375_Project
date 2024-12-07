from transformers import pipeline
import torch
#review put here rather than as argument when calling script in order to facilitate easy re-running for consistency testing
model_id = "meta-llama/Llama-3.2-1B-Instruct"
pipe = pipeline(
    "text-generation",
    model=model_id,
    device_map="auto",
)
messages = [#change system prompt to include (or not) explanation of review when desired
    {"role": "system", "content": """You are an advanced AI assistant created to perform sentiment analysis on reviews of college professors. I need you to analyze each review you receive and provide your analysis using the following csv format:
[teaching_sentiment, difficulty_sentiment]
teaching_sentiment = A floating-point representation of the sentiment of the review regarding the quality and effectiveness of teaching, rounded to two decimal places. Scale ranges from -1.0 (negative) to 1.0 (positive), where 0.0 represents neutral sentiment.
difficulty_sentiment = A floating-point representation of the sentiment of the review regarding how easy the class is, rounded to two decimal places. Scale ranges from -1.0 (difficult) to 1.0 (easy), where 0.0 represents neutral sentiment.
Always respond with the values for teaching_sentiment and difficulty_sentiment seperated by a comma. Do not include any other text or messages in your response.  Exclude markdown."""},
    {"role": "user", "content": "This class is NOT beginner friendly. The grading criteria is overwhelmingly unfair. If you are new to coding, unless you spend all day every day trying to learn this you aren't passing. The exams have questions that she never even mentions during the lectures. Like windows processes??? Just feels rigged. Also, she's weird and laughs like a maniac."},
]
outputs = pipe(
    messages,
    max_new_tokens=128,
    do_sample=True
)
print(outputs[0]["generated_text"][-1])
