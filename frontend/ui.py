import streamlit as st
import requests

st.set_page_config(page_title="Hybrid Search Chat", layout="wide")

st.sidebar.title("Navigation")
tab = st.sidebar.radio("Choose a tab", ["➕ Add Post", "💬 Search Chat"])

API_URL = "http://127.0.0.1:8000/api"

if tab == "➕ Add Post":
    st.title("Add a New Post")
    title = st.text_input("Post Title")
    content = st.text_area("Post Content")
    if st.button("Add Post"):
        res = requests.post(f"{API_URL}/add_post/", json={"title": title, "content": content})
        st.success(res.json()["message"])

elif tab == "💬 Search Chat":
    st.title("Chat & Search Posts")

    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    def add_message(role, content):
        st.session_state["messages"].append({"role": role, "content": content})

    for msg in st.session_state["messages"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_input = st.chat_input("Ask something...")
    if user_input:
        add_message("user", user_input)
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.spinner("Searching..."):
            #res = requests.post(f"{API_URL}/search/", json={"query": user_input})
            res = requests.get(API_URL + "/search/", params={"query": user_input})  # ✅ Correct: Using GET

            results = res.json()["results"]

        response = "Here are some relevant posts:\n\n" if results else "No relevant posts found."
        for post in results:
            response += f"**{post['title']}**\n{post['content']}\n\n"

        add_message("assistant", response)
        with st.chat_message("assistant"):
            st.markdown(response)
