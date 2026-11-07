import os
from config import MAX_CHARS


def get_file_content(working_directory: str, file_path: str) -> str:
    output = f'Result for reading "{file_path}" file:'
    
    abs_working_dir_path = os.path.abspath(working_directory)
    target_file_path     = os.path.normpath(os.path.join(abs_working_dir_path, file_path))
    valid_target_dir     = os.path.commonpath([abs_working_dir_path, target_file_path]) == abs_working_dir_path
    if not valid_target_dir:
        output += f'\n    Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        return output
    if not os.path.isfile(target_file_path):
        output += f'\n    Error: File not found or is not a regular file: "{file_path}"'
        return output

    with open(target_file_path, "r") as f:
        file_content_string = f.read(MAX_CHARS)
        if f.read(1):
            file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
    output += f"\n\n{file_content_string}"
    return output

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": f"Retrieves the content (at most {MAX_CHARS} characters) of a specified file within the working directory",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file to read, relative to the working directory",
                },
            },
            "required": ["file_path"],
        },
    },
}
