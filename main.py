from tools import completion_verify_agent, query_llm, survey_guide_agent, ai_led

def main():
    # print("hey there")
    # resp = query_llm.query_llm(model_name='llama3.2',system_prompt='you are a assistant',messages=[{
    #     "role": "user",
    #     "content": "how can you help me"
    # }])
    # print(resp['message']['content'])

    # completion agent test
    # valid = completion_verify_agent.completion_verify_agent('Have you had the latest flu shot?', "no")
    # print(f"valid: {valid}")

    # survey guide agent test
    # resp = survey_guide_agent.survey_guide_agent('Have you had the latest flu shot?', "")
    # print(resp)

    ai_led.start()


if __name__=="__main__":
    main()