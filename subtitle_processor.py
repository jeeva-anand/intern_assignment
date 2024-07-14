import re

# Function to read an ASS file and return its lines
def read_ass_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    return lines

# Function to write lines to an ASS file
def write_ass_file(file_path, lines):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(lines)

# Function to clean text by removing specific patterns
def clean_text(text):
    return re.sub(r'\{\\rH\}|\{\\r\}', '', text)

# Function to process event lines and create new events
def process_events(events):
    new_events = []
    
    # Determine the length of the text component in an event
    str_len = len(events[0].strip().split(",")[-1].split(" "))
    
    for i, event in enumerate(events):
        index = event.find(',Default')
        
        # Get the previous event text, clean it, and format it
        prev = events[i - str_len].strip().split(",")[-1] if i > str_len - 1 else '...'
        prev_text = clean_text(prev)
        prev_text = event[:index] + ",P,,0,0,0,," + prev_text + '\n'
        
        # Current event text
        curr_text = event[:-1] + '\n'
        
        # Get the next event text, clean it, and format it
        next = events[i + str_len].strip().split(",")[-1] if i < len(events) - str_len else '...'
        next_text = clean_text(next)
        next_text = event[:index] + ",F,,0,0,0,," + next_text + "\n\n"
        
        # Append formatted texts to new events list
        new_events.append(prev_text)
        new_events.append(curr_text)
        new_events.append(next_text)
    
    return new_events

# Main function to convert an input ASS file to an output ASS file
def convert_ass(input_file, output_file):
    # Read the input ASS file
    lines = read_ass_file(input_file)
    header = []
    events = []
    is_event_section = False

    # Separate the header and events sections
    for line in lines:
        if line.strip().lower().startswith("[events]"):
            is_event_section = True
            header.append(line)
        elif is_event_section and line.strip().startswith("Dialogue:"):
            events.append(line)
        else:
            header.append(line)
    
    # Process events and create new event lines
    new_events = process_events(events)
    output_lines = header + new_events
    
    # Write the new lines to the output ASS file
    write_ass_file(output_file, output_lines)

# Specify the input and output file paths
input_file = './original_subtitles.ass'
output_file = './processed_subtitles.ass'

# Convert the input_subtitles.ass to output_subtitles.ass
convert_ass(input_file, output_file)
