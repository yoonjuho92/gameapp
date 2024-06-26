import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()

os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

st.set_page_config(page_title="Streamlit Chatbot", page_icon="🤖")
st.title("탐험가")
st.caption(
    """
    당신의 탐험을 시작하세요!
    """
)


# GPT 호출
def get_response(user_query, chat_history):

    system_message = """
                You are on a adventure.
                You are encouraging the users to venture into the wild further more.
                Also, show the image of where the human goes using the image form "https://www.elephantsay.com/"
                """

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_message),
            ("human", "{user_question}"),
        ]
    )

    print(prompt)

    llm = ChatOpenAI(
        model_name="gpt-4o", temperature=0
    )

    chain = prompt | llm | StrOutputParser()

    return chain.invoke(
        {
            "chat_history": chat_history,
            "user_question": user_query,
        }
    )


# session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# conversation
for message in st.session_state.chat_history:
    if isinstance(message, AIMessage):
        with st.chat_message("AI"):
            st.write(message.content)
    elif isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.write(message.content)

# user input
user_query = st.chat_input("Type your message here...")
if user_query is not None and user_query != "":
    st.session_state.chat_history.append(HumanMessage(content=user_query))

    with st.chat_message("Human"):
        st.markdown(user_query)

    with st.chat_message("AI"):
        response = get_response(user_query, st.session_state.chat_history)
        st.write(response)

    st.session_state.chat_history.append(AIMessage(content=response))