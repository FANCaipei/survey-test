from tools import query_llm

angent_prompt = '''
    Your response is to summary user's medical profile based on questions and answers.
    **Must follow rules**:
    1. The profile must be concise
    2. No explanation is needed, just output profile
'''
def profile_generate_agent(messages):
    resp = query_llm.query_llm(model_name='llama3.1:8b', system_prompt=angent_prompt, messages=messages)
    resp_msg = resp['message']['content']
    print(f"profile: {resp_msg}")
    return resp_msg