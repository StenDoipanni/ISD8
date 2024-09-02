import anthropic
import csv
from anthropic import APIError, InternalServerError, RateLimitError
import time

max_retries = 5
retry_delay = 5  # seconds

client = anthropic.Anthropic()
output_file = '/Users/stefanodegiorgis/Desktop/ISD8/out/isd8-chunk4.json'

def process_sentence(sentence):
    for attempt in range(max_retries):
        try:
            message = client.messages.create(
                model="claude-3-5-sonnet-20240620",
                max_tokens=1000,
                temperature=0,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": f"""
                    Consider the following list of image schemas:
                    [CENTER-PERIPHERY, CONTACT, CONTAINMENT, COVERING, FORCE, LINK, OBJECT, PART-WHOLE, SCALE, SOURCE_PATH_GOAL, SPLITTING, SUBSTANCE, SUPPORT, VERTICALITY]

                    Task 1:
                    For the following sentence, annotate one, or more, image schemas that apply. Order them starting from the most relevant to the least. Do not provide any further explanation or description, just write the original sentence, and list the annotation with the above mentioned rationale.

                    Example:
                    "sentence" : "That idea bowled me over."
                    "annotation" : CONTACT, SOURCE_PATH_GOAL, FORCE"

                    "sentence" : "There are seven days in a week."
                    "annotation" : CONTAINMENT, PART-WHOLE

                    "sentence" : "We connect."
                    "annotation" : LINK, FORCE, CONTACT, SOURCE_PATH_GOAL

                    Task 2:
                    In addition to this: note that the sentence is pretty metaphorical. Consider the same image schematic pattern, and generate a more literal sentence.

                    Metaphorical Example:
                    "Religion is the pillar of certain societies."
                    Literal Sentence:
                    "The column is the pillar of the roof"

                    Metaphorical Example:
                    "I was touched by his remark."
                    Literal Sentence:
                    "The cup touches the table."

                    Metaphorical Example:
                    "Our agenda is packed with events."
                    Literal Sentence:
                    "The bag is packed with clothes."

                    Provide the output as json line file with these keys: "original", "annotation", "literal".

                    The sentence to be analised is:
                    {sentence}
                    """
                            }
                        ]
                    }
                ]
            )
            content = message.content[0].text if isinstance(message.content, list) else message.content
            return content
        except (APIError, InternalServerError, RateLimitError) as e:
            if attempt < max_retries - 1:
                print(f"Error occurred: {str(e)}. Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                print(f"Failed to process sentence after {max_retries} attempts: {sentence}")
                return f"Error processing sentence: {sentence}\nError: {str(e)}"
            
def process_csv(file_path):
    with open(file_path, 'r', newline='', encoding='utf-8') as csvfile, \
         open(output_file, 'w', encoding='utf-8') as outfile:
        csv_reader = csv.DictReader(csvfile)

        for row in csv_reader:
            sentence = row['sentence']
            
            content = process_sentence(sentence)
            
            # Write the response to the output file
            outfile.write(content + "\n\n")  # Add an extra newline for separation
            
            # Also print to console for monitoring
            print(content)
            print("\n")  # Add an extra newline for separation in console output


# Usage
csv_file_path = '/Users/stefanodegiorgis/Desktop/ISD8/resources/chunks/isd8-1920-end.csv'
process_csv(csv_file_path)