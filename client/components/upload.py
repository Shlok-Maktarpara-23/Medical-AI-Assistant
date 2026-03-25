import streamlit as st
from utils.api import upload_pdfs_api, get_uploaded_files, delete_file


def render_uploader():
    st.sidebar.header("Upload Medical documents (.PDFs)")
    uploaded_files = st.sidebar.file_uploader("Upload multiple PDFs", type="pdf", accept_multiple_files=True)
    if st.sidebar.button("Upload DB") and uploaded_files:
        response = upload_pdfs_api(uploaded_files)
        if response.status_code == 200:
            st.sidebar.success("Uploaded successfully")
        else:
            st.sidebar.error(f"Error:{response.text}")

    # --- Uploaded Files Section ---
    st.sidebar.markdown("---")
    st.sidebar.header("Uploaded Files")

    with st.sidebar:
        with st.spinner("Loading files..."):
            try:
                response = get_uploaded_files()
                if response.status_code == 200:
                    files = response.json().get("files", [])
                    if files:
                        for file in files:
                            col1, col2 = st.columns([5, 1])
                            col1.markdown(f"<p style='font-size:16px; padding-top:8px; margin:0;'>📄 {file}</p>", unsafe_allow_html=True)
                            if col2.button("✖", key=f"del_{file}", help=f"Delete {file}"):
                                del_response = delete_file(file)
                                if del_response.status_code == 200:
                                    st.success(f"'{file}' deleted!")
                                    st.rerun()
                                else:
                                    st.error(f"Failed to delete '{file}'")
                    else:
                        st.sidebar.info("No files uploaded yet.")
                else:
                    st.sidebar.warning("Could not fetch uploaded files.")
            except Exception:
                st.sidebar.warning("Server not reachable.")

