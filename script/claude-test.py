import anthropic
import csv

client = anthropic.Anthropic()
output_file = '/Users/stefanodegiorgis/Desktop/ISD8/resources/ISCAT_4_ISD8-test-out.txt'

def process_csv(file_path):
    with open(file_path, 'r', newline='', encoding='utf-8') as csvfile, \
         open(output_file, 'w', encoding='utf-8') as outfile:
        csv_reader = csv.DictReader(csvfile)

        for row in csv_reader:
            sentence = row['sentence']
            image_schema = row['image_schema']
            annotation = row['annotation']

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


                The sentence to be analised is:
                {sentence}
                """
                            }
                        ]
                    }
                ]
            )
            
            # Write the response to the output file
            outfile.write(message.content + "\n\n")  # Add an extra newline for separation
            
            # Also print to console for monitoring
            print(message.content)
            print("\n")  # Add an extra newline for separation in console output

# Usage
csv_file_path = '/Users/stefanodegiorgis/Desktop/ISD8/resources/isd8-limit-excedeed.csv'
process_csv(csv_file_path)