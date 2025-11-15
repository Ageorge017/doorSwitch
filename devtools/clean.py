import os

def delete_all_in_current_directory():
    """Deletes all files and subdirectories in the current working directory,
    excluding 'boot.py' if present at the root level.
    """
    current_dir = os.getcwd()  # Get the current working directory

    for item in os.ilistdir(current_dir):
        name, type_code = item[0:2]
        full_path = f"{current_dir}/{name}"

        # Skip 'boot.py' if it's at the root of the filesystem to prevent bricking the device
        if current_dir == '/' and name == 'boot.py':
            continue

        if type_code == 0x8000:  # It's a file
            os.remove(full_path)
            print(f"Removed file: {full_path}")
        elif type_code == 0x4000: # It's a directory
            # Recursively delete contents of subdirectories
            delete_all_in_directory_recursive(full_path)
            os.rmdir(full_path)
            print(f"Removed directory: {full_path}")
            
def delete_all_in_directory_recursive(path):
    """Recursively deletes all files and subdirectories within a given path."""
    for item in os.ilistdir(path):
        name, type_code = item[0:2]
        full_path = f"{path}/{name}"

        if type_code == 0x8000:  # It's a file
            os.remove(full_path)
            print(f"Removed file: {full_path}")
        elif type_code == 0x4000:  # It's a directory
            delete_all_in_directory_recursive(full_path)
            os.rmdir(full_path)
            print(f"Removed directory: {full_path}")

# Call the function to delete all items in the current directory
delete_all_in_current_directory()