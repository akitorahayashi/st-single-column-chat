import streamlit as st

st.title("Single Column Chat")

if "history" not in st.session_state:
    st.session_state.history = []

user_input = st.chat_input("メッセージを入力")
if user_input:
    st.session_state.history.append({"role": "user", "content": user_input})
    ai_response = f"AIが返す: {user_input}"  # 自前のAIロジックをここで呼ぶ
    st.session_state.history.append({"role": "assistant", "content": ai_response})

for chat in st.session_state.history:
    if chat["role"] == "user":
        st.chat_message("user").write(chat["content"])
    else:
        st.chat_message("assistant").write(chat["content"])
