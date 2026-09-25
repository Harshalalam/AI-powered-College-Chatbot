import streamlit as st
import pandas as pd
from database import get_all_complaints, update_status, init_db

# Initialize database
init_db()

st.set_page_config(page_title="Admin Dashboard", page_icon="🛠️", layout="wide")

st.title("🛠️ College Complaint Admin Dashboard")
st.markdown("View and manage all registered complaints")
st.divider()

# Fetch complaints
complaints = get_all_complaints()

if not complaints:
    st.info("No complaints registered yet.")
else:
    # Convert to DataFrame
    df = pd.DataFrame(complaints, columns=["Ticket ID", "Complaint", "Category", "Priority", "Status", "Created At"])
    
    st.subheader(f"Total Complaints: {len(df)}")
    
    # Show table
    st.dataframe(df, use_container_width=True)
    
    st.divider()
    st.subheader("Update Complaint Status")
    
    ticket_ids = df["Ticket ID"].tolist()
    selected_ticket = st.selectbox("Select Ticket ID", ticket_ids)
    
    new_status = st.selectbox("New Status", ["Pending", "In Progress", "Resolved"])
    
    if st.button("Update Status"):
        update_status(selected_ticket, new_status)
        st.success(f"Status of {selected_ticket} updated to {new_status}")
        st.rerun()
