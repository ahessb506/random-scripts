import os
import pandas as pd
import glob
import csv  # Import the csv module

# Define the directory containing your CSV files
csv_directory = 'transcripts/'  # Replace with your directory path

# Use glob to get all CSV files in the directory
csv_files = glob.glob(os.path.join(csv_directory, '*.csv'))

# Initialize lists to store summaries, conversations, and filenames
summaries = []
conversations = []
filenames = []

for file in csv_files:
    try:
        with open(file, 'r', encoding='utf-8') as f:
            lines = f.read().splitlines()
        
        # Initialize variables
        summary = ''
        conversation = []
        in_conversation = False

        for line in lines:
            if line.strip() == "Conversation":
                in_conversation = True
                continue
            
            if not in_conversation:
                summary += line.strip() + ' '
            else:
                conversation.append(line.strip())
        
        # Check if summary and conversation were found
        if not summary:
            print(f"Warning: No summary found in {file}.")
        if not conversation:
            print(f"Warning: No conversation found in {file}.")

        # Append to lists
        summaries.append(summary.strip())
        conversations.append(' '.join(conversation))  # Use '\n'.join(conversation) if preserving line breaks
        filenames.append(os.path.basename(file))
    
    except Exception as e:
        print(f"Error processing {file}: {e}")

# Create a DataFrame
data = {
    'Filename': filenames,
    'Summary': summaries,
    'Conversation': conversations
}

df = pd.DataFrame(data)

# Save to a new CSV file with proper quoting
output_file = 'combined_transcripts.csv'
df.to_csv(output_file, index=False, encoding='utf-8', quoting=csv.QUOTE_ALL)  # Use csv.QUOTE_ALL here

print(f"All transcripts have been combined into {output_file}")