import csv

def clean_dataset(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        reader = csv.DictReader(infile)
        
        # Assuming the output should have the same headers as the input
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        
        # Write the header to the output file
        writer.writeheader()
        
        for row in reader:
            if "en" in row.get('Language', ''):
                writer.writerow(row)

# Usage
input_file = '/Users/stefanodegiorgis/Desktop/ISD8/isd8-finetuning/resources/iscat-en-only.csv'
output_file = '/Users/stefanodegiorgis/Desktop/ISD8/isd8-finetuning/resources/iscat-en-only-out.csv'
clean_dataset(input_file, output_file)
print(f"Cleaning complete. Output saved to {output_file}")