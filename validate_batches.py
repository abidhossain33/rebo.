"""
Validation script for the 15 batch files.
Checks:
- Existence of data_batch_01.json through data_batch_15.json
- Valid JSON formatting and parsing
- Exactly 1,000 items per file (total 15,000 items)
- Strict sequential IDs from Q00001 to Q15000 with no gaps or duplicates
- Completeness and structural validity of each record
"""

import json
import os
import sys

def validate():
    repo_dir = os.path.dirname(os.path.abspath(__file__))
    expected_files = [f"data_batch_{i:02d}.json" for i in range(1, 16)]
    total_items = 0
    seen_ids = set()
    current_expected_id = 1

    print("=== Starting Dataset Validation ===")
    
    for filename in expected_files:
        filepath = os.path.join(repo_dir, filename)
        if not os.path.exists(filepath):
            print(f"ERROR: File missing: {filename}")
            sys.exit(1)
        
        file_size = os.path.getsize(filepath)
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            print(f"ERROR: Failed to parse JSON in {filename}: {e}")
            sys.exit(1)
        
        if not isinstance(data, list):
            print(f"ERROR: Content in {filename} is not a JSON array.")
            sys.exit(1)
            
        count = len(data)
        if count != 1000:
            print(f"ERROR: {filename} contains {count} items, expected 1,000.")
            sys.exit(1)
            
        for item in data:
            if "id" not in item:
                print(f"ERROR: Missing 'id' in item in {filename}")
                sys.exit(1)
            q_id = item["id"]
            expected_id_str = f"Q{current_expected_id:05d}"
            if q_id != expected_id_str:
                print(f"ERROR: ID mismatch! Expected {expected_id_str}, got {q_id}")
                sys.exit(1)
            if q_id in seen_ids:
                print(f"ERROR: Duplicate ID found: {q_id}")
                sys.exit(1)
            seen_ids.add(q_id)
            current_expected_id += 1
            
            # Verify required fields
            for field in ["domain", "subfield", "instruction", "question", "difficulty", "research_type"]:
                if not item.get(field):
                    print(f"ERROR: Missing or empty field '{field}' in {q_id}")
                    sys.exit(1)
                    
        total_items += count
        print(f"[OK] {filename}: 1,000 items validated (IDs Q{(current_expected_id-1000):05d} to Q{(current_expected_id-1):05d}, size: {file_size/1024:.1f} KB)")

    if total_items != 15000:
        print(f"ERROR: Total items {total_items} != 15,000")
        sys.exit(1)

    print("\n=== Validation Successful! ===")
    print(f"Total files validated: {len(expected_files)}")
    print(f"Total questions: {total_items}")
    print(f"Sequential ID range: Q00001 to Q15000 (all verified, no gaps, no duplicates)")

if __name__ == "__main__":
    validate()
