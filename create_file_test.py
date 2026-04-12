import json
import os
import random
import pandas as pd

# We use the same config as script 1 to "read" the ground truth
BASE_DIR = "benchmark_assets"
FILE_TYPES = ["png", "jpg", "pdf", "csv"]
SAMPLES_PER_TYPE = 20 # 10 consistent, 10 conflicting

benchmark_data = []

def get_actual_value(file_path):
    # Logic to 'know' what we put in the files for the answer key
    ext = file_path.split('.')[-1]
    if ext in ["png", "jpg"]:
        # In a real pipeline, you'd track this in a DB. 
        # For this script, we'll assume the model needs to identify color/shape.
        return "N/A" # Placeholder logic

# Generate JSON entries
test_id = 1
for ftype in FILE_TYPES:
    for i in range(SAMPLES_PER_TYPE):
        is_conflicting = i >= (SAMPLES_PER_TYPE // 2)
        file_name = f"{ftype}_{i:02d}.{ftype}"
        file_path = os.path.join(BASE_DIR, file_name)
        
        # Scenario Logic
        if ftype in ["png", "jpg"]:
            color = random.choice(["red", "blue", "green"])
            text_color = random.choice(["yellow", "black"]) if is_conflicting else color
            
            # Create a Yes/No question 50% of the time
            if random.random() > 0.5:
                q = f"Is the shape in the file {color}? (yes/no)"
                f_ans = "yes"
                t_ans = "no" if is_conflicting else "yes"
            else:
                q = "What is the color of the shape?"
                f_ans = color
                t_ans = text_color
            
            text_input = f"A photo of a {text_color} object."
            
        else: # PDF or CSV
            metric = "Revenue"
            val = random.randint(50, 100)
            text_val = random.randint(10, 49) if is_conflicting else val
            
            if random.random() > 0.5:
                q = f"Is the {metric} value exactly {val}? (yes/no)"
                f_ans = "yes"
                t_ans = "no" if is_conflicting else "yes"
            else:
                q = f"What is the {metric} value?"
                f_ans = str(val)
                t_ans = str(text_val)
            
            text_input = f"The summary report indicates a {metric} of {text_val}."

        entry = {
            "id": test_id,
            "file_type": ftype,
            "file_path": file_path,
            "text_input": text_input,
            "question": q,
            "file_answer": f_ans,
            "text_answer": t_ans,
            "conflicting": is_conflicting,
            "modality_priority_target": "file" # Helpful for scoring
        }
        benchmark_data.append(entry)
        test_id += 1

# Save to JSON
with open("vlm_benchmark.json", "w") as f:
    json.dump(benchmark_data, f, indent=4)

print(f"Generated vlm_benchmark.json with {len(benchmark_data)} questions.")