import os
import json

def analyze(criteria):
    dataset_dir = 'dataset'
    count = 0

    for filename in os.listdir(dataset_dir):
        if filename.endswith('.json'):
            with open(os.path.join(dataset_dir, filename), 'r') as f:
                data = json.load(f)
                for instance in data:
                    if all(any(keyword in instance.get(field, '') for keyword in keywords) for field, keywords in criteria.items()):
                        count += 1
    
    return count