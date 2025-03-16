import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from agent import graph
from tools import reset
import nest_asyncio
import torch

# Stop annoying exceptions.
nest_asyncio.apply()
torch.classes.__path__ = [] # add this line to manually set it to empty. 

st.set_page_config(page_title="UFO Bot", page_icon=":robot_face:", layout="wide")

left_col, main_col, right_col = st.columns([1,3,3])
if "message_history" not in st.session_state:
    st.session_state.message_history = [AIMessage(content="I am a UFOologist. Ask me anything about UFOs and aliens.")]

with left_col:
    if st.button("Clear"):
        st.session_state.message_history = []
 
with main_col:
    user_input = st.chat_input("Ask me anything about UFOs!")
    if user_input:
        # Get the user input and append it to the list of messages.
        st.session_state.message_history.append(HumanMessage(content=user_input))
        # Invoke the LLM.
        response = graph.invoke({"messages": list(st.session_state.message_history)})
        # The response contains the full history, so can replace the current message_history.
        st.session_state.message_history = response["messages"]

    # Show the message history in reverse order (most recent at the top.)
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
    compose_message = st.form('compose_message')
    title = compose_message.text("Compose a message to be sent to an alien species")
    species = compose_message.selectbox("Species", ["Arcturus", "Aryans (Blondes)", "Blues (Star Warriors)", "Confederation of Humans", "Greys", "Orion Empire", "Pleiadians", "Sirius", "Reptoids", "Vega", "Venusians/Nordics"])
    purpose = compose_message.selectbox("Purpose of message", ["Communicate Peaceful Intent", "Establish Trade", "PScientific Exchange", "Warning", "Ask for Assistance", "Declare War"])
    aggressiveness = compose_message.slider("Aggressiveness", 0, 100, 50)
    submit = compose_message.form_submit_button("Generate Intersteller Message")
    extra_prompt = '''
       Compose a message from humanity to the aliens from Arcturus. Use formal diplomatic language.
       
       The purpose of the message is to Establish Trade. The agressiveness of the message should be high. 
       The message should include mention of how our excellent sausagesm, and very nice submarines would be very popular there, and how we would enjoy their fine house-siced snuff-boxes, and wonderful silent singing performances on Earth.

       Sign the message: Edward Hartnett, UFOologist, North American Continent, Planet Earth, Sol System, Milky Way Galaxy
    '''
    st.session_state.message_history.append(HumanMessage(content=extra_prompt))
    output = graph.invoke({"messages": list(st.session_state.message_history)})
    st.text(output["messages"][-1].content)
    st.session_state.message_history.append(AIMessage(content=output["messages"][-1].content))
if submit:
    st.text("Output")

