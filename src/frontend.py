import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from agent import graph

st.set_page_config(page_title="UFO Bot", page_icon=":robot_face:", layout="wide")

left_col, main_col, right_col = st.columns([1,3,3])
if "message_history" not in st.session_state:
    st.session_state.message_history = [AIMessage(content="I am a UFOologist. Tell me about your UFO sighting.")]

with left_col:
    if st.button("Clear"):
        st.session_state.message_history = []

with main_col:
    user_input = st.chat_input("Ask me anything about UFOs!")
    if user_input:
        # if collection_choice == "FAQs":
        #     related_questions = vector_store.query_faqs(user_input)
        # else:
        #     related_questions = vector_store.query_aliens(user_input)
        st.session_state.message_history.append(HumanMessage(content=user_input))
        response = graph.invoke({"messages": list(st.session_state.message_history)})
        st.session_state.message_history = response["messages"]

    for i in range(1, len(st.session_state.message_history) + 1):
        this_message = st.session_state.message_history[-i]
        if isinstance(this_message, HumanMessage):
            message_box = st.chat_message("user")
        elif isinstance(this_message, AIMessage):
            message_box = st.chat_message("assistant")
        else:
            message_box = st.chat_message("system")
        message_box.markdown(this_message.content)

with right_col:
    st.text(st.session_state.message_history)    
