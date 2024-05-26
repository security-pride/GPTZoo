def show_help():
    help_text = """
    GPTZoo CLI Help
    Usage:
      python gptzoo.py -search --tags <tag1> <tag2> ... --description <keyword1> <keyword2> ...
      python gptzoo.py -analyze --tags <tag1> <tag2> ... --description <keyword1> <keyword2> ...
      python gptzoo.py -help

    Options:
      -search       Search for GPT instances based on criteria
      -analyze      Analyze GPT instances by counting matches based on criteria
      -help         Show this help message

    Examples:
      python gptzoo.py -search --tags "programming" "software guidance" --description "software development"
      python gptzoo.py -analyze --tags "programming" "software guidance" --description "software development"
    """
    print(help_text)