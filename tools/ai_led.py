from tools import completion_verify_agent, survey_guide_agent, profile_generate_agent, questionnaire_agent
import json
import asyncio

questions = []
with open('./questions.json') as f:
    questions = json.load(f)

temp_db = {}

def generate_next_question(question, answer, uid):
    is_answer_valid = completion_verify_agent.completion_verify_agent(question, answer)
    if is_answer_valid:
        append_msg(question, answer, uid)
        next_question = survey_guide_agent.survey_guide_agent(preview_question=question,user_profile=temp_db[uid]["profile"])
        if len(next_question) > 0:
            return next_question
        else:
            return 'Finished' 
    else:
        return question

def append_msg(question, answer, uid):
    # TODO: store in database
    if uid not in temp_db:
        temp_db[uid] = {"messages": [], "profile": ''}
    temp_db[uid]["messages"].append({
        "role": "user",
        "content": f"[question:] {question} [answer]: {answer}"
    })
    # temp append to profile
    temp_db[uid]["profile"] += f"[question]:{question}, [user answer]: {answer}\n"
    print("=======================")
    print(f"profile: \n{temp_db[uid]['profile']}")
    print("=======================")
    # asyncio.run(update_user_profile(uid))

async def update_user_profile(uid):
    profile = profile_generate_agent.profile_generate_agent(temp_db[uid]["messages"])
    temp_db[uid]["profile"] = profile

def start():
    uid = 'test'
    current_question_index = 0
    repeat_asked_question = False
    while current_question_index < len(questions):
        q_item = questions[current_question_index]

        u_profile = ""
        if uid in temp_db:
            if "profile" in temp_db[uid]:
                u_profile = temp_db[uid]["profile"]

        should_ask = True if repeat_asked_question is True else questionnaire_agent.questionnaire_agent(question=q_item['question'], condition=q_item['condition'], user_profile=u_profile)
        if not should_ask:
            current_question_index += 1
            repeat_asked_question = False
            continue
        else:
            answer = input(f"{q_item['question']} \n")
            is_answer_valid = completion_verify_agent.completion_verify_agent(q_item['question'], answer)
            if is_answer_valid:
                append_msg(question=q_item['question'], answer=answer,uid=uid)
                current_question_index += 1
                repeat_asked_question = False
            else:
                repeat_asked_question = True
                continue

    # current_question = "Have you had the latest flu shot?"
    # while current_question != 'Finished':
    #     answer = input(f"Question: {current_question} \n")
    #     current_question = generate_next_question(question=current_question, answer=answer, uid=uid)