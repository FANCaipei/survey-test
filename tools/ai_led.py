from tools import completion_verify_agent, survey_guide_agent, profile_generate_agent, questionnaire_agent,questionnaire_agent_v2
import json
import asyncio

questions = []
with open('./questions.json') as f:
    questions = json.load(f)

temp_db = {}

# def generate_next_question(question, answer, uid):
#     is_answer_valid = completion_verify_agent.completion_verify_agent(question, answer)
#     if is_answer_valid:
#         append_survey(question, answer, uid)
#         next_question = survey_guide_agent.survey_guide_agent(preview_question=question,user_profile=temp_db[uid]["profile"])
#         if len(next_question) > 0:
#             return next_question
#         else:
#             return 'Finished' 
#     else:
#         return question

def append_survey(question_id, question, answer, uid):
    # TODO: store in database
    if uid not in temp_db:
        temp_db[uid] = {"survey": []}
    temp_db[uid]["survey"].append({
        "id": question_id,
        "question": question,
        "answer": answer
    })
    print("=======================")
    print(f"current survey: \n{temp_db[uid]['survey']}")
    print("=======================")

async def update_user_profile(uid):
    profile = profile_generate_agent.profile_generate_agent(temp_db[uid]["survey"])
    temp_db[uid]["profile"] = profile

def find_target_question_in_user_history(uid, question_id):
    if uid in temp_db:
        if "survey" in temp_db[uid]:
            return next((item for item in temp_db[uid]["survey"] if item['id'] == question_id), None)
    return None

def should_ask_the_question(question_item, uid):
    if "conditions" not in question_item:
        return True
    
    # generate condition based question answers
    condition_base_text = ''
    for cond in question_item['conditions']:
        expected_answer_text = cond['expected_answer']
        base_question = find_target_question_in_user_history(uid, cond['condition_question_id'])
        if base_question is not None:
            condition_base_text += f"[question]:{base_question['question']},[answer]:{base_question['answer']},[expected]:{expected_answer_text}\n"
    
    if len(condition_base_text) <= 0:
        # means no base questions base questions has been asked, so should not ask this question
        return False
    
    return questionnaire_agent_v2.questionnaire_agent_v2(condition_base_text)


def start():
    uid = 'test'
    current_question_index = 0
    repeat_asked_question = False
    while current_question_index < len(questions):
        q_item = questions[current_question_index]

        should_ask = True if repeat_asked_question is True else should_ask_the_question(q_item, uid)
        if not should_ask:
            current_question_index += 1
            repeat_asked_question = False
            print(f"should not ask question: {q_item['question']}")
            continue
        else:
            answer = input(f"{q_item['question']} \n")
            is_answer_valid = completion_verify_agent.completion_verify_agent(q_item['question'], answer)
            if is_answer_valid:
                append_survey(question_id=q_item['id'] ,question=q_item['question'], answer=answer,uid=uid)
                current_question_index += 1
                repeat_asked_question = False
            else:
                repeat_asked_question = True
                continue

    # current_question = "Have you had the latest flu shot?"
    # while current_question != 'Finished':
    #     answer = input(f"Question: {current_question} \n")
    #     current_question = generate_next_question(question=current_question, answer=answer, uid=uid)