import argparse
import os
import json
from datetime import datetime
from automated_cli import data_retrieval, data_analysis, help

def search_instances(criteria):
    results = data_retrieval.search(criteria)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'result/search_results_{timestamp}.json'
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f'Search results saved to {filename}')

def analyze_instances(criteria):
    count = data_analysis.analyze(criteria)
    print(f'Number of matching instances: {count}')

def main():
    parser = argparse.ArgumentParser(description="GPTZoo CLI")
    parser.add_argument('-search', action='store_true', help="Search for GPT instances")
    parser.add_argument('-analyze', action='store_true', help="Analyze GPT instances")
    parser.add_argument('-help', action='store_true', help="Show help information")
    parser.add_argument('--tags', nargs='+', help="Tags to filter by")
    parser.add_argument('--description', nargs='+', help="Description keywords to filter by")

    args = parser.parse_args()

    if args.help:
        help.show_help()
    elif args.search or args.analyze:
        criteria = {}
        if args.tags:
            criteria['tags'] = args.tags
        if args.description:
            criteria['description'] = args.description
        
        if args.search:
            search_instances(criteria)
        elif args.analyze:
            analyze_instances(criteria)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()