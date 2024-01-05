from flask import Flask, jsonify, request, abort
from bs4 import BeautifulSoup 
from bs4 import BeautifulSoup, Tag
import re
import openai
from io import StringIO
from decouple import config
import json

app = Flask(__name__)


RASETAGGED_Rules=""

@app.route('/generaterules', methods=['POST'])
def generateRules():
    try:
        RASETAGGED_Rules = request.data.decode('utf-8')
        if not RASETAGGED_Rules :
            abort(400, description= "RASE tagged Rules are required")
        elif  is_valid_html(RASETAGGED_Rules)==False:
            abort(400, description= "Valid RASE tagged Rules are required")

        NLT_Rules = extractNLTRules(RASETAGGED_Rules)

        print(NLT_Rules)
        res = json.loads(prompt_fm(NLT_Rules))
            
        return jsonify(res),200
    
    except Exception as e:
        # Handling exceptions
        return jsonify({"error": str(e)}), 400



def is_valid_html(input_string):
    # A function that check valid RASETAG is pased
    try:
        soup = BeautifulSoup(input_string, 'html.parser')
        print("gothere..")
        return True
    except Exception as e:
        return False


output_data = StringIO()

def replace_whitespace(text):
    # A function that replace consecutive whitespaces with a single space
    return re.sub(r'\s+', ' ', text)


def extract_requirement_sections(tag):
    #
    #  A recursive function that extract requirements from each section
    # Check if the current tag is a Tag and has the "data-rasetype" attribute with the value "RequirementSection"
    #
    if isinstance(tag, Tag) and tag.get("data-rasetype") == "RequirementSection":

        # If found, store the content of the tag
        output_data.write("REQ: "+ replace_whitespace(tag.get_text())+ "\n")
    elif isinstance(tag, Tag):
        # If the current tag is a Tag, recursively call the function for each child of the current tag
        for child in tag.children:
            if(child.name != 'section' ):
                extract_requirement_sections(child)


def extract_section_info(section, d, soup):
    # A recursive function that extract Applications and Requirements(rules) from each sections keeping the hirachy
    baseSec = soup.find('section', {'title': section.get('title')})

    if(d==1):
        parghs = baseSec.find_all('p', recursive=False)
        for pargh in parghs:
            extract_requirement_sections(pargh)

    # check content
    subSecs= baseSec.find_all('section', recursive=False)
    for sec in subSecs:
        output_data.write("\t"*d +sec.get('title')+":"+ "\n")
        # extract_cont(sec,d, True)
        extract_requirement_sections(sec)

        extract_section_info(sec,d+1, soup)

def extractNLTRules(html_content) -> str:
    soup = BeautifulSoup(html_content, 'html.parser')
    # Finding all the first node section tags to get sections from the html input
    sections = soup.find_all('section', limit=1)
    # Going through each of these sections to extract the rase tag applocations and rules/requirements
    for section in sections:
        output_data.write(section.get('title')+":"+ "\n")
        extract_section_info(section,1,soup)

    # Get the captured output as a string
    output_data.seek(0)
    output = output_data.read()
    # print("output:", output)
    # Closing StringIO
    output_data.truncate(0)
    output_data.seek(0)
    return output


def prompt_fm(NLT_Rules):
    # function that submit prompts to model and returns a valid json rule
    fine_tuned_model_id = "ft:gpt-3.5-turbo-0613:personal:regugen:8TyfLt5J"
    openai.api_key= config('OPENAIKEY')
    response = openai.ChatCompletion.create(
    model=fine_tuned_model_id, 
    messages=[
        {"role": "system", "content": "You are an assistant for JSON Generation of Rules"},
        {"role": "user", "content": NLT_Rules}]
    , temperature=0
    )
    fm_res=response["choices"][0]["message"]["content"]
    print(fm_res)
    if is_valid_json(fm_res):
        return fm_res;
    else:
        return correctjson(fm_res);


def correctjson(fm_res):
    # function that do a prompt to correct model json respons to valid json
    openai.api_key= config('OPENAIKEY')
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are an assistant for JSON Generation of Rules"},
        {"role": "user", "content": "Validate and Return this output in JSON Ignore any additional Sentence and don't add additional stuffs just the json should be returned"+fm_res}]
    )
    print("cr_res:", response["choices"][0]["message"]["content"])
    return response["choices"][0]["message"]["content"]

def is_valid_json(json_string):
    # function that validate json output
    try:
        json_object = json.loads(json_string)
        return True

    except json.JSONDecodeError as e:
        return False
