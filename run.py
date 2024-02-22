import openai
import streamlit as st
import time
from captcha.image import ImageCaptcha
import random


messages_counter = 0
assistant_id = "asst_MsTwpSRZ5bIyEmIZ6mMDh8wW"

client = openai

if "chat_pilli" not in st.session_state:
    st.session_state['chat_pilli'] = False
if "chat_self" not in st.session_state:
    st.session_state['chat_self'] = False
if "thread_id" not in st.session_state:
    st.session_state.thread_id = None
if "messages_counter" not in st.session_state:
    st.session_state.messages_counter = 0


st.set_page_config(page_title="my girlfriend", page_icon=":speech_balloon:")

# openai.api_key = "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"
openai.api_key = st.secrets["API_KEY"]



st.title(":)")
st.write("Message from Pilli: Put yourself in my shoe and convince her if you can.")


if st.button("Talk to the 😈"):
    captcha = ImageCaptcha()
    # data = captcha.generate('1234')
    # print(data)
    codever = random.randrange(1, 10**4)
    captcha.write(str(codever), 'out.png')
    st.image('out.png')
    st.text_input('Enter the captcha', value='', key=12)

    def submit():
        cap_text = st.session_state[12]
        print(codever == cap_text)
        if str(str(codever) == str(cap_text)):
            st.session_state.chat_pilli = True
            thread = client.beta.threads.create()
            st.session_state.thread_id = thread.id

    st.button('Submit', on_click=submit)


    

# if st.button("Chat as Yourself 😈"):
#     st.session_state.chat_self = True
#     thread = client.beta.threads.create()
#     st.session_state.thread_id = thread.id
    

if st.sidebar.button("I am done, Bye Bye!!"):
    st.session_state.messages = []  # Clear the chat history
    st.session_state.chat_pilli = False  # Reset the chat state
    st.session_state.chat_self = False  # Reset the chat state
    st.session_state.thread_id = None

# st.sidebar.caption("I love to create entertaining apps like this. I am a student and constraint by resources. A Euro can make a difference. Thanks.")

# url = "https://www.paypal.com/donate/?hosted_button_id=TSRDAVJKRUE8J"
# st.sidebar.link_button("PayPal Donate", url)
# url = "https://revolut.me/spilliire"
# st.sidebar.link_button("Revolut Donate", url)
# st.sidebar.image("revolut.jpg")


if st.session_state.chat_pilli:
    if "openai_model" not in st.session_state:
        st.session_state.openai_model = "gpt-3.5-turbo"
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # st.chat_message("user", avatar="😇")
    # st.chat_message("assistant", avatar="👩")

    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar="⚫"): 
            st.markdown(message["content"])
        

    if prompt := st.chat_input("hi, how is your day?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="😇"):
            st.markdown(prompt)

        client.beta.threads.messages.create(
                thread_id=st.session_state.thread_id,
                role="user",
                content=prompt
            )
        
        run = client.beta.threads.runs.create(
            thread_id=st.session_state.thread_id,
            assistant_id=assistant_id,
            instructions="Act as my girlfriend.\
            Behave like a nagging girlfriend. \
            Give some irritated emojis.\
            Have a personality type of passive-aggressive or negativistic.\
            Bring any situation and start nagging about it.\
            Talking moderately short sentences.\
            correct the grammar.\
            have a lot of conversation"
            # Nag him till he finds out that you want ice cream\
            # rule: don't say the word ice cream"
            # if he asks for ice cream say I love you and quit." 
        )

        while run.status != 'completed':
            time.sleep(1)
            run = client.beta.threads.runs.retrieve(
                thread_id=st.session_state.thread_id,
                run_id=run.id
            )
        messages = client.beta.threads.messages.list(
            thread_id=st.session_state.thread_id
        )

        

        # Process and display assistant messages
        assistant_messages_for_run = [
            message for message in messages 
            if message.run_id == run.id and message.role == "assistant"
        ]
        st.session_state.messages_counter += len(assistant_messages_for_run)
        print(st.session_state.messages_counter)

        if st.session_state.messages_counter > 10:
            st.session_state.messages = []  # Clear the chat history
            st.session_state.chat_pilli = False  # Reset the chat state
            st.session_state.thread_id = None
            #save messages and thread here.

        for message in assistant_messages_for_run:
            st.session_state.messages.append({"role": "assistant", "content": message.content[0].text.value})
            with st.chat_message("assistant", avatar="👩"):
                st.markdown(message.content[0].text.value)
# elif st.session_state.chat_self:
#     if "openai_model" not in st.session_state:
#         st.session_state.openai_model = "gpt-3.5-turbo"
#     if "messages" not in st.session_state:
#         st.session_state.messages = []
    
#     for message in st.session_state.messages:
#         with st.chat_message(message["role"]):
#             st.markdown(message["content"])

#     if prompt := st.chat_input("hi, how is your day?"):
#         st.session_state.messages.append({"role": "user", "content": prompt})
#         with st.chat_message("user"):
#             st.markdown(prompt)

#         client.beta.threads.messages.create(
#                 thread_id=st.session_state.thread_id,
#                 role="user",
#                 content=prompt
#             )
        
#         run = client.beta.threads.runs.create(
#             thread_id=st.session_state.thread_id,
#             assistant_id=assistant_id,
#             instructions="Act as Stephen's girlfriend.\
#             Behave like a nagging girlfriend. \
#             Give some irritated emojis.\
#             Have a personality type of passive-aggressive or negativistic.\
#             Bring any situation and start nagging about it.\
#             Talking moderately short sentences.\
#             correct the grammar\
#             you are talking to a common friend, so complain about Stephen.\
#             Information about stephen:\
#             Stephen is into engages in deep conversations.\
#             Stephen is into sports \
#             Stephen introverted sometimes.\
#             complain about stephen." 
#         )

#         while run.status != 'completed':
#             time.sleep(1)
#             run = client.beta.threads.runs.retrieve(
#                 thread_id=st.session_state.thread_id,
#                 run_id=run.id
#             )
#         messages = client.beta.threads.messages.list(
#             thread_id=st.session_state.thread_id
#         )

#         # Process and display assistant messages
#         assistant_messages_for_run = [
#             message for message in messages 
#             if message.run_id == run.id and message.role == "assistant"
#         ]
#         for message in assistant_messages_for_run:
#             st.session_state.messages.append({"role": "assistant", "content": message.content[0].text.value})
#             with st.chat_message("assistant"):
#                 st.markdown(message.content[0].text.value)
else:
    st.write("Let's see.")