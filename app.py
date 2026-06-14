import streamlit as st
import pandas as pd
from datetime import date, timedelta

st.set_page_config(
    page_title="Smart Campus Resource Sharing System",
    page_icon="🏫",
    layout="wide"
)

# --------------------------
# Sample Data
# --------------------------
resources = pd.DataFrame({
    "Item": [
        "Scientific Calculator",
        "Umbrella",
        "Laptop Charger",
        "Lab Coat",
        "Power Bank",
        "First Aid Kit"
    ],
    "Category": [
        "Academic Items",
        "Emergency Resources",
        "Electronics",
        "Lab Equipment",
        "Electronics",
        "Emergency Resources"
    ],
    "Available": [15, 10, 8, 12, 6, 5]
})

borrowings = pd.DataFrame({
    "Item": ["Scientific Calculator", "Umbrella"],
    "Due Date": ["Jun 18", "Jun 15"],
    "Status": ["Active", "Due Soon"]
})

notifications = [
    "Reminder: Return Calculator in 1 day",
    "Penalty Alert: Umbrella overdue",
    "New Resource Available: Power Bank"
]

penalties = pd.DataFrame({
    "Student Name": ["Rithika", "Rahul", "Ananya"],
    "Item": ["Calculator", "Umbrella", "Lab Coat"],
    "Days Late": [2, 1, 3],
    "Fine (₹)": [40, 20, 60]
})

# --------------------------
# Session State
# --------------------------
if "role" not in st.session_state:
    st.session_state.role = None

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "student_name" not in st.session_state:
    st.session_state.student_name = "Anshul"

# --------------------------
# Welcome Screen
# --------------------------
if st.session_state.role is None:

    st.title("🏫 Smart Campus Resource Sharing System")

    st.markdown("## Select Your Role")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("👨‍🎓 Student", use_container_width=True):
            st.session_state.role = "Student"
            st.rerun()

    with col2:
        if st.button("👨‍💼 Admin", use_container_width=True):
            st.session_state.role = "Admin"
            st.rerun()

# --------------------------
# STUDENT FLOW
# --------------------------
elif st.session_state.role == "Student":

    if not st.session_state.logged_in:

        st.title("👨‍🎓 Student Login")

        student_id = st.text_input("Student ID / Email")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            st.session_state.logged_in = True
            st.rerun()

    else:

        page = st.sidebar.radio(
            "Navigation",
            [
                "Home Dashboard",
                "Resource Catalog",
                "Item Details",
                "Borrow Confirmation",
                "My Borrowings",
                "Notifications",
                "Return Item"
            ]
        )

        if page == "Home Dashboard":

            st.title("🏠 Home Dashboard")

            st.success(f"Welcome, {st.session_state.student_name}")

            search = st.text_input("🔍 Search Resources")

            st.subheader("Categories")

            cols = st.columns(5)

            categories = [
                "Academic Items",
                "Lab Equipment",
                "Electronics",
                "Emergency Resources",
                "Miscellaneous"
            ]

            for col, cat in zip(cols, categories):
                col.info(cat)

            st.divider()

            c1, c2, c3 = st.columns(3)

            c1.metric("Available Items", 56)
            c2.metric("Borrowed Items", 18)
            c3.metric("Due Soon", 4)

        elif page == "Resource Catalog":

            st.title("📚 Resource Catalog")

            st.dataframe(resources, use_container_width=True)

        elif page == "Item Details":

            st.title("📦 Item Details")

            st.subheader("Scientific Calculator")

            st.write("**Availability:** 15")
            st.write("**Borrow Duration:** 3 Days")
            st.write("**Penalty:** ₹20/day after due date")
            st.write("**Condition:** Good")

            st.button("Borrow Now")

        elif page == "Borrow Confirmation":

            st.title("✅ Borrow Confirmation")

            st.write("**Item Name:** Scientific Calculator")
            st.write(f"**Borrow Date:** {date.today()}")

            return_date = date.today() + timedelta(days=3)

            st.write(f"**Return Date:** {return_date}")
            st.write("**Penalty Policy:** ₹20/day after due date")

            agree = st.checkbox(
                "I agree to return the item on time"
            )

            if st.button("Confirm Borrow"):

                if agree:
                    st.success("Borrow Request Confirmed!")
                else:
                    st.warning("Please agree to the policy.")

        elif page == "My Borrowings":

            st.title("📋 My Borrowings")

            st.subheader("Active Borrowings")

            st.dataframe(
                borrowings,
                use_container_width=True
            )

        elif page == "Notifications":

            st.title("🔔 Notifications")

            for note in notifications:
                st.info(note)

        elif page == "Return Item":

            st.title("↩️ Return Item")

            st.write("📷 Student scans QR code")

            st.write("**Item Name:** Scientific Calculator")
            st.write("**Return Status:** Ready for Return")

            if st.button("Complete Return"):
                st.success("Item Returned Successfully!")

# --------------------------
# ADMIN FLOW
# --------------------------
elif st.session_state.role == "Admin":

    page = st.sidebar.radio(
        "Navigation",
        [
            "Admin Dashboard",
            "Inventory Management",
            "Penalty Management"
        ]
    )

    if page == "Admin Dashboard":

        st.title("👨‍💼 Admin Dashboard")

        c1, c2, c3, c4 = st.columns(4)

        c1.metric("Total Resources", 100)
        c2.metric("Borrowed Resources", 30)
        c3.metric("Overdue Resources", 5)
        c4.metric("Available Resources", 70)

    elif page == "Inventory Management":

        st.title("📦 Inventory Management")

        st.subheader("Add Item")

        item_name = st.text_input("Item Name")
        quantity = st.number_input(
            "Quantity",
            min_value=1,
            value=1
        )

        if st.button("Add Item"):
            st.success(f"{item_name} added successfully!")

        st.divider()

        st.subheader("Remove Item")

        st.selectbox(
            "Select Item",
            resources["Item"]
        )

        st.button("Remove Item")

        st.divider()

        st.subheader("Update Quantity")

        st.selectbox(
            "Item to Update",
            resources["Item"],
            key="update_item"
        )

        st.number_input(
            "New Quantity",
            min_value=0,
            value=10,
            key="qty_update"
        )

        st.button("Update Quantity")

        st.divider()

        st.subheader("Mark Item Damaged")

        st.selectbox(
            "Damaged Item",
            resources["Item"],
            key="damaged_item"
        )

        st.button("Mark Damaged")

    elif page == "Penalty Management":

        st.title("💰 Penalty Management")

        st.dataframe(
            penalties,
            use_container_width=True
        )

# --------------------------
# Reset Role Button
# --------------------------
st.sidebar.divider()

if st.sidebar.button("🔄 Change Role"):
    st.session_state.role = None
    st.session_state.logged_in = False
    st.rerun()
    