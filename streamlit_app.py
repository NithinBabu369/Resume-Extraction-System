# streamlit_app.py
import streamlit as st
import json
from app.services.extractor import extract_text_from_file
from app.services.llm_parser import parse_resume_text

# Page Configuration
st.set_page_config(
    page_title="Ordered CV Parser",
    page_icon="📄",
    layout="wide"
)

st.title("📄 Resume Extraction System")
st.caption("Transform unstructured CVs into validated data models using PyMuPDF, groq/compound-mini, and Pydantic.")

# File Upload Section
uploaded_file = st.file_uploader("Upload a CV (PDF or DOCX)", type=["pdf", "docx"])

if uploaded_file is not None:
    # Read raw bytes
    file_bytes = uploaded_file.read()
    filename = uploaded_file.name

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("1. File Extraction")
        st.info(f"Loaded **{filename}**")
        
        with st.spinner("Extracting text from file..."):
            try:
                raw_text = extract_text_from_file(file_bytes, filename)
                st.success("Text extracted successfully!")
                with st.expander("View Raw Extracted Text", expanded=False):
                    st.text_area("Extracted Raw Text", raw_text, height=400)
            except Exception as e:
                st.error(f"Error extracting text: {e}")
                raw_text = None

    with col2:
        st.subheader("2. Structured Parsing")
        
        if raw_text:
            if st.button("Parse CV into Ordered Schema", type="primary"):
                with st.spinner("Parsing CV with groq/compound-mini..."):
                    try:
                        # Extract structured data
                        parsed_data = parse_resume_text(raw_text)
                        
                        # Convert model to dict to display
                        data_dict = parsed_data.model_dump()
                        st.session_state["parsed_result"] = data_dict
                        st.success("Parsing complete!")
                    except Exception as e:
                        st.error(f"Failed to parse resume: {e}")

        # Render parsed results if present in session state
        if "parsed_result" in st.session_state:
            result = st.session_state["parsed_result"]
            
            # Formatted JSON Download Button
            json_str = json.dumps(result, indent=2)
            st.download_button(
                label="📥 Download JSON Output",
                data=json_str,
                file_name=f"{filename.split('.')[0]}_parsed.json",
                mime="application/json"
            )

            # Display sections in exact ordered hierarchy
            st.markdown("---")
            
            # 1. Header
            st.markdown("### 👤 Header")
            header = result.get("header", {})
            st.write(f"**Name:** {header.get('full_name')}")
            st.write(f"**Email:** {header.get('email') or 'N/A'}")
            st.write(f"**Phone:** {header.get('phone') or 'N/A'}")
            st.write(f"**Location:** {header.get('location') or 'N/A'}")
            if header.get("links"):
                st.write("**Links:** " + ", ".join(header.get("links")))

            # 2. Profile
            st.markdown("### 📝 Profile")
            st.write(result.get("profile") or "No profile summary found.")

            # 3. Experience
            st.markdown("### 💼 Experience")
            exp_list = result.get("experience", [])
            if exp_list:
                for exp in exp_list:
                    st.markdown(f"**{exp.get('job_title')}** at *{exp.get('company')}* ({exp.get('duration') or 'N/A'})")
                    for resp in exp.get("responsibilities", []):
                        st.markdown(f"- {resp}")
            else:
                st.write("No work experience found.")

            # 4. Projects
            st.markdown("### 🚀 Projects")
            proj_list = result.get("projects", [])
            if proj_list:
                for proj in proj_list:
                    st.markdown(f"**{proj.get('title')}**")
                    st.write(proj.get("description"))
                    if proj.get("technologies"):
                        st.caption("Technologies: " + ", ".join(proj.get("technologies")))
            else:
                st.write("No projects found.")

            # 5. Skills
            st.markdown("### 🛠️ Skills")
            skills = result.get("skills", [])
            if skills:
                st.write(", ".join(skills))
            else:
                st.write("No skills found.")

            # 6. Education
            st.markdown("### 🎓 Education")
            edu_list = result.get("education", [])
            if edu_list:
                for edu in edu_list:
                    st.write(f"- **{edu.get('degree')}** — {edu.get('institution')} ({edu.get('year') or 'N/A'})")
            else:
                st.write("No education details found.")

            # 7. Certification
            st.markdown("### 📜 Certifications")
            certs = result.get("certification", [])
            if certs:
                for cert in certs:
                    st.write(f"- {cert}")
            else:
                st.write("No certifications found.")