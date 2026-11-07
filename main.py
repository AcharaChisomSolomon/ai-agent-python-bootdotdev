import argparse
import os
import json

from dotenv  import load_dotenv
from openai  import OpenAI
from prompts import system_prompt

from functions.get_files_info   import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file       import schema_write_file
from functions.run_python_file  import schema_run_python_file


def main():
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if api_key == None:
        raise RuntimeError("'OPENROUTER_API_KEY' not found")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    parser = argparse.ArgumentParser(description="AI-agent")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]

    available_functions = [
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file
    ]

    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        tools=available_functions
    )

    message = response.choices[0].message

    if response.usage is None:
        raise RuntimeError("no response returned from prompt")
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")

    if message.tool_calls != None:
        for tool_call in message.tool_calls:
            function_args = json.loads(tool_call.function.arguments or "{}")
            print(f"Calling function: {tool_call.function.name}({function_args})")
    else:
        print("Response:")
        print(message.content)


if __name__ == "__main__":
    main()
