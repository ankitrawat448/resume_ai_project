import streamlit as st
from resume_agent import resume_builder_agent
from profile_agent import profile_builder_agent  # your scraper
import os

st.set_page_config(page_title="AI Resume Builder", layout="centered")
st.title("🧠 AI Resume Builder from LinkedIn")
st.markdown("Paste a public LinkedIn profile URL below. The app will scrape the profile and generate a `.docx` + `.pdf` resume.")

linkedin_url = st.text_input("🔗 LinkedIn Profile URL")

if st.button("Generate Resume"):
    if not linkedin_url:
        st.warning("Please enter a LinkedIn profile URL.")
    else:
        with st.spinner("🔍 Scraping LinkedIn profile..."):
            profile_data = profile_builder_agent(linkedin_url)

        if "error" in profile_data:
            st.error(f"❌ Error during scraping: {profile_data['error']}")
        else:
            st.success("✅ Profile scraped successfully!")
            st.subheader("👀 Preview Extracted Data")
            st.json(profile_data)

            with st.spinner("📄 Generating resume..."):
                result = resume_builder_agent(profile_data)

            if "error" in result:
                st.error(f"❌ Resume generation failed: {result['error']}")
            else:
                st.success("✅ Resume generated!")

                st.download_button(
                    label="⬇️ Download DOCX",
                    data=open(result["docx_file"], "rb").read(),
                    file_name="resume.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )

                st.download_button(
                    label="⬇️ Download PDF",
                    data=open(result["pdf_file"], "rb").read(),
                    file_name="resume.pdf",
                    mime="application/pdf"
                )
