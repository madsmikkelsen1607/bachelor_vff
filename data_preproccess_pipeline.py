import pandas as pd
import os
import json
from pathlib import Path

current_dir = Path.cwd()
project_root = os.path.abspath(os.path.join(current_dir, ".."))  # Move up to root if needed

# Relative path to the video files folder
video_dir = os.path.join(project_root, "videos")
data_dir = os.path.join(project_root, "vff_loc_data")

import os
import json
import pandas as pd

# File path construction
file_name = "full-markings-3.jsonl"
file_path = os.path.join(data_dir, file_name)

print(f"Looking for file at: {file_path}")

# Initialize lists for valid and invalid data
valid_events = []
invalid_lines = []

# Open and process the file
try:
    with open(file_path, 'r') as file:
        for i, line in enumerate(file):
            line = line.strip()
            if not line:
                invalid_lines.append((i, "Empty line"))
                continue

            try:
                # Parse the JSON line
                data = json.loads(line)

                # Check if optaEvent exists and is valid
                if "optaEvent" in data and data["optaEvent"] is not None:
                    valid_events.append(data["optaEvent"])
                else:
                    invalid_lines.append((i, "'optaEvent' is None or missing"))

            except json.JSONDecodeError as e:
                invalid_lines.append((i, f"Malformed JSON: {e}"))

    print(f"Processed {i + 1} lines. Found {len(valid_events)} valid events and {len(invalid_lines)} invalid lines.")

    # Convert valid events to a DataFrame
    valid_df = pd.json_normalize(valid_events, sep='_')

    # Save valid events to CSV
    output_csv_path = "valid_events_data.csv"
    valid_df.to_csv(output_csv_path, index=False, na_rep='null')
    print(f"Valid events saved to {output_csv_path}")

    # Logging invalid lines
    if invalid_lines:
        log_path = "invalid_lines_log.txt"
        with open(log_path, 'w') as log_file:
            for line_no, reason in invalid_lines:
                log_file.write(f"Line {line_no}: {reason}\n")
        print(f"Invalid lines logged to {log_path}")

except FileNotFoundError:
    print(f"Error: File not found at {file_path}")
