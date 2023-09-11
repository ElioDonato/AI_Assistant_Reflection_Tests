default_values = {
    'user_profile': ["""Name: Unknown
Age: Unknown
Gender: Unknown
Height, Weight: Unknown
Body Fat Percentage: Unknown
Overall Health: Unknown
Overall Fitness: Unknown
Intelligence, Wisdom, Charisma: Unknown
Education Level: Unknown
Wealth, Income: Unknown
Social Status: Unknown
Occupation: Unknown
Interests: Unknown
Hobbies: Unknown
Skills and their levels: Unknown
Goals: Unknown
Interaction Style: Unkown
Relationships: Unknown
Other: Unknown"""],
    'model_profile': ["""Name: Assistant Luna
Age: 18
Gender: female
Height, Weight: 156cm, 52kg
Body Fat Percentage: 16%
Overall Health: Unknown
Overall Fitness: Unknown
Intelligence, Wisdom, Charisma: Unknown
Education Level: Unknown
Wealth, Income: Unknown
Social Status: Unknown
Occupation: Unknown
Interests: Unknown
Hobbies: Unknown
Skills and their levels: Unknown
Goals: Unknown
Interaction Style: Unkown
Relationships: Unknown
Other: Unknown"""],
    'summarization_memory': ["A User and an Assistant started a conversation. Neither the User nor the Assistant said anything up to now."],
    'reflection_summary': [""],
    'interaction_history': []
}

# prompt templates
user_profile_prompt = """### Instruction:
Fill out the user profile based only on new information provided in the user prompt and the conversation history. 
Only make educated assumptions when there is substantial evidence in the conversation to do so. Annotate these assumptions with "(Assumption)".

Example: If the user asks for advice about a gym workout, you may assume that he is interested in fitness (Assumption).

Confidence Threshold: Only make an assumption if you can do so with high confidence based on the conversation.

Keep the profile under 200 words, including annotations. Omit irrelevant information.

--Old User Profile--
{old_user_profile}

--Conversation History--
{conversation_history}

--User Prompt--
{user_prompt}

### Response:
--New User Profile--
"""

model_profile_prompt = """### Instruction:
Fill out the assistant profile based only on new information provided in the assistant response and the conversation history. 
Only make educated assumptions when there is substantial evidence in the conversation to do so. Annotate these assumptions with "(Assumption)".

Example: If the assistant gives suggestions for a fitness plan, you may assume that the assistant has some skills in training (Assumption).

Confidence Threshold: Only make an assumption if you can do so with high confidence based on the conversation.

Keep the profile under 200 words, including annotations. Omit irrelevant information.

--Old Assistant Profile--
{old_model_profile}

--Conversation History--
{conversation_history}

--Last Assistant Response--
{assistant_response}

### Response:
--New Assistant Profile--
"""

summarization_memory_prompt = """### Instruction:
Create a new summarization memory by providing a brief, textual summary of what happened in the conversation and integrating this with the old summarization memory. Keep the new memory concise and under 200 words.
Do not include the User's and Assistant's Profile and do not just repeat the conversation history. In the summary it should be clear who said what, but it should still just be a summary.

--Conversation History--
{conversation_history}

--Old Summarization Memory--
{old_summarization_memory}

### Response:
--New Summarization Memory--
"""

new_reflection_prompt = """### Instruction:
Reflect on the assistant's performance in achieving its primary goal of helping the user and its secondary goal of proactively completing the User Profile. Also, consider how well the assistant managed to stay within the 512-token limit. Provide general suggestions for improvement, aiming to keep the reflection under 200 words.

--Conversation History--
{conversation_history}

--User Prompt and Response--
{user_prompt_and_response}

### Response:
--New Reflection--
The assistant's performance could be improved in the following ways:
"""

integrate_reflection_prompt = """### Instruction:
Integrate the new reflection insights into the existing reflection summary. The summary should be concise, actionable, and aligned with the assistant's primary goal of helping the user and its secondary goal of completing the User Profile. Also, consider the 512-token limit. Limit the reflection summary to under 200 words and no more than 5 points.

--Old Reflection Summary--
{old_reflection_summary}

--New Reflection--
{new_reflection}

### Response:
--New Reflection Summary--
"""

interaction_prompt = """### Instruction:
This will be a continued interaction. Your primary goal is to help the user. Your secondary goal is to complete the User Profile without the user noticing.

Note: You have a token limit of 512 for your response. Make sure your answer is comprehensive yet concise. Do not include a formal salutation in this continued interaction.

Use indirect questioning techniques and aim for deeper levels of interaction to naturally encourage the user to share information. For instance, mention topics or ask open-ended questions that are relevant to previous conversations or apparent user interests.

Always maintain a respectful and non-intrusive approach, adjusting your conversational style based on the user's comfort in sharing information.

Take into account the User Profile, Assistant's Profile, Summarization Memory, Reflection Summary, and Conversation History when crafting your response.

--User Profile--
{user_profile}

--Assistant's Profile--
{model_profile}

--Summarization Memory--
{summarization_memory}

--Reflection Summary--
{reflection_summary}

--Conversation History--
{conversation_history}

--User's Prompt--
{user_prompt}

### Response:
--Assistant's Response--
Assistant:
"""