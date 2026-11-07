import os 
import subprocess


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    output = f'Result for executing "{file_path}":'
            
    abs_working_dir_path = os.path.abspath(working_directory)
    target_file_path     = os.path.normpath(os.path.join(abs_working_dir_path, file_path))
    valid_target_dir     = os.path.commonpath([abs_working_dir_path, target_file_path]) == abs_working_dir_path
    if not valid_target_dir:
        output += f'\n    Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        return output
    if not os.path.isfile(target_file_path):
        output += f'\n    Error: "{file_path}" does not exist or is not a regular file'
        return output
    if not target_file_path.endswith(".py"):
        output += f'\n    Error: "{file_path}" is not a Python file'
        return output

    try:
        command = ["python", target_file_path]
        if args is not None:
            command.extend(args)
        result = subprocess.run(command, text=True, timeout=30, capture_output=True)
        output += "\n\n"
        if result.returncode != 0:
            output += f"Process exited with code {result.returncode}"
    
        stdout = (result.stdout or "").strip()
        stderr = (result.stderr or "").strip()
    
        if not stdout and not stderr:
            output += "No output produced"
        else:
            if stdout:
                output += f"STDOUT:\n{stdout}"
            if stderr:
                output += f"STDERR:\n{stderr}"
        return output
    except Exception as e:
        output += f"\n    Error: executing Python file: {e}"
        return output


schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Executes a specified Python file within the working directory and returns its output",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the Python file to run, relative to the working directory",
                },
                "args": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Optional list of arguments to pass to the Python script",
                },
            },
            "required": ["file_path"],
        },
    },
}
