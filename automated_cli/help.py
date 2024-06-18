def show_help():
    help_text = """
    GPTZoo CLI Help
    Usage:
      python gptzoo.py -search [options]
      python gptzoo.py -analyze [options]
      python gptzoo.py -help

    Options:
      -search               Search for GPT instances based on criteria
      -analyze              Analyze GPT instances by counting matches based on criteria
      -help                 Show this help message
      --name <name1> <name2> ...          Name keywords to filter by
      --author <author1> <author2> ...    Author keywords to filter by
      --rating <rating1> <rating2> ...    Rating keywords to filter by
      --tags <tag1> <tag2> ...            Tags to filter by
      --description <keyword1> <keyword2> ... Description keywords to filter by
      --chat_count           Chat count to filter by
      --release_date         Release date to filter by
      --category             Category to filter by

    Examples:
      python gptzoo.py -search --tags "programming" "software guidance" --description "software development"
      python gptzoo.py -analyze --name "Unknown" --chat_count
    """
    print(help_text)