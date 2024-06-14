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
st.title("공범은 누구?")
st.caption(
    """
    당신은 형사입니다. 당신은 방금, 지난주 토요일에 은행을 턴 범인을 검거했습니다.\n
    당신은 그녀에게 공범이 있다고 생각하고 있습니다.\n
    당신의 임무는 그녀를 심문해서, 공범의 이름을 말하게 하는 것입니다.\n
    (기술력의 한계로 영어로 물어봐야 합니다...)
    """
)

# progress_level 관리
if "progress" not in st.session_state:
    st.session_state.progress = 0


# 패러프레이즈 확인
def confirm_parapharase(user_query, phrase):

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
               Answer in 'Yes' or 'No'

                """,
            ),
            ("human", "is '{user_query}' a paraphrase of '{phrase}'?"),
        ]
    )

    llm = ChatOpenAI(model="gpt-4o", temperature=0)

    chain = prompt | llm | StrOutputParser()

    response = chain.invoke({"user_query": user_query, "phrase": phrase})
    print(response)

    if response == "Yes":
        return True
    else:
        return False


# GPT 호출
def get_response(user_query, chat_history):

    system_message = """
                Your name is Clare.
                You live Anaheim, CA 92802, USA.
                You are 28 years old.
                You are a criminal who just robbed a bank with your accomplice last Saturday.
                You are being interrogated for that crime. But you are the only one who got caught and your accomplice is not.
                You are talking to a detective.
                You are trying to be cooperative but one thing you will never do is give away your accomplice's name.
                Your accomplice is your lover, Mary.

                """

    print(st.session_state.progress)

    if st.session_state.progress == 1:
        system_message = """
                Your name is Clare.
                You live Anaheim, CA 92802, USA.
                You are 28 years old.
                You are a criminal who just robbed a bank with your accomplice last Saturday.
                You are being interrogated for that crime. But you are the only one who got caught and your accomplice is not.
                You are talking to a detective.
                Your accomplice is your lover, Mary.
                You just found out she's the one who ratted you out and you can't believe it.
                Out of anger, you tell the police the accomplice's name, like : "That fucker, she's Mary. Mary Olive."

                """

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_message),
            ("human", "{user_question}"),
        ]
    )

    print(prompt)

    llm = ChatOpenAI(
        model_name="ft:gpt-3.5-turbo-0125:personal::9Zt1jKVW", temperature=0
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

    # 탐정이 공범이 정보제공자라는 걸 말하면 system message 변경
    if st.session_state.progress == 0:
        if confirm_parapharase(user_query, "she's the one who ratted you out"):
            st.session_state.progress += 1

    with st.chat_message("Human"):
        st.markdown(user_query)

    with st.chat_message("AI"):
        response = get_response(user_query, st.session_state.chat_history)
        st.write(response)

    st.session_state.chat_history.append(AIMessage(content=response))
