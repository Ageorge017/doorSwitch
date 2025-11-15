import os

# Example: Moving 'my_file.txt' from the root to the 'data' folder
name = "private.key.der"
old_path = name
new_path = f"certs/{name}" 

try:
    # Create the destination directory if it doesn't exist
    dest_dir = new_path.split('/')[0]  # Extract 'certs' from 'certs/filename'
    try:
        os.mkdir(dest_dir)
        print(f"Created directory: {dest_dir}")
    except OSError:
        # Directory already exists, which is fine
        pass
    
    os.rename(old_path, new_path)
    print(f"File '{old_path}' moved to '{new_path}' successfully.")
except OSError as e:
    print(f"Error moving file: {e}")