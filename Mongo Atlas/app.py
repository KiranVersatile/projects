import streamlit as st
from pymongo import MongoClient
from bson.objectid import ObjectId


MONGO_URI = "mongodb+srv://kiran:Kiran99@cluster0.ymkwlan.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(MONGO_URI)
db = client["user_db"]
collection = db["users"]

st.set_page_config(page_title="MongoDB ", layout="centered")

st.title("MongoDB ")


def user_form(default_data=None, form_key="form"):
    with st.form(key=form_key):
        name = st.text_input(
            "Name", value=default_data["name"] if default_data else "")
        email = st.text_input(
            "Email", value=default_data["email"] if default_data else "")
        age = st.number_input("Age", min_value=0, max_value=120,
                              value=default_data["age"] if default_data else 18)
        submitted = st.form_submit_button("Submit")
        return submitted, {"name": name, "email": email, "age": age}


st.subheader("Add New User")
submitted, user_data = user_form(form_key="create_user_form")
if submitted:
    collection.insert_one(user_data)
    st.success("User added successfully!")


st.subheader("Existing Users")

users = list(collection.find())
if not users:
    st.info("No users found.")
else:
    for user in users:
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            st.markdown(
                f"**{user['name']}** ({user['email']}, Age: {user['age']})")

        with col2:
            if st.button("Edit", key=f"edit_button_{user['_id']}"):
                with st.expander(f"Edit {user['name']}", expanded=True):
                    edit_submitted, updated_data = user_form(
                        user, form_key=f"edit_form_{user['_id']}")
                    if edit_submitted:
                        collection.update_one({"_id": user["_id"]}, {
                                              "$set": updated_data})
                        st.success("updated successfully")

        with col3:
            if st.button("Delete", key=f"delete_button_{user['_id']}"):
                collection.delete_one({"_id": user["_id"]})
                st.warning(f" Deleted {user['name']}. Please refresh.")
