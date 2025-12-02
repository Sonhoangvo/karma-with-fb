import openai
import json
from .feedback import get_llm_feedback
import re
import os # Import os module to handle file paths

# Configuration for OpenAI API (assuming these are constant for the project)
openai.api_base = "https://openrouter.ai/api/v1"
openai.api_key = "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"

# Define paths relative to the project root
SIMILARITY_FLAG_PATH = 'logs/similarity_flag.json'
MESSAGES_PATH = 'logs/messages.json'
PROMPTS_DIR = 'prompts'
RESOURCES_DIR = 'resources'
TARGET_TASK_FUNCTIONS_PATH = 'scripts/task_functions.py'
GENERATED_FUNCTION_NAME_PATH = 'logs/generated_function_name.json'

def load_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def insert_code_into_file(new_code, target_file_path, start_line_number):
    with open(target_file_path, 'r') as file:
        lines = file.readlines()

    # Preserve content before the generated function
    before_function_content = lines[:start_line_number - 1]

    # Find the end of the existing generated function
    # Assuming the function is a top-level function, find the next top-level 'def' or end of file
    end_of_function_index = start_line_number - 1
    # Iterate from the presumed start of the function (start_line_number - 1)
    # to find where the old function ends.
    # It ends either at the next top-level 'def' or at the end of the file.
    for i in range(start_line_number - 1, len(lines)):
        stripped_line = lines[i].strip()
        # Look for a 'def ' that is not part of the current function's body
        # (i.e., not indented further than the current function)
        # For simplicity, we assume the first 'def ' after the current one marks the end
        if stripped_line.startswith("def ") and i >= start_line_number: # start_line_number is 1-indexed
            end_of_function_index = i
            break
        elif i == len(lines) - 1: # Reached end of file
            end_of_function_index = len(lines)
            break
        else: # Continue consuming lines as part of the function
            end_of_function_index = i + 1
    
    # If no other 'def' found, the function goes to the end of the file from start_line_number
    if end_of_function_index < start_line_number:
         end_of_function_index = len(lines)

    # Preserve content after the generated function
    after_function_content = lines[end_of_function_index:]

    new_full_content_lines = before_function_content + new_code.splitlines(keepends=True) + after_function_content

    with open(target_file_path, 'w') as file:
        file.writelines(new_full_content_lines)


def load_similarity_flag():
    try:
        with open(SIMILARITY_FLAG_PATH, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data.get("similarity_flag", False)
    except FileNotFoundError:
        return False

def generate_and_correct_plan(user_instruction):
    use_short_term_memory = load_similarity_flag()
           
    skills = load_file(os.path.join(PROMPTS_DIR, 'skills.txt'))
    skills_ex = load_file(os.path.join(RESOURCES_DIR, 'actions.py'))
    role = load_file(os.path.join(PROMPTS_DIR, 'role.txt'))
    examples = load_file(os.path.join(PROMPTS_DIR, 'examples.txt'))
    emphasize = load_file(os.path.join(PROMPTS_DIR, 'emphasize.txt'))
    instruction_prompt = f"Please help me decompose the following tasks: {user_instruction}. Please output only the generated code."
    short_term_memory = load_file(os.path.join(PROMPTS_DIR, 'short_term_memory.txt'))
    long_term_memory = load_file(os.path.join(PROMPTS_DIR, 'long_term_memory.txt'))

    messages = [
        {"role": "user", "content": skills},
        {"role": "user", "content": skills_ex},
        {"role": "system", "content": role},
        {"role": "user", "content": examples},
        {"role": "user", "content": emphasize},
        {"role": "user", "content": long_term_memory},
        {"role": "user", "content": instruction_prompt}
    ]

    if use_short_term_memory:
        messages.insert(5, {"role": "user", "content": short_term_memory})

    with open(MESSAGES_PATH, 'w', encoding='utf-8') as file:
        json.dump(messages, file, ensure_ascii=False, indent=4)    

    # Initial plan generation
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini-2024-07-18",
        messages=messages,
        max_tokens=4096,
        temperature=0,
        stop=None
    )

    response_content = response.choices[0].message['content'].strip()

    lines = response_content.split('\n')
    code_lines = []
    recording = False
    function_name = None

    for line in lines:
        if line.strip().startswith("def "):
            recording = True
            function_name = line.split('(')[0].split()[1]
        if recording:
            if line.strip() == '```':
                continue
            code_lines.append(line)

    api_generated_code = '\n'.join(code_lines).strip()

    print("--- Initial Generated Plan ---")
    print(api_generated_code)
    print("--------------------")

    # Get feedback on the generated plan
    print("Getting feedback on the plan...")
    feedback_text, improved_code = get_llm_feedback(api_generated_code, messages)

    print("--- LLM Feedback ---")
    print(feedback_text)
    print("--------------------")

    final_plan_code = api_generated_code
    if improved_code:
        print("\n--- Applying Suggested Improvements ---")
        final_plan_code = improved_code
        print("--- Modified Plan ---")
        print(final_plan_code)
        print("--------------------")
    else:
        print("\nNo specific code improvements suggested by the LLM.")

    return final_plan_code, feedback_text, function_name

if __name__ == '__main__':
    # Example usage when run as a script
    user_task = "wash the apple"
    final_plan, feedback_output, func_name = generate_and_correct_plan(user_task)
    
    # In the original script, this part would insert code into task_functions.py
    # and save the function name. This needs to be handled by the caller (GUI_karma.py)
    # or by a separate execution step if it's still desired to write to file.
    
    # For now, just print what would have been written
    print(f"\n--- Final Plan to be executed ---")
    print(final_plan)
    print(f"\n--- Generated Function Name ---")
    print(func_name)
    
    insert_code_into_file(final_plan, TARGET_TASK_FUNCTIONS_PATH, 6)
    with open(GENERATED_FUNCTION_NAME_PATH, 'w') as file:
        json.dump({"function_name": func_name}, file)
