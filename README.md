# ReguGenuis-Client-API

This Exposes the finetuned GPT3.5 LLM as A REST service to enable seamless integration without the intricate understanding of the data preprocessing or the LLM prompt interface.

Takes the RASE-tagged rule as Request and returns the Machine-readable JSON generated by the finetuned LLM as Response.


<img width="1151" alt="image" src="https://github.com/Falu-G/ReguGenuis-Client/assets/33534666/edc1dec3-915a-4bec-81a0-2298ae7b47c3">

<img width="1146" alt="image" src="https://github.com/Falu-G/ReguGenuis-Client/assets/33534666/302ca804-4569-4883-a396-eeda2b08ea7a">


# To Interact directly with the model, below is a sample function.

**The model => ft:gpt-3.5-turbo-0613:personal:regugen:8TyfLt5J**

OPENAIKEY api key is required for every prompts

``` python code
def prompt_fm(NLT_Rules):
    # function that submit prompts to model and returns a json rule
    fine_tuned_model_id = "ft:gpt-3.5-turbo-0613:personal:regugen:8TyfLt5J"
    openai.api_key= <OPENAIKEY>
    response = openai.ChatCompletion.create(
    model=fine_tuned_model_id, 
    messages=[
        {"role": "system", "content": "You are an assistant for JSON Generation of Rules"},
        {"role": "user", "content": NLT_Rules}]
    , temperature=0
    )
    fm_res=response["choices"][0]["message"]["content"]
    print(fm_res)
    return fm_res;
```

