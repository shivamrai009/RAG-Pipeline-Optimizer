import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("🧪 RAG Pipeline Optimizer")

st.sidebar.header("Upload Configuration")
uploaded_file = st.sidebar.file_uploader("Upload Company Doc (PDF)", type="pdf")
question = st.sidebar.text_input("Test Question", "What is the policy on remote work?")

if st.sidebar.button("Run Experiments"):
    if uploaded_file and question:
        with st.spinner("Running 3 RAG Pipelines & Evaluator Agent..."):
            # Send to Backend
            files = {"file": uploaded_file.getvalue()}
            data = {"question": question}
            
            # Assuming backend is on port 8000
           import os  # Add this at the top if missing

# ... inside your button click logic ...

# Dynamic URL: Uses the environment variable if available, otherwise defaults to localhost
backend_url = os.getenv("BACKEND_URL", "http://localhost:8000")
api_endpoint = f"{backend_url}/optimize"

response = requests.post(api_endpoint, files={"file": uploaded_file}, data={"question": question})
            
            if response.status_code == 200:
                results = response.json()["results"]
                
                # Visuals
                df = pd.DataFrame([
                    {
                        "Strategy": r["strategy"],
                        "Relevance": r["scores"]["relevance_score"],
                        "Accuracy": r["scores"]["accuracy_score"],
                        "Chunk Size": r["chunk_size"]
                    } for r in results
                ])
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("Performance Comparison")
                    fig = px.bar(df, x="Strategy", y=["Relevance", "Accuracy"], barmode="group")
                    st.plotly_chart(fig)
                
                with col2:
                    st.subheader("Detailed Analysis")
                    st.dataframe(df)

                st.subheader("Pipeline Outputs")
                for r in results:
                    with st.expander(f"Strategy: {r['strategy']} (Score: {r['scores']['relevance_score']}/10)"):
                        st.markdown(f"**Answer:** {r['answer']}")
                        st.caption(f"**Judge's Explanation:** {r['scores']['explanation']}")
            else:
                st.error("Error connecting to backend.")