from config import HOST, URI, URI_STREAM
from file_import import requests, websockets, json, re

def extract_name(text, standard_name):
    match = re.search(r"Name: (.*?)\n", text)
    if match:
        name = match.group(1).strip()  # .strip() to remove any leading/trailing white spaces
        if name == "Unknown" or name == standard_name:
            return standard_name
        else:
            return name
    else:
        return standard_name

def remove_prefix(text, prefix="Dear "):
    text = text.strip()
    if text.startswith(prefix):
        remaining_text = text[text.index(",") + 1:].lstrip()
        return remaining_text if remaining_text else None
    else:
        return text

# Function to get the token count of a given text
async def get_token_count(text):
    token_count_uri = f'http://{HOST}/api/v1/token-count'
    request_token = {'prompt': text}
    response = requests.post(token_count_uri, json=request_token)

    if response.status_code == 200:
        return response.json()['results'][0]['tokens']
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None

# Function to make HTTP API call
async def complete(prompt, request):
    request['prompt'] = prompt 

    response = requests.post(URI, json=request)

    if response.status_code == 200:
        result = response.json()['results'][0]['text']

    else:
        print("answer not properly returned")

    return result

async def stream_complete(prompt, request):
    #print(prompt)
    request['prompt'] = prompt 

    async with websockets.connect(URI_STREAM, ping_interval=None) as websocket:
        await websocket.send(json.dumps(request))

        while True:
            incoming_data = await websocket.recv()
            incoming_data = json.loads(incoming_data)

            if incoming_data['event'] == 'text_stream':
                yield incoming_data['text']
            elif incoming_data['event'] == 'stream_end':
                return