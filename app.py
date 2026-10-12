
import streamlit as st
from datetime import date

st.set_page_config(
    page_title="Smart Student Assistant",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 Smart Student Assistant")
st.write("Your personal study planner and learning companion.")

st.sidebar.title("Student Hub")
page = st.sidebar.radio(
    "Choose a page",
    ["Dashboard", "Study Planner", "Python Quiz"]
)

# Store tasks during the current session
if "tasks" not in st.session_state:
    st.session_state.tasks = []

if page == "Dashboard":
    st.header("📊 Your Dashboard")

    total = len(st.session_state.tasks)
    completed = sum(
        1 for task in st.session_state.tasks
        if task["done"]
    )

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Tasks", total)
    col2.metric("Completed", completed)
    col3.metric("Pending", total - completed)

    if total > 0:
        st.progress(completed / total)

    pending = [
        task for task in st.session_state.tasks
        if not task["done"]
    ]

    if pending:
        st.subheader("🎯 Suggested Next Task")
        high_priority = [
            task for task in pending
            if task["priority"] == "High"
        ]

        if high_priority:
            st.info("Start with: " + high_priority[0]["title"])
        else:
            st.info("Start with: " + pending[0]["title"])
    else:
        st.success("Add a study task to get started!")

elif page == "Study Planner":
    st.header("🗓️ Study Planner")

    with st.form("task_form"):
        title = st.text_input("Task name")
        subject = st.selectbox(
            "Subject",
            ["Python", "C Programming", "AI/ML", "Maths", "Other"]
        )
        priority = st.selectbox(
            "Priority", ["High", "Medium", "Low"]
        )
        due_date = st.date_input("Due date", value=date.today())

        submitted = st.form_submit_button("Add Task")

    if submitted:
        if title.strip():
            st.session_state.tasks.append({
                "title": title.strip(),
                "subject": subject,
                "priority": priority,
                "due": due_date,
                "done": False
            })
            st.success("Task added successfully!")
        else:
            st.warning("Please enter a task name.")

    st.subheader("📚 Your Tasks")

    for i, task in enumerate(st.session_state.tasks):
        st.write(
            f"**{task['title']}** — {task['subject']} "
            f"— {task['priority']} priority"
        )
        st.caption(f"Due: {task['due']}")

        task["done"] = st.checkbox(
            "Completed",
            value=task["done"],
            key=f"task_{i}"
        )

elif page == "Python Quiz":
    st.header("🧠 Python Beginner Quiz")

    questions = [
        (
            "Which keyword defines a function?",
            ["func", "def", "make"],
            "def"
        ),
        (
            "Which type stores True or False?",
            ["int", "bool", "str"],
            "bool"
        ),
        (
            "What does len([1, 2, 3]) return?",
            ["2", "3", "4"],
            "3"
        )
    ]

    answers = []

    for i, question in enumerate(questions):
        answer = st.radio(
            question[0],
            question[1],
            key=f"quiz_{i}"
        )
        answers.append(answer)

    if st.button("Check Score"):
        score = sum(
            answers[i] == questions[i][2]
            for i in range(len(questions))
        )
        st.metric("Your Score", f"{score}/3")

        if score == 3:
            st.success("Excellent! All answers are correct.")
        else:
            st.info("Keep practising and try again.")

st.sidebar.markdown("---")
st.sidebar.caption("Built with Python + Streamlit")
