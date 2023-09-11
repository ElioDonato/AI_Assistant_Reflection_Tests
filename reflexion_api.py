from prompts import *
from api_functions import complete, stream_complete, get_token_count

# Functions for Reflexion Assistant
async def update_user_profile_api(user_profile: str, conversation_history: str, user_prompt: str, request) -> str:
    prompt = user_profile_prompt.format(old_user_profile=user_profile, conversation_history=conversation_history, user_prompt=user_prompt)
    conversation_history = f"{conversation_history}\n{user_prompt}\n"
    return (await complete(prompt, request)).strip(), conversation_history

async def update_model_profile_api(model_profile: str, conversation_history: str, assistant_response: str, request) -> str:
    prompt = model_profile_prompt.format(old_model_profile=model_profile, conversation_history=conversation_history, assistant_response=assistant_response)
    conversation_history = f"{conversation_history}\n{assistant_response}"
    return (await complete(prompt, request)).strip(), conversation_history

async def generate_summarization_memory_api(user_profile: str, model_profile: str, conversation_history: str, old_summarization_memory: str, request) -> str:
    prompt = summarization_memory_prompt.format(user_profile=user_profile, model_profile=model_profile, conversation_history=conversation_history, old_summarization_memory=old_summarization_memory)
    return (await complete(prompt, request)).strip()

async def generate_new_reflection_api(conversation_history: str, user_prompt: str, assistant_response: str, request) -> str:
    user_prompt_and_response = f"{user_prompt}\n\n{assistant_response}"
    prompt = new_reflection_prompt.format(conversation_history=conversation_history, user_prompt_and_response=user_prompt_and_response)
    return (await complete(prompt, request)).strip()

async def integrate_new_reflection_api(old_reflection_summary: str, new_reflection: str, request) -> str:
    prompt = integrate_reflection_prompt.format(old_reflection_summary=old_reflection_summary, new_reflection=new_reflection)
    return (await complete(prompt, request)).strip()

async def generate_final_response_api(user_profile: str, model_profile: str, summarization_memory: str, reflection_summary: str, conversation_history: str, user_prompt: str, request) -> str:
    prompt = interaction_prompt.format(user_profile=user_profile, model_profile=model_profile, summarization_memory=summarization_memory, reflection_summary=reflection_summary, conversation_history=conversation_history, user_prompt=user_prompt)
    full_text = ""  # Initialize an empty string to hold the full text
    async for text in stream_complete(prompt, request):
        print(text, end="")  # This will print each piece of text as it arrives
        full_text += text  # This will accumulate the full text
    return full_text.strip()  # Return the full text when the streaming ends



# Main function to handle the entire conversation flow
async def reflexion_assistant_api(user_profile, model_profile, conversation_history, summarization_memory, reflection_summary, user_prompt, assistant_response, request):

    # Update User Profile
    request['stopping_strings'].append("\n\n")
    user_profile[0], conversation_history = await update_user_profile_api(user_profile[0], conversation_history, user_prompt, request)
    user_profile[1] = await get_token_count(user_profile[0])

    # Update Model Profile
    model_profile[0], conversation_history = await update_model_profile_api(model_profile[0], conversation_history, assistant_response, request)
    model_profile[1] = await get_token_count(model_profile[0])
    del request['stopping_strings'][-1]

    # Generate Summarization Memory
    summarization_memory[0] = await generate_summarization_memory_api(user_profile[0], model_profile[0], conversation_history, summarization_memory[0], request)
    summarization_memory[1] = await get_token_count(summarization_memory[0])

    # Generate New Reflection
    new_reflection = await generate_new_reflection_api(conversation_history, user_prompt, assistant_response, request)

    # Integrate New Reflection into Reflection Summary
    reflection_summary[0] = await integrate_new_reflection_api(reflection_summary[0], new_reflection, request)
    reflection_summary[1] = await get_token_count(reflection_summary[0])

    # Return the final response (or stream it in a real-world application)
    return user_profile, model_profile, summarization_memory, reflection_summary