import os

# Get the current working directory
current_dir = os.getcwd()

# Construct the directory path for the output files
output_dir = os.path.join(current_dir, 'output')
os.makedirs(output_dir, exist_ok=True)  # Create the output directory if it doesn't exist

with open(os.path.join(output_dir, 'links.txt'), 'r') as file:
    links = [line.strip() for line in file.readlines() if line.strip() and line.strip().startswith('https:')]

print(f'Link counts: {len(links)}')

unique_links = set(links)
file_count = 2
chunk_size = 19000

for i in range(0, len(unique_links), chunk_size):
    chunk = list(unique_links)[i:i+chunk_size]
    output_file_path = os.path.join(output_dir, f'links_unique{file_count}.txt')

    with open(output_file_path, 'w') as file:
        for link in chunk:
            file.write(link + '\n')

    print(f'File {file_count}: {len(chunk)} links written to {output_file_path}')
    file_count += 1

print(f'Total unique counts: {len(unique_links)}')
