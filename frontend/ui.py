import streamlit as st
import requests

st.set_page_config(page_title="Echo Chat", layout="wide")

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
import streamlit as st
import requests

# Streamlit UI
st.title("Login")

# Input fields for username and password
username = st.text_input("Username")
password = st.text_input("Password", type="password")

# Button to submit login form
if st.button("Login"):
    # Send login request to Django backend
    response = requests.post("http://localhost:8000/api/token/", data={
        "username": username,
        "password": password
    })

    if response.status_code == 200:
        # Successful login
        token = response.json().get("access")
        st.success("Login successful!")
        st.session_state['token'] = token
    else:
        # Failed login
        st.error("Login failed. Please check your credentials.")

# Example of using the token to access a protected endpoint
if 'token' in st.session_state:
    headers = {"Authorization": f"Bearer {st.session_state['token']}"}
    protected_response = requests.get("http://localhost:8000/protected-endpoint/", headers=headers)

    if protected_response.status_code == 200:
        st.write("Access to protected data:", protected_response.json())
    else:
        st.error("Failed to access protected data.")

   # Streamlit UI
st.title("Register")

# Input fields for registration
reg_username = st.text_input("Username", key="reg_username")
reg_password = st.text_input("Password", type="password", key="reg_password")
reg_email = st.text_input("Email", key="reg_email")

# Button to submit registration form
if st.button("Register"):
    # Send registration request to Django backend
    reg_response = requests.post("http://localhost:8000/register/", data={
        "username": reg_username,
        "password": reg_password,
        "email": reg_email
    })

    if reg_response.status_code == 201:
        # Successful registration
        st.success("Registration successful! You can now log in.")
    else:
        # Failed registration
        st.error("Registration failed. Please check your details and try again.")