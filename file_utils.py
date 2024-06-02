import os

def calculate_file_size(file_path):
    if os.path.exists(file_path):
        # Get the file size in bytes
        file_size_bytes = os.path.getsize(file_path)
        
        # Convert bytes to megabytes
        file_size_mb = file_size_bytes / (1024 * 1024)
        
        return file_size_mb
    else:
        return None
