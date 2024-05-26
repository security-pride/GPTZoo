import os
import json

def search(criteria):
    dataset_dir = 'dataset'
    results = []

    for filename in os.listdir(dataset_dir):
        if filename.endswith('.json'):
            with open(os.path.join(dataset_dir, filename), 'r', encoding='utf-8') as f:
                data = json.load(f)
                for instance in data:
                    if all(any(keyword in instance.get(field, '') for keyword in keywords) for field, keywords in criteria.items()):
                        results.append(instance)

    return results