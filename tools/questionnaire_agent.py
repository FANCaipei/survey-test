from tools import query_llm

angent_prompt = '''
As a clinical questionnaire assistant, your responsibility is to decide if should ask the question based on the user profile and question condition.

**Must follow rules:**
1. if condition is "true" or "True", always return 'TURE'

**output format**:
Boolean value between 'TRUE' and 'FALSE' . No other output accepted
'''


def questionnaire_agent(question, condition, user_profile=""):
    msg = [{
        "role": "user",
        "content": f"[question]: {question} \n [condition]: {condition} \n[user profile]: {user_profile}"
    }]
    resp = query_llm.query_llm(model_name='llama3:8b', system_prompt=angent_prompt, messages=msg)
    resp_msg = resp['message']['content']
    if 'TRUE' in resp_msg:
        return True
    else:
        print(f"question should not ask: {question}")
        return False