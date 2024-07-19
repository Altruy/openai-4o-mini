from openai import OpenAI 
import base64
import streamlit as st
from io import BytesIO
from PIL import Image

def getResponse(prompt):
    if len(prompt) < 10:
        raise Exception("The prompt is too short, Please enter more than 10 Characters")

    with st.spinner("Getting response..."):
        response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=300,
        )
        rsp = response.choices[0].message.content
        print('text completino',rsp)
    return rsp

def getImageRespone(prompt,base64_image):
    # return "Image to text"
    if len(prompt) < 10:
        raise Exception("The prompt is too short, Please enter more than 10 Characters")
    with st.spinner("Getting response..."):
        response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {
                "type": "image_url",
                "image_url": {
                    "url":  f"data:image/jpeg;base64,{base64_image}",
                },
                },
            ],
            }
        ],
        max_tokens=300,
        )
        rsp = response.choices[0].message.content
        print('image completion',rsp)
    return rsp


def clar_chat():
    del st.session_state["messages"]


st.title("OpenAI Chatbot")
st.caption("A chatbot Using OpenAI 4o-mini")

@st.experimental_fragment
def stre():
    con = st.container(height=450,border=True)
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]
        con.chat_message("assistant").write("How can I help you?")
    else:
        for msg in st.session_state.messages:
            con.chat_message(msg["role"]).write(msg["content"])
    

    with st.form("response",clear_on_submit=True):

        prompt = st.text_input("Enter Your Prompt")

        uploaded_file = st.file_uploader("Upload Your file")
        if uploaded_file is not None:
            bytes_data = uploaded_file.getvalue()
            image = Image.open(BytesIO(bytes_data))
            output_file = 'images/output_image.jpg'
            image.save(output_file, 'JPEG')
            b64 = base64.b64encode(bytes_data)
            base64_string = b64.decode("ascii") 
        else: base64_string = ""


        submitted = st.form_submit_button("Submit",)
        if submitted:
            st.session_state.messages.append({"role": "user", "content": prompt})
            con.chat_message("user").write(prompt)
            
            if uploaded_file is None:
                response = getResponse(prompt)
            else:
                response = getImageRespone(prompt, base64_string)
            msg = response
            st.session_state.messages.append({"role": "assistant", "content": msg})
            con.chat_message("assistant").write(msg)


if "api_key" in st.session_state:
    client = OpenAI(api_key=st.session_state["api_key"])
    stre()
else:
    st.write("Please Add your OpenAi API Key")


cola, colb = st.columns([0.8,0.2])
colb.button("Clear Chat",on_click=clar_chat)
with cola.expander("API Key"):
    key = st.chat_input("Enter Your OpenAi API Key")
    if key is not None:
        if len(key.strip()) > 1:
            st.session_state["api_key"] = key
            client = OpenAI(api_key=key)
