import re
import os

def replace_pattern(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    pattern = r'}\n\s*{'
    replacement = r'},\n{'
    modified_content = re.sub(pattern, replacement, content)

    modified_lines = ['\t' + line for line in modified_content.split('\n')]

    modified_lines.insert(0, '[')

    modified_lines.append(']')

    modified_content = '\n'.join(modified_lines)

    modified_content = re.sub(r'\n\s*\n', '\n', modified_content)

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(modified_content)

    print(f"Pattern replacement completed successfully in {file_path}")

folder_path = r"F:\Projects\PycharmProjects\gpt_store\gptsapp_io\output"

for filename in os.listdir(folder_path):

    if filename.endswith('.json'):
        file_path = os.path.join(folder_path, filename)
        replace_pattern(file_path)