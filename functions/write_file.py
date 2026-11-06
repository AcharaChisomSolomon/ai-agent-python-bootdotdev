import os


def write_file(working_directory: str, file_path: str, content: str) -> str:
    output = f'Result for writing to "{file_path}":'
        
    abs_working_dir_path = os.path.abspath(working_directory)
    target_file_path     = os.path.normpath(os.path.join(abs_working_dir_path, file_path))
    valid_target_dir     = os.path.commonpath([abs_working_dir_path, target_file_path]) == abs_working_dir_path
    if not valid_target_dir:
        output += f'\n    Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        return output
    if os.path.isdir(target_file_path):
        output += f'\n    Error: Cannot write to "{file_path}" as it is a directory'
        return output

    dirs_and_files   = target_file_path.split("/")
    target_file_path = "/".join(dirs_and_files[:-1])
    os.makedirs(target_file_path, exist_ok=True)
    target_file_path = target_file_path + "/" + dirs_and_files[-1]
    try:
        with open(target_file_path, "w") as f:
            f.write(content)
    except Exception:
        output += f"\n    Error: failed to write to \"{file_path}\""
        return output
    output += f'\n    Successfully wrote to "{file_path}" ({len(content)} characters written)'
    return output