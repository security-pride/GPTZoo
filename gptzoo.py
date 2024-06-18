import argparse
import os
import json
from datetime import datetime
import pandas as pd
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
    results = data_analysis.analyze(criteria)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'result/analyze_results_{timestamp}.csv'
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    results.to_csv(filename, index=False)
    print(f'Analysis results saved to {filename}')

def main():
    parser = argparse.ArgumentParser(description="GPTZoo CLI")
    parser.add_argument('-search', action='store_true', help="Search for GPT instances")
    parser.add_argument('-analyze', action='store_true', help="Analyze GPT instances")
    parser.add_argument('-help', action='store_true', help="Show help information")
    parser.add_argument('--tags', nargs='+', help="Tags to filter by")
    parser.add_argument('--description', nargs='+', help="Description keywords to filter by")
    parser.add_argument('--name', nargs='+', help="Name keywords to filter by")
    parser.add_argument('--author', nargs='+', help="Author keywords to filter by")
    parser.add_argument('--rating', nargs='+', help="Rating keywords to filter by")
    parser.add_argument('--chat_count', action='store_true', help="Chat count to filter by")
    parser.add_argument('--release_date', action='store_true', help="Release date to filter by")
    parser.add_argument('--category', action='store_true', help="Category to filter by")

    args = parser.parse_args()

    if args.help:
        help.show_help()
    elif args.search or args.analyze:
        criteria = {}
        if args.tags:
            criteria['tags'] = args.tags
        if args.description:
            criteria['description'] = args.description
        if args.name:
            criteria['name'] = args.name
        if args.author:
            criteria['author'] = args.author
        if args.rating:
            criteria['rating'] = args.rating
        if args.chat_count:
            criteria['chat_count'] = args.chat_count
        if args.release_date:
            criteria['release_date'] = args.release_date
        if args.category:
            criteria['category'] = args.category

        if args.search:
            search_instances(criteria)
        elif args.analyze:
            analyze_instances(criteria)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()