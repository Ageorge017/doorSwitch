# Open the file in read mode ('r')
# Replace 'your_file.txt' with the actual name of your file
try:
    with open('fatal_log_20251115_023621.txt', 'r') as f:
        # Read the entire content of the file
        content = f.read()
        # Print the content to the console
        print(content)
except OSError as e:
    print(f"Error reading file: {e}")