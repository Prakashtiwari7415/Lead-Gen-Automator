import os

import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.set_page_config(page_title="Lead-Gen Automator", layout="wide")
st.title("Lead-Gen Automator")
st.caption("Find leads, research them, and draft personalized outreach.")

with st.sidebar:
    st.header("Lead Search Inputs")
    niche = st.text_input("Niche", placeholder="IT services")
    location = st.text_input("Location", placeholder="Noida")
    client_service = st.text_area("Your Service", placeholder="Web development and SEO for local businesses")
    max_leads = st.slider("Max leads", min_value=1, max_value=10, value=5)
    run_btn = st.button("Generate Leads", type="primary")

if run_btn:
    if not niche or not location or not client_service:
        st.error("Please fill niche, location, and your service.")
    else:
        with st.spinner("Researching leads..."):
            try:
                resp = requests.post(
                    f"{BACKEND_URL}/api/leads/generate",
                    json={
                        "niche": niche,
                        "location": location,
                        "client_service": client_service,
                        "max_leads": max_leads,
                    },
                    timeout=200,
                )
            except requests.exceptions.ConnectionError:
                st.error(
                    f"❌ **Cannot connect to backend server at `{BACKEND_URL}`.**\n\n"
                    "**How to fix:**\n"
                    "1. **If running locally:** Make sure the FastAPI backend server is running in another terminal:\n"
                    "   ```bash\n"
                    "   python3 -m uvicorn backend.app.main:app --reload --port 8000\n"
                    "   ```\n"
                    "2. **If running on Streamlit Cloud:** Streamlit Cloud cannot connect to `localhost`. You must deploy your backend to a public host (e.g. Render, Railway) and set `BACKEND_URL` in Streamlit App Secrets."
                )
                st.stop()
            except requests.exceptions.RequestException as exc:
                st.error(f"❌ Backend request failed: {exc}")
                st.stop()

        if resp.status_code != 200:
            st.error(f"Backend error: {resp.status_code} - {resp.text}")
        else:
            data = resp.json()
            leads = data.get("leads", [])
            st.success(f"Generated {len(leads)} leads")
            for idx, lead in enumerate(leads, start=1):
                with st.expander(f"{idx}. {lead.get('company_name', 'Unknown')}"):
                    st.write(f"**Website:** {lead.get('website', '')}")
                    st.write(f"**Email:** {lead.get('contact_email', 'N/A')}")
                    st.write(f"**Phone:** {lead.get('phone', 'N/A')}")
                    st.write(f"**Summary:** {lead.get('summary', '')}")
                    st.write("**Pain Points:**")
                    for p in lead.get("pain_points", []):
                        st.write(f"- {p}")
                    st.write("**Outreach Draft:**")
                    st.code(lead.get("outreach_message", ""), language="markdown")

st.divider()
st.subheader("Search Lead Memory (Vector DB)")
memory_query = st.text_input("Memory query", placeholder="Companies needing better online visibility")
if st.button("Search Memory"):
    if not memory_query:
        st.warning("Enter a query first.")
    else:
        try:
            resp = requests.post(
                f"{BACKEND_URL}/api/leads/search-memory",
                json={"query": memory_query, "top_k": 5},
                timeout=60,
            )
        except requests.exceptions.ConnectionError:
            st.error(
                f"❌ **Cannot connect to backend server at `{BACKEND_URL}`.** Make sure FastAPI backend server is running."
            )
            st.stop()
        except requests.exceptions.RequestException as exc:
            st.error(f"❌ Backend request failed: {exc}")
            st.stop()

        if resp.status_code != 200:
            st.error(f"Backend error: {resp.status_code} - {resp.text}")
        else:
            results = resp.json().get("results", [])
            if not results:
                st.info("No stored leads found yet.")
            for r in results:
                st.write(f"**Score:** {r.get('score', 0):.4f}")
                meta = r.get("metadata", {})
                st.write(f"**Company:** {meta.get('company_name', 'N/A')}")
                st.write(f"**Website:** {meta.get('website', 'N/A')}")
                st.caption(r.get("content", "")[:300] + "...")
                st.divider()
