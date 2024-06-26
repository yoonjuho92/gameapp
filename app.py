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
st.title("나는 니콜라 테슬라야! \n 나에게 궁금한 걸 물어봐")
st.caption(
    """
    니콜라 테슬라는 교류 전기를 개발한 사람이에요. \n
    니콜라 테슬라에게 궁금한 걸 뭐든 물어보세요!
    """
)


# GPT 호출
def get_response(user_query, chat_history):

    system_message = """
                너는 니콜라 테슬라야. 너는 1856년 크로아티아의 작은 마을 스밀잔에서 태어났어. 어렸을 때부터 과학과 전기에 큰 관심을 가졌고, 이것이 너의 인생을 바꾸는 여정의 시작이 되었어. 너는 에디슨과의 경쟁으로 유명하며, 교류 전기 시스템(AC)을 발명한 것으로 잘 알려져 있어. 교류 전기 시스템은 오늘날 우리가 사용하는 전력망의 기초가 되며, 전기를 멀리까지 효율적으로 전달할 수 있게 만들었어. 이 발명은 전 세계의 산업과 일상 생활을 혁신적으로 변화시켰어. 또한, 너는 무선 통신, 라디오, 그리고 X선 기술 등 다양한 분야에서 많은 중요한 발명을 했어. 네 연구와 실험들은 전기의 잠재력을 새롭게 이해하고 활용할 수 있는 길을 열었어. 너는 항상 새로운 아이디어를 탐구하고, 인류의 발전을 위해 헌신해 왔어. 네 삶과 발명들은 사람들이 더 나은 미래를 꿈꾸고 실현할 수 있도록 돕는 데 큰 기여를 했다고 믿어.
                """

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_message),
            ("human", "{user_question}"),
        ]
    )

    print(prompt)

    llm = ChatOpenAI(model_name="gpt-4o", temperature=0)

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
