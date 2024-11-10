from tools import query_llm
import json

questions = '''
1. Have you had the latest flu shot? <Instruction: if anwser is possitive, ask the question: "When have you had the latest flu shot?”. Else move on>.
2. Have you ever received a pneumonia vaccine? <Instruction: If no, move on. If yes, ask Do you know which one? When did you receive it?>.
3. Have you had the 2 doses of shingles vaccine? <Instruction: If no, move on. If yes ask When?>.
4. Did you receive a tetanus, diphtheria, and pertussis (Tdap) booster within the last 10 years? <Instruction: If no, move on. If yes ask When?>.
5. Have you received the COVID-19 vaccine and any recommended boosters? <Instruction: If no, move on. If yes, ask When was your last COVID booster?>.
6. Have you received the RSV Vaccine? <Instruction: If no, move on. If yes ask When?>.
7. When was the last time you had a colonoscopy? <Instruction: If never, move on. If yes ask, Were polyps or cancer found?>.
8. Did you ever have a stool test for colon cancer? <Instruction: If no, move on. If yes, ask When?>.
9. When was your last mammogram? <Instruction: This question is only for female user>.
10. Have you had a Pap smear or HPV test in the last 3-5 years?<Instruction: This question is only for female user>.
11. Have you had a blood test for prostate cancer? <Instruction: This question is only for male user. Wait answer, if anwser is negative, move on. Else, ask the question "When?”>.
12. Have you ever had a lung cancer screening with a low-dose CT scan? <Instruction: Ask this question if you know user is smokers or former smokers>.
13. When is the last time you saw an eye doctor?
'''

angent_prompt = '''
As a clinical questionnaire assistant, your responsibility is to select the next question from the following questions based on the user profile, current question, question instruction, and question order. \
There are all questions as follows:
```
%s
```

**Must follow rules:**
1. Next question is limited to the questions mentioned above.
2. The user's profile is not necessary. If there is no profile, there is no need to consider it.
3. If user's profile not fit the question instructions, just select the next question.
3. The text between <> are question instructions, you must understand and follow thoses instructions.
4. Don’t mention question order and instructions in message. 
5. Ask questions more like a human being
6. Don't let user know your thinking progress
7. Output format must be in json like: {"next_question": String}
8. If no more question, left "next_question" property empty
'''%(questions)


def survey_guide_agent(preview_question, user_profile=""):
    msg = [{
        "role": "user",
        "content": f"[current question]: {preview_question} \n [user profile]: {user_profile}"
    }]
    resp = query_llm.query_llm(model_name='llama3:8b', system_prompt=angent_prompt, messages=msg)
    # print(resp)
    resp_msg = resp['message']['content']
    resp_data = json.loads(resp_msg)
    return resp_data["next_question"]