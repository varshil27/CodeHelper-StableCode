import streamlit as st
from htmltemp import css, bot_template, user_template
import os
import requests




def userinput_llmoutput(user_question):
    url = "http://localhost:5000/instruct"
    objj = {"input":user_question}
    data = requests.post(url, json = objj)
    res = data.json()
    print(data)
    req = res["code"]
    index = req.index("### Response: ")
    req = req[index+14:]
    print(req)
    st.write(user_template.replace(
                "{{MSG}}", user_question), unsafe_allow_html=True)
    st.write(bot_template.replace(
                "{{MSG}}", st.code(req)), unsafe_allow_html=True)


def main():
    st.set_page_config(page_title="StableCode",
                       page_icon=":books:")
    st.write(css, unsafe_allow_html=True)


    st.header("Ask this bot any coding questions :robot_face:")
    user_question = st.text_input("Ask a question:")
    if user_question:
        userinput_llmoutput(user_question)


if __name__ == '__main__':
    main()
