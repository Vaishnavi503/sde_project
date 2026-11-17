
import streamlit as st
import pandas as pd

# Initialize student records
if "students" not in st.session_state:
    st.session_state.students = pd.DataFrame(
        columns=["Roll No", "Name", "Age", "Course"]
    )

st.title("Student Record Management System")

menu = st.sidebar.selectbox(
    "Select Operation",
    ["Add Student", "View Students", "Update Student", "Delete Student"]
)

# CREATE
if menu == "Add Student":
    st.header("Add New Student")

    roll = st.number_input("Roll Number", min_value=1, step=1)
    name = st.text_input("Student Name")
    age = st.number_input("Age", min_value=1, max_value=100, step=1)
    course = st.text_input("Course")

    if st.button("Add Student"):
        if name.strip() and course.strip():
            if roll not in st.session_state.students["Roll No"].values:
                new_student = pd.DataFrame([{
                    "Roll No": roll,
                    "Name": name,
                    "Age": age,
                    "Course": course
                }])

                st.session_state.students = pd.concat(
                    [st.session_state.students, new_student],
                    ignore_index=True
                )

                st.success("Student added successfully!")
            else:
                st.error("Roll Number already exists!")
        else:
            st.error("Please enter all details.")

# READ
elif menu == "View Students":
    st.header("All Student Records")

    st.dataframe(st.session_state.students, use_container_width=True)

# UPDATE
elif menu == "Update Student":
    st.header("Update Student Details")

    df = st.session_state.students

    if not df.empty:
        roll = st.selectbox("Select Roll Number", df["Roll No"])

        student = df[df["Roll No"] == roll].iloc[0]

        name = st.text_input("Name", value=student["Name"])
        age = st.number_input("Age", min_value=1, max_value=100,
                              value=int(student["Age"]))
        course = st.text_input("Course", value=student["Course"])

        if st.button("Update"):
            st.session_state.students.loc[
                st.session_state.students["Roll No"] == roll,
                ["Name", "Age", "Course"]
            ] = [name, age, course]

            st.success("Student updated successfully!")
    else:
        st.info("No student records available.")

# DELETE
elif menu == "Delete Student":
    st.header("Delete Student Record")

    df = st.session_state.students

    if not df.empty:
        roll = st.selectbox("Select Roll Number", df["Roll No"])

        if st.button("Delete"):
            st.session_state.students = df[
                df["Roll No"] != roll
            ].reset_index(drop=True)

            st.success("Student deleted successfully!")
    else:
        st.info("No student records available.")
