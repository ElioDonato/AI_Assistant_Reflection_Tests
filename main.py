from file_import import asyncio, signal, os, json
from save_load_variables import save_variables, load_variables
from api_functions import get_token_count, extract_name
from config import request, TRUNCATION_LENGTH, MAX_TOKENS
from prompts import interaction_prompt
from api_functions import remove_prefix
from reflexion_api import generate_final_response_api, reflexion_assistant_api

folder_path = ""
user_profile = []
model_profile = []           
summarization_memory = []
reflection_summary = []
interaction_history = []

# Function to handle Ctrl+C
def handle_exit(signum, frame):
    try:
        print("\nCtrl+C pressed. Saving variables...")
        save_variables(user_profile, model_profile, summarization_memory, reflection_summary, interaction_history, folder_path)
        print("Variables saved. Exiting...")
    except Exception as e:
        print(f"An error occurred while saving: {e}")
    finally:
        exit(0)

def initializing():
        # Ask the user for the name of the conversation
    conversation_name = input("Enter the name of the conversation you want to continue: ")

    # Define the folder path
    folder_path = f"./{conversation_name}"

    # Create the folder if it doesn't exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"New folder '{conversation_name}' created.")
    else:
        print(f"Continuing conversation '{conversation_name}'.")
    return folder_path

"""
async def assistant_logic(user_input, session):
    # Load all globals into session variables if not present.
    if 'interaction_history' not in session:
        session['interaction_history'] = []
        session['user_profile'], session['model_profile'], session['summarization_memory'], session['reflection_summary'] = load_variables()

    user_name = "User"
    assistant_name = "Assistant"
    user_name = extract_name(user_profile[0], user_name)
    assistan_name = extract_name(model_profile[0], assistan_name)

    interaction_history = session['interaction_history']

    # ... existing logic to prepare user prompt and conversation history ...
    
    user_prompt = [f"User:\n{user_input.strip()}"]
    user_prompt.append(await get_token_count(user_prompt[0]))

    # ... existing logic to generate assistant's response ...

    assistant_response = [remove_prefix(await generate_final_response_api(
        session['user_profile'][0], 
        session['model_profile'][0], 
        session['summarization_memory'][0], 
        session['reflection_summary'][0], 
        conversation_history[0], 
        user_prompt[0], 
        request))]
        
    assistant_response.append(await get_token_count(assistant_response[0]))
    
    # ... existing logic for reflexion_assistant_api ...

    session['user_profile'], session['model_profile'], session['summarization_memory'], session['reflection_summary'] = await reflexion_assistant_api(
        session['user_profile'],
        session['model_profile'],
        conversation_history[0],
        session['summarization_memory'],
        session['reflection_summary'],
        user_prompt[0],
        assistant_response[0],
        request
    )
    
    interaction_history.append(user_prompt.copy())
    interaction_history.append(assistant_response.copy())
    session['interaction_history'] = interaction_history

    # ... existing logic to save interaction_history ...

    return assistant_response[0]
"""
    
async def main():
    global user_profile
    global model_profile
    global summarization_memory
    global reflection_summary
    global interaction_history
    global folder_path

    folder_path = initializing()
    loaded_vars = load_variables(folder_path)

    user_profile = loaded_vars['user_profile']
    model_profile = loaded_vars['model_profile']
    summarization_memory = loaded_vars['summarization_memory']
    reflection_summary = loaded_vars['reflection_summary']
    interaction_history = loaded_vars['interaction_history']

    user_name = "User"
    assistan_name = "Assistant"

    # Attach the handler to the SIGINT signal
    signal.signal(signal.SIGINT, handle_exit)

    #interaction prompt token for later use
    interaction_prompt_tokens = await get_token_count(interaction_prompt.format(user_profile="", model_profile="", summarization_memory="", reflection_summary="", conversation_history="", user_prompt=""))

    if len(user_profile) < 2:
        user_profile.append(await get_token_count(user_profile[0]))

    if len(model_profile) < 2:
        model_profile.append(await get_token_count(model_profile[0]))

    conversation_history = [""]
    conversation_history.append(await get_token_count(conversation_history[0]))

    if len(summarization_memory) < 2:
        summarization_memory.append(await get_token_count(summarization_memory[0]))

    if len(reflection_summary) < 2:
        reflection_summary.append(await get_token_count(reflection_summary[0]))

    user_prompt = [""]
    user_prompt.append(await get_token_count(user_prompt[0]))

    assistant_response = [""]
    assistant_response.append(await get_token_count(assistant_response[0]))

    while True:
        #Get user input:
        user_name = extract_name(user_profile[0], user_name)
        assistan_name = extract_name(model_profile[0], assistan_name)
        print(f"{user_name}:")
        user_prompt[0] = f"User:\n{str(input()).strip()}"
        user_prompt[1] = await get_token_count(user_prompt[0])

        # generate the new conversation_history with the help of the interaction history
        t = TRUNCATION_LENGTH - (MAX_TOKENS + interaction_prompt_tokens + user_profile[1] + model_profile[1] + summarization_memory[1] + reflection_summary[1] + user_prompt[1])
        conversation_history = ["", 0]
        # Enumerate through interaction_history in reverse
        for _, i in reversed(list(enumerate(interaction_history))):
            t -= i[1]
            if t < 0:
                break
            else:
                # Prepend each item to the beginning of the conversation_history string
                conversation_history[0] = f"{i[0]}\n\n{conversation_history[0]}"
                conversation_history[1] += i[1]
        conversation_history[0] = conversation_history[0].strip()

        # Generate the Response to the User
        print(f"\n{assistan_name}:")
        request['stopping_strings'].append("User:")
        request['stopping_strings'].append("{user_name}:")
        assistant_response[0] = remove_prefix(await generate_final_response_api(user_profile[0], model_profile[0], summarization_memory[0], reflection_summary[0], conversation_history[0], user_prompt[0], request))
        del request['stopping_strings'][-1]
        del request['stopping_strings'][-1]
        # Reformat the user prompt and assistant response
        print("")
        assistant_response[0] = f"Assistant:\n{assistant_response[0]}"
        assistant_response[1] = await get_token_count(assistant_response[0])

        user_profile, model_profile, summarization_memory, reflection_summary = await reflexion_assistant_api(
        user_profile,
        model_profile,
        conversation_history[0],
        summarization_memory,
        reflection_summary,
        user_prompt[0],
        assistant_response[0],
        request
        )
        # Add the user prompt and the assistant response to the interaction_history
        interaction_history.append(user_prompt.copy())
        interaction_history.append(assistant_response.copy())


        # save the interaction_history
        if len(interaction_history) >= 100:
            existing_data = []

            # Attempt to read the existing JSON file
            try:
                with open("interaction_history.json", "r") as f:
                    existing_data = json.load(f)
            except FileNotFoundError:
                print("interaction_history.json not found. A new file will be created.")
            except json.JSONDecodeError:
                print("Error decoding the existing JSON data. A new file will be created.")
            except Exception as e:
                print(f"An unexpected error occurred: {e}. A new file will be created.")

            # Append the new 50 elements to existing data
            existing_data.extend(interaction_history[:50])

            # Attempt to write the updated data to the JSON file
            try:
                with open("interaction_history.json", "w") as f:
                    json.dump(existing_data, f)
            except Exception as e:
                print(f"An error occurred while writing to the JSON file: {e}")

            # Delete the first 50 elements from the list
            interaction_history = interaction_history[50:]

if __name__ == "__main__":
    asyncio.run(main())