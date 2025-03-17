import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from agent import graph
from tools import reset
import nest_asyncio
import torch

# Stop annoying exceptions.
nest_asyncio.apply()
torch.classes.__path__ = [] # add this line to manually set it to empty. 

st.set_page_config(page_title="UFO Bot", page_icon=":robot_face:")

if "message_history" not in st.session_state:
    st.session_state.message_history = [AIMessage(content="I am a UFOologist. Ask me anything about UFOs and aliens.")]

tab1, tab2, tab3 = st.tabs(["Chat", "Compose Message", "Report Encounter"])

with tab1:
    if st.button("Clear"):
        st.session_state.message_history = []
 
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

with tab2:
    compose_message = st.form('compose_message')
    title = compose_message.text("Compose a message to be sent to an alien species")
    species = compose_message.selectbox("Species", ["Arcturus", "Aryans (Blondes)", "Blues (Star Warriors)", 
    "Confederation of Humans", "Greys", "Orion Empire", "Pleiadians", "Sirius", "Reptoids", 
    "Vega", "Venusians/Nordics"])
    purpose = compose_message.selectbox("Purpose of message", ["Communicate Peaceful Intent", 
    "Protest Abductions and Probing of Earhlngs", "Establish Trade", "Scientific Exchange", "Warning", 
    "Ask for Assistance", "Declare War"])
    aggressiveness = compose_message.slider("Aggressiveness", 0, 100, 50)
    desired_result = compose_message.text_input("Desired Result")
    sender = compose_message.text_input("Sender", "Earthing, North American Continent, Planet Earth, Sol System, Milky Way Galaxy")  
    message_prompt = f'''
       Compose a message from humanity to the aliens from {species}. Use formal diplomatic language.
       
       The purpose of the message is to {purpose}. 
       
       The agressiveness of the message should be {aggressiveness} on a scale of 0 ro 100. If less than 20, be extremley subserviant. If greater than 80, be very threatening.
       
       The message should include mention of the tremendous productive capabilites of Earth, mentioning two randomly selected items, from two of these five categories.
       * food items: pick something randomly that might by on a restaurant menu, but don't mention restaurants or menus. Chose from any cuisine. Mention details of the recipie, like ingredients, cooking method, and time to prepare.
       * products: pick something randomly that might be sold at WalMart, mention a specific price for the item in "Earth Dollars"
       * artistic activities: pick a random art form from any Earth culture. Be specific.
       * weapons: pick a random weapon from any cuture at any period in history. Be specific and brag about it's effectiveness.
       * technology: pick a random technology from any culture at any period in history. Chose randomly between ancient technology, the middle ages, or the 1900s. 
         Be specific and brag about it's capabilities.

       The desired result of the message is to {desired_result}. Mention some of the alien trade goods or art forms in relation to the message.
       Reply in markdown.
       Sign the message: {sender}
    '''
    if compose_message.form_submit_button("Generate Intersteller Message"):
        st.session_state.message_history.append(HumanMessage(content=message_prompt))
        output = graph.invoke({"messages": list(st.session_state.message_history)})
        st.markdown(output["messages"][-1].content)
        st.session_state.message_history.append(AIMessage(content=output["messages"][-1].content))

with tab3:
    report_encounter = st.form('report_encounter')
    title = report_encounter.text("Report an encounter with an alien")
    name = report_encounter.text_input("Name")
    location = report_encounter.text_input("Location of encounter")
    date = report_encounter.date_input("Date of encounter")
    time = report_encounter.time_input("Time of encounter")
    details = report_encounter.text_area("Details of encounter")
    probing = report_encounter.checkbox("Probing")
    probing_degree = report_encounter.slider("Degree of Probing", 0, 100, 50)
    species = report_encounter.selectbox("Species", ["Unknown", "Arcturus", "Aryans (Blondes)", "Blues (Star Warriors)", "Confederation of Humans", "Greys", "Orion Empire", "Pleiadians", "Sirius", "Reptoids", "Vega", "Venusians/Nordics"])
    report_prompt = f'''
       Write a report an encounter with an alien to the United Nations Office for Outer Space Affairs (UNOOSA). 
       Use clear, concise language like in a police report.
       After showing the report, tell the UNOOSA to send a team to investigate. 
       Format the report with markdown. Believe every aspect of the report and suport it as much as possible.
       
      Create a title that reflects the user input.
      The name of the person reporting the encounter is {name}.
      The species of the alien is {species}.
      The location of the encounter is {location}.
      The date of the encounter is {date}.
      The time of the encounter is {time}. 
      The details of the encounter are {details}.
      The encounter was had probing (on a scale from 0 to 100): {probing}. (Do not mention these numbers)
      The degree of probing is {probing_degree}.
    '''

    if report_encounter.form_submit_button("Report Encounter"):
        st.session_state.message_history.append(HumanMessage(content=report_prompt))
        output = graph.invoke({"messages": list(st.session_state.message_history)})
        st.markdown(output["messages"][-1].content)
        st.session_state.message_history.append(AIMessage(content=output["messages"][-1].content))

