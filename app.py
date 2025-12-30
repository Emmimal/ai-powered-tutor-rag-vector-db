import streamlit as st
# ... (imports from above)

st.title("Your Personal AI Tutor")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask me anything about the subject!"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = chain.stream(prompt)
        full_response = st.write_stream(response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})
