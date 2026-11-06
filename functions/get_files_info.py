import os


def get_files_info(working_directory: str, directory: str = ".") -> str:
    output = f'Result for {"current" if directory == "." else f'"{directory}"'} directory:'

    abs_working_dir_path = os.path.abspath(working_directory)
    target_dir           = os.path.normpath(os.path.join(abs_working_dir_path, directory))
    valid_target_dir     = os.path.commonpath([abs_working_dir_path, target_dir]) == abs_working_dir_path
    if not valid_target_dir:
        output += f'\n    Error: Cannot list "{directory}" as it is outside the permitted working directory'
        return output
    if not os.path.isdir(target_dir):
        output += f'\n    Error: "{directory}" is not a directory'
        return output

    for item in os.listdir(target_dir):
        file_size = os.path.getsize(target_dir + f"/{item}")
        is_dir    = os.path.isdir(target_dir + f"/{item}")
        output   += f"\n  - {item}: file_size={file_size} bytes, is_dir={is_dir}"
    return output
