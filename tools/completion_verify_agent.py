from tools import query_llm

angent_prompt = '''
    User will send you a question with it’s answer.
    The conversation will be limited in medical domain.
    Your response is to verify if question has been completed and clearly answered.
    **output format**:
    Boolean value between ‘TRUE’ and ‘FALSE’ . No other output accepted
'''
def completion_verify_agent(question,answer):
    msg = [{
        "role": "user",
        "content": f"[question]: {question} \n [answer]: {answer}"
    }]
    resp = query_llm.query_llm(model_name='llama3.1:8b', system_prompt=angent_prompt, messages=msg)
    resp_msg = resp['message']['content']
    if 'TRUE' in resp_msg:
        return True
    else:
        print('completion check not passed')
        return False