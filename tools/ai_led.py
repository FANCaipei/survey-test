from tools import completion_verify_agent, survey_guide_agent, profile_generate_agent
import asyncio

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
    temp_db[uid]["profile"] += f";{question}: {answer}"

    # asyncio.run(update_user_profile(uid))

async def update_user_profile(uid):
    profile = profile_generate_agent.profile_generate_agent(temp_db[uid]["messages"])
    temp_db[uid]["profile"] = profile

def start():
    uid = 'test'
    current_question = "Have you had the latest flu shot?"
    while current_question != 'Finished':
        answer = input(f"{current_question} \n")
        current_question = generate_next_question(question=current_question, answer=answer, uid=uid)