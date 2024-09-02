import csv
import json
import random

def convert_csv_to_json(input_file, output_file):
    variations = [
        "Create a sentence demonstrating the following image schema(s):",
        "Compose a statement that illustrates this image schema:",
        "Craft a sentence showcasing the given image schema(s):",
        "Formulate an expression using the following image schema(s):",
        "Construct a sentence that embodies this image schema:",
        "Devise a phrase exemplifying the provided image schema(s):",
        "Write a sentence that captures the essence of this image schema:",
        "Produce a statement reflecting the following image schema(s):",
        "Design a sentence that manifests the given image schema:",
        "Develop an example sentence for this image schema:",
        "Articulate a thought using the following image schema(s):",
        "Shape a sentence around this image schema:",
        "Frame a statement that represents the given image schema(s):",
        "Invent a sentence portraying the following image schema:",
        "Build a phrase that encapsulates this image schema:",
        "Assemble words to depict the provided image schema(s):",
        "Fashion a sentence embodying the following image schema:",
        "Contrive an expression that mirrors this image schema:",
        "Concoct a statement exhibiting the given image schema(s):",
        "Synthesize a sentence that conveys the following image schema:"
    ]

    conversations = []
    
    with open(input_file, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            prompt = random.choice(variations)
            conversation = [
                {
                    "from": "human",
                    "value": f"{prompt} {row['IS_ANNOTATION']}"
                },
                {
                    "from": "gpt",
                    "value": f"{row['LinguisticExamples']}"
                }
            ]
            conversations.append(conversation)
    
    result = {"conversations": conversations}
    
    with open(output_file, 'w') as jsonfile:
        json.dump(result, jsonfile, indent=2)

# Usage
input_file = '/Users/stefanodegiorgis/Desktop/ISD8/isd8-finetuning/resources/iscat2finetune_en.csv'
output_file = '/Users/stefanodegiorgis/Desktop/ISD8/isd8-finetuning/resources/iscat2finetune_en_var_out.json'
convert_csv_to_json(input_file, output_file)
print(f"Conversion complete. Output saved to {output_file}")