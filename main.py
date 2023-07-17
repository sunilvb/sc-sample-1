import os
import streamlit as st
from langchain.llms import OpenAI, AI21
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SimpleSequentialChain


st.title("GPT and AI21 AI Paraphraser")

col1, col2 = st.columns(2)

with col1:
    gpt_api_key = st.text_input("Enter the ChatGPT API Key")
    gpt_enabed = st.checkbox("enable gpt", key=0)

with col2:
    ai21_api_key = st.text_input("Enter the AI21 API Key")
    ai21_enabled = st.checkbox("enable ai21", key=1)

input_text = st.text_area("Input your Paragraph")

gpt_rewrite_prompt = PromptTemplate(
    input_variables=['input'],
    template="rewrite the paragraph and correcet the grammar mistakes {input}"
)

ai21_rewrite_prompt = PromptTemplate(
    input_variables=['paragraph'],
    template="parphraser the paragraph {paragraph}"
)


if gpt_enabed == True:
    try:
        os.environ['OPENAI_API_KEY'] = gpt_api_key
        llm = OpenAI(temperature=0)
    except:
        pass
elif ai21_enabled == True:
    try:
        os.environ['AI21_API_KEY'] = ai21_api_key
        llm = AI21(temperature=0)
    except:
        pass
try:
    if gpt_enabed == True and ai21_enabled == False:
        chain = LLMChain(llm=llm, prompt=gpt_rewrite_prompt)
        output = chain.run(input_text)
        text = "This is your GPT paraphrased response"
    elif gpt_enabed == False and ai21_enabled == True:
        chain = LLMChain(llm=llm, prompt=ai21_rewrite_prompt)
        output = chain.run(input_text)
        text = "This is your AI21 paraphrased response"
    elif gpt_enabed == True & ai21_enabled == True:
        gpt_chain = LLMChain(llm=llm, prompt=gpt_rewrite_prompt)
        ai21_chain = LLMChain(llm=llm, prompt=ai21_rewrite_prompt)
        chain = SimpleSequentialChain(chains=[gpt_chain, ai21_chain], verbose=True)
        output = chain.run(input_text)
        text = "This is your GPT and AI21 response"
    st.text(text)
    st.text(output)
except:
    pass

