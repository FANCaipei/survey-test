from tools import query_llm

angent_prompt = '''
As a clinical questionnaire assistant, your responsibility is to verify if the answer are expected for user provided question base on user provided expect answer.
If all answers are expected, return 'TRUE', else return 'FALSE'

**output format**:
Boolean value between 'TRUE' and 'FALSE' . No other output accepted
'''


def questionnaire_agent_v2(condition_text):
    print(condition_text)
    print("*****")
    msg = [{
        "role": "user",
        "content": condition_text
    }]
    resp = query_llm.query_llm(model_name='llama3.1:8b', system_prompt=angent_prompt, messages=msg)
    resp_msg = resp['message']['content']
    if 'TRUE' in resp_msg:
        return True
    else:
        return False