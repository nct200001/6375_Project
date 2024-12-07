from transformers import pipeline
import torch

#review put here rather than as argument when calling script in order to facilitate easy re-running for consistency testing
review_text = """I came to class 4 minutes late and she marked me absent but she marked other people present that came 10+ minutes late, she calls people out pls dont take if you love yourself.
Overly strict for no reason. Kind of a rude teacher and has a lot of attitude. Not engaging. Very nit-picky on CS code which isn't even related to the code itself but the comments. No earbuds, if you get caught wearing earbuds you will get called out in front of the whole class and even risk being absent. The assigned seats thing is very childish.
creepy smile, do not take if you want a free grade
Professor Thompson's class is challenging but engaging.
Tough grader, not kind to students
Horrible, do not take.
This is the toughest grader ever, she will nitpick you with every little mistake that has nothing to do with the code and mainly with the Code Comments like it's an English class. You will lose points if you forget a single space or tab.
Overall, she is kind and respectful at times but also strict and treats students like highschool, no earbuds during lectures or she will yell at you. She is very nitpicky when it comes to programing style guideline. Oh, you forget a single space? Minus points. You forget a single tab? Minus Points. Hardly ever getting 100 in lab...
Thought she was gonna be great, but she proved me wrong.After a month she made a seating chart on the one day I wasn't in class.She marked me absent for the next class after that just because I wasn't in the right seat (that I didn't choose) even though she talked to me during attendence.I just completely stopped going to class and still got a B...
Do not take this professor: very exam heavy and lecture heavy. Teaches materials less than a week before exam and has seating charts.
Goes in depth on content/explains things well, but takes an hour to explain what could as easily be done in 30 min+makes you stay in class (2hr15m long) until you finish that day's lab, which she doesnt give access to until after 1hr+ lecture. Avoid her if u can, the evil laugh thing is not a joke.2 exams-70%, labs-15%,assignments-10%,attendance-5%
Thompson is a pretty decent teacher in that she goes in depth but that causes her to be 1-2 weeks behind other classes. But she only has 2 labs per week, 3 coding assignments, and only 2 tests. But you have to write code on the test so I recommend to take another professor cause 50% of test grade is coding which is take-home. Overall, she's fine.
This class is NOT beginner friendly. The grading criteria is overwhelmingly unfair. If you are new to coding, unless you spend all day every day trying to learn this you aren't passing. The exams have questions that she never even mentions during the lectures. Like windows processes??? Just feels rigged. Also, she's weird and laughs like a maniac.
She gives 2 tests throughout the semester, which is the midterm (35%) and the final (35%) which makes up for 70%, attendance is mandatory, and she will even count you late if you are not on time. Lectures can get boring since she is just reading off the slides, there are labs every single class, If you dont know how to code, then dont take it.
Took her as a freshmen, and now I'm a senior. This professor is really the bottom of the barrel. I had already been programming for several years. Her teaching was obtuse and removed from learning; thus, it made things hard despite already knowing what I was doing. Her tests asked overly specific questions, including things about her personal life.
Great professor, easily to understand and follow along. She will answer any question you have while not faulting you for asking. It is a very exam focused call so study for the Exams. I recommend you read the book to get a better understanding of C++. The textbook also has a lot of the solutions for assignments and lab assignment.
For a freshman course, she makes her test and overall assignments in a way that if you don't read the textbook back to back you're going to fail. Avoid her at all cost, I would wait for next semester if she's the only professor available. Mandatory attendance and she starts counting attendance 5min before the class starts.
She takes her time and explains the code really well. The test can be short in the fact that some of the code traces weigh a lot on the test so make sure you don't mess up in the code traces or else the whole question gets marked wrong. The labs and the practice assignments arn't bad and are engaging and helpful.
*Note this is for CS 1136 NOT CS 1336* Never met Prof Thompson in person, as the TA's ran the lab, but received multiple emails throughout the course regarding hints with assignments, extensions for labs, and additional submissions on Zylabs (sent to everyone in the class). Accommodations were reasonable, and the lab was not hard overall.
Worst cs professor , if you take her just be prepared to take labs at 9pm with no real help . Attendance is mandatory and she starts class 5 min early to take attendance (so if you come to class on time she'll mark you late)  , and makes class last 15m longer , so prepare to have 20m wasted . Her laugh is absolutely diabolical and makes you cringe."""

model_id = "fine-tuned-model"
pipe = pipeline(
    "text-generation",
    model=model_id,
    device_map="auto",
)
messages = [#change system prompt to include (or not) explanation of review when desired
    {"role": "system", "content": """You are an advanced AI assistant created to perform sentiment analysis on reviews of college professors. You will be prompted with a batch of reviews for the same professor, with each review placed on a new line. I need you to analyze each batch of reviews you receive and provide your analysis using the following csv format:
[teaching_sentiment, difficulty_sentiment, sentiment_explanation]
teaching_sentiment = A floating-point representation of the average sentiment of the reviews regarding the quality and effectiveness of teaching, rounded to two decimal places. Scale ranges from -1.0 (negative) to 1.0 (positive), where 0.0 represents neutral sentiment.
difficulty_sentiment = A floating-point representation of the average sentiment of the reviews regarding how easy the class is, rounded to two decimal places. Scale ranges from -1.0 (difficult) to 1.0 (easy), where 0.0 represents neutral sentiment.
sentiment_explanation = A brief description explaining the logic used to determine the values of teaching_sentiment and difficulty_sentiment
Always respond with the values for teaching_sentiment, difficulty_sentiment, and sentiment_explanation seperated by commas. Do not include any other text or messages in your response."""},
    {"role": "user", "content": review_text},
]
outputs = pipe(
    messages,
    max_new_tokens=16384,
    do_sample=True
)
print(outputs[0]["generated_text"][-1])
