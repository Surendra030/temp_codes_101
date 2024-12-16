import pyzipper
import zipfile
import shutil
import os
import subprocess

def unzip_password_protected(zip_path, password, extract_to):
    try:
        # Open the password-protected zip file
        with pyzipper.AESZipFile(zip_path, 'r') as zip_file:
            zip_file.setpassword(password.encode())  # Set the password to access the zip file

            # Extract all files to the specified directory
            zip_file.extractall(path=extract_to)

        print(f"Files successfully extracted to {extract_to}")
    except Exception as e:
        print(f"Error while extracting files: {e}")

def unzip_file(zip_path, extract_to):
    try:
        # Open the zip file
        with zipfile.ZipFile(zip_path, 'r') as zip_file:
            # Extract all files to the specified directory
            zip_file.extractall(path=extract_to)

        print(f"Files successfully extracted to {extract_to}")
    except Exception as e:
        print(f"Error while extracting files: {e}")

def move_files_to_working_dir(source_dir, working_dir):
    try:
        # Iterate through all files in the source directory
        for file_name in os.listdir(source_dir):
            full_file_path = os.path.join(source_dir, file_name)

            if os.path.isfile(full_file_path):
                # Move each file to the working directory
                shutil.move(full_file_path, working_dir)

        print(f"Files successfully moved to {working_dir}")
    except Exception as e:
        print(f"Error while moving files: {e}")

def run_python_script():
    """Run a Python script using subprocess."""
    try:
        # Execute the Python script using subprocess
        result = subprocess.run(["python", "./test/upload_videos_from_cloud.py"])


        # Print the script output
        print("Script output:")
        print(result.stdout)

        # Print any errors from the script
        if result.stderr:
            print("Script errors:")
            print(result.stderr)
    
    except Exception as e:
        print(f"Error while running script: {e}")


# Example usage
protected_zip_path = "protected.zip"  # Path to the password-protected zip file
password = os.getenv("PASSWORD") # Password for the protected zip file
protected_extract_to = "extracted_protected"  # Path to extract the protected zip file

# Step 1: Unzip the protected zip file
unzip_password_protected(protected_zip_path, password, protected_extract_to)

# Step 2: Locate the inner non-protected zip file
inner_zip_path = os.path.join(protected_extract_to, "test.zip")  # Replace with the actual inner zip name
inner_extract_to = os.getcwd()  # Path to extract the inner zip file

# Step 3: Unzip the non-protected zip file
unzip_file(inner_zip_path, inner_extract_to)

# Step 4: Move extracted files to the working directory
shutil.rmtree("extracted_protected")

print(os.listdir())

run_python_script()