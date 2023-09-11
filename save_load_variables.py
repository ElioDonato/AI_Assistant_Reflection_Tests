from file_import import json
from prompts import default_values

# Function to load variables if they exist
def load_variables(folder_path):
    variables = {}
    for var_name, default_value in default_values.items():
        try:
            with open(f"{folder_path}/{var_name}.json", "r") as f:
                variables[var_name] = json.load(f)
        except FileNotFoundError:
            print(f"{var_name}.json not found. Initializing with default value.")
            variables[var_name] = default_value
    return variables

# Function to save the variables
def save_variables(user_profile, model_profile, summarization_memory, reflection_summary, interaction_history, folder_path):
    with open(f'{folder_path}/user_profile.json', 'w') as f:
        json.dump(user_profile, f)
    
    with open(f'{folder_path}/model_profile.json', 'w') as f:
        json.dump(model_profile, f)
    
    with open(f'{folder_path}/summarization_memory.json', 'w') as f:
        json.dump(summarization_memory, f)
    
    with open(f'{folder_path}/reflection_summary.json', 'w') as f:
        json.dump(reflection_summary, f)
    
    # Read existing interaction history if available
    existing_data = []
    try:
        with open(f'{folder_path}/interaction_history.json', 'r') as f:
            existing_data = json.load(f)
    except FileNotFoundError:
        print("interaction_history.json not found. A new file will be created.")
        
    # Append new interaction history
    existing_data.extend(interaction_history)
    
    # Save back to file
    with open(f'{folder_path}/interaction_history.json', 'w') as f:
        json.dump(existing_data, f)