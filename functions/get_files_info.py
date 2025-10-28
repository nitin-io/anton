import os

def get_files_info(working_directory, directory):
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
