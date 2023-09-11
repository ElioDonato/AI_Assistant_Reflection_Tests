# API configurations
HOST = 'localhost:5000'
URI = f'http://{HOST}/api/v1/generate'
HOST_STREAM = 'localhost:5005'
URI_STREAM = f'ws://{HOST_STREAM}/api/v1/stream'
MAX_TOKENS = 512
TRUNCATION_LENGTH = 8192
custom_end = ["</s><s>", "</s>", "###", "--"]
request = {
    'prompt': '',
    'max_new_tokens': MAX_TOKENS,
    'auto_max_new_tokens': False,
    'preset': 'None',
    'do_sample': True,
    '_continue': False,
    'temperature': 0.2,
    'top_p': 0.95,
    'typical_p': 1,
    'epsilon_cutoff': 0,
    'eta_cutoff': 0,
    'tfs': 1,
    'top_a': 0,
    'repetition_penalty': 1,
    'repetition_penalty_range': 0,
    'top_k': 50,
    'min_length': 0,
    'no_repeat_ngram_size': 0,
    'num_beams': 1,
    'penalty_alpha': 0,
    'length_penalty': 1,
    'early_stopping': False,
    'mirostat_mode': 0,
    'mirostat_tau': 5,
    'mirostat_eta': 0.1,
    'guidance_scale': 1,
    'negative_prompt': '',
    'seed': -1,
    'add_bos_token': True,
    'truncation_length': TRUNCATION_LENGTH,
    'ban_eos_token': False,
    'skip_special_tokens': True,
    'stopping_strings': custom_end
}