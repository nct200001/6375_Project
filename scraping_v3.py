import requests
from bs4 import BeautifulSoup

# Define the input and output file names
input_file = "professor_urls.txt"
output_file = "all_reviews_output.txt"

# Function to process a single professor URL and extract reviews
def process_professor_url(url):
    reviews_data = []  # List to hold all reviews for this professor

    # Send a GET request to fetch the page content
    response = requests.get(url)

    if response.status_code == 200:
        # Parse the page content with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract the professor's name
        professor_name_tag = soup.find('h1', class_='NameTitle__NameWrapper-dowf0z-2 erLzyk')
        professor_name = professor_name_tag.get_text() if professor_name_tag else "Unknown Professor"

        # Find all review containers
        reviews = soup.find_all('div', class_='Rating__RatingBody-sc-1rhvpxz-0 dGrvXb')

        # Iterate over each review
        for review in reviews:
            review_data = {"Professor": professor_name}

            # Extract the course of the review
            course = review.find('div', class_='RatingHeader__StyledClass-sc-1dlkqw1-3 eXfReS')
            review_data["Course"] = course.get_text() if course else "Unknown"

            # Extract the quality score of the review
            quality_container = review.find('div', class_='CardNumRating__StyledCardNumRating-sc-17t4b9u-0 eWZmyX')
            if quality_container:
                quality_score_div = quality_container.find_all('div')[1]
                try:
                    review_data["Quality"] = float(quality_score_div.get_text())
                except (ValueError, IndexError):
                    review_data["Quality"] = "N/A"

            # Extract the difficulty score of the review
            difficulty = review.find('div', class_='CardNumRating__CardNumRatingNumber-sc-17t4b9u-2 cDKJcc')
            try:
                review_data["Difficulty"] = float(difficulty.get_text()) if difficulty else "N/A"
            except ValueError:
                review_data["Difficulty"] = "N/A"

            # Extract the date of the review
            date = review.find('div', class_='TimeStamp__StyledTimeStamp-sc-9q2r30-0 bXQmMr RatingHeader__RatingTimeStamp-sc-1dlkqw1-4 iwwYJD')
            review_data["Date"] = date.get_text() if date else "Unknown"

            # Extract the sentiment
            sentiment = review.find('div', class_='Comments__StyledComments-dzzyvm-0 gRjWel')
            review_data["Sentiment"] = sentiment.get_text() if sentiment else "N/A"

            # Extract all qualifiers for this review
            review_qualifiers = review.find_all('div', class_='MetaItem__StyledMetaItem-y0ixml-0 LXClX')
            review_data["Qualifiers"] = ', '.join(qualifier.get_text() for qualifier in review_qualifiers) if review_qualifiers else "None"

            # Append review data to list
            reviews_data.append(review_data)

    else:
        print(f"Failed to retrieve the page for URL: {url}. Status code: {response.status_code}")

    return reviews_data

# Read URLs from the input file
try:
    with open(input_file, "r") as file:
        urls = [line.strip() for line in file.readlines() if line.strip()]
except FileNotFoundError:
    print(f"Input file '{input_file}' not found.")
    urls = []

# List to hold all reviews from all URLs
all_reviews = []

# Process each URL
for url in urls:
    print(f"Processing URL: {url}")
    all_reviews.extend(process_professor_url(url))

# Write all reviews to the output file
try:
    with open(output_file, "w", encoding="utf-8") as file:  # Specify UTF-8 encoding
        # Write headers
        file.write("Professor | Course | Quality | Difficulty | Date | Sentiment | Qualifiers\n")
        file.write("-" * 100 + "\n")

        # Write each review
        for review in all_reviews:
            file.write(f"{review['Professor']} | {review['Course']} | {review['Quality']} | {review['Difficulty']} | {review['Date']} | {review['Sentiment']} | {review['Qualifiers']}\n")

    print(f"File writing successful: '{output_file}' created.")
except Exception as e:
    print(f"Error writing to file: {e}")
