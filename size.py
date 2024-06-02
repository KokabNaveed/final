import os

def get_file_size(file_path):
    size_in_bytes = os.path.getsize(file_path)
    # Convert file size to megabytes (MB)
    size_in_mb = size_in_bytes / (1024 * 1024)
    return size_in_mb

# Example usage

current_dir = os.path.dirname(os.path.realpath(__file__))
file_path = os.path.join(current_dir, "audio.mp3")

# file_path = 'C:\\FA\\audio.mp3'
file_size_in_mb = get_file_size(file_path)
print(f"File Size: {file_size_in_mb:.2f} MB")
