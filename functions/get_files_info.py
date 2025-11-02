import os
from config import MAX_CHARS
import subprocess

def is_valid_directory(working_directory, file_or_dir):
    # TODO: Make a decorator to validate path
    pass

def get_files_info(directory, working_directory="calculator"):
    abs_working_dir = os.path.abspath(working_directory)
    abs_dir = os.path.abspath(os.path.join(working_directory, directory))
    if not abs_dir.startswith(abs_working_dir):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    dir_contents = os.listdir(abs_dir)
    detailed = []
    for content in dir_contents:
        abs_path = os.path.abspath(os.path.join(abs_dir, content))
        is_dir = os.path.isdir(abs_path)
        size = os.path.getsize(abs_path)
        detailed.append(f" - {content}: file_size={size} bytes, is_dir={is_dir}")
    return f"Result for current directory: \n{"\n".join(detailed)}\n"

def get_file_content(working_directory, file_path):
    absolute_working_dir = os.path.abspath(working_directory)
    absolute_dir = os.path.abspath(os.path.join(working_directory, file_path))
    if not absolute_dir.startswith(absolute_working_dir):
      return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(absolute_dir):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    with open(absolute_dir, 'r') as file:
        file_content_string = file.read()
        char_count = len(file_content_string)
        if char_count > MAX_CHARS:
            file_content_string = file_content_string[:MAX_CHARS]
            file_content_string += f' [...FILE "{file_path}" truncated at {MAX_CHARS} characters]'
        return file_content_string

def write_file(working_directory, file_path, content):
    absolute_working_dir = os.path.abspath(working_directory)
    absolute_dir = os.path.abspath(os.path.join(working_directory, file_path))
    if not absolute_dir.startswith(absolute_working_dir):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    path = os.path.dirname(absolute_dir)
    if not os.path.exists(path):
        os.makedirs(path)
    with open(absolute_dir, "w") as f:
        f.write(content)
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

def run_python_file(working_directory, file_path, args=[]):
    absolute_working_dir = os.path.abspath(working_directory)
    absolute_dir = os.path.abspath(os.path.join(working_directory, file_path))
    if not absolute_dir.startswith(absolute_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(absolute_dir):
        return f'Error: File "{file_path}" not found.'
    if not absolute_dir.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    if len(args) > 0:
        args.insert(0, "python3")
        args.insert(1, absolute_dir)
    else:
        args = ["python3", absolute_dir]
    try:
        print("Command: ", " ".join(args))
        completed_process = subprocess.run(args=args, timeout=3, capture_output=True)
        return f"STDOUT: {completed_process.stdout}, STDERR: {completed_process.stderr}"
    except Exception as e:
        return f"Error: executing Python file: {e}"
