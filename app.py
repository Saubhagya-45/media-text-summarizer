import streamlit as st
from utils.summarizer import summarize_long_text
from utils.pdf_reader import extract_text_from_pdf
from utils.question_answer import answer_question

# -----------------------------------
# PAGE CONFIG
# -----------------------------------

st.set_page_config(
    page_title="Media & Text Summarizer",
    page_icon="📝",
    layout="wide"
)

# -----------------------------------
# CUSTOM CSS
# -----------------------------------

st.markdown("""
<style>

.main {
    padding-top: 1rem;
}

.stButton > button {
    width: 100%;
    border-radius: 10px;
    height: 3em;
    font-size: 16px;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------------
# HEADER
# -----------------------------------

st.title("📝 Media & Text Summarizer")
st.markdown(
    "Generate summaries and ask questions from text or PDF documents using AI."
)

# -----------------------------------
# SIDEBAR
# -----------------------------------

st.sidebar.title("About")

st.sidebar.info(
    """
    AI-powered document assistant.

    Features:
    • Text Summarization
    • PDF Summarization
    • Question Answering
    • Download Summary
    """
)

st.sidebar.markdown("---")
st.sidebar.write("👨‍💻 Developed by Saubhagya Tiwari")

# -----------------------------------
# SESSION STATE
# -----------------------------------

if "summary" not in st.session_state:
    st.session_state.summary = ""

# -----------------------------------
# LAYOUT
# -----------------------------------

col1, col2 = st.columns(2)

user_text = ""

# -----------------------------------
# INPUT SECTION
# -----------------------------------

with col1:

    st.subheader("📄 Input")

    input_type = st.radio(
        "Choose Input Type",
        ["Text", "PDF"]
    )

    if input_type == "Text":

        user_text = st.text_area(
            "Paste your text below",
            height=350,
            placeholder="Enter or paste text here..."
        )

    else:

        uploaded_file = st.file_uploader(
            "Upload PDF",
            type=["pdf"]
        )

        if uploaded_file:

            with st.spinner("Reading PDF..."):

                user_text = extract_text_from_pdf(
                    uploaded_file
                )

            st.success("PDF Loaded Successfully")

            st.text_area(
                "Extracted Text Preview",
                value=user_text[:1500],
                height=200
            )

    word_count = len(user_text.split())
    char_count = len(user_text)

    st.write(f"📊 Words: **{word_count}**")
    st.write(f"🔤 Characters: **{char_count}**")

    summary_type = st.selectbox(
        "Summary Length",
        ["Short", "Medium", "Detailed"]
    )

    if summary_type == "Short":

        max_len = 50
        min_len = 20

    elif summary_type == "Medium":

        max_len = 100
        min_len = 40

    else:

        max_len = 180
        min_len = 80

    summarize_btn = st.button(
        "🚀 Generate Summary",
        use_container_width=True
    )

# -----------------------------------
# OUTPUT SECTION
# -----------------------------------

with col2:

    st.subheader("📝 Summary")

    if summarize_btn:

        if not user_text.strip():

            st.warning(
                "Please provide text or upload a PDF."
            )

        else:

            with st.spinner(
                "Generating Summary..."
            ):

                st.session_state.summary = summarize_long_text(
                    user_text,
                    max_len,
                    min_len
                )

            st.success(
                "Summary Generated Successfully!"
            )

    if st.session_state.summary:

        st.text_area(
            "Generated Summary",
            value=st.session_state.summary,
            height=250
        )

        st.download_button(
            label="📥 Download Summary",
            data=st.session_state.summary,
            file_name="summary.txt",
            mime="text/plain"
        )

    st.markdown("---")

    st.subheader("❓ Ask Questions")

    question = st.text_input(
        "Enter your question about the document"
    )

    if st.button("Get Answer"):

        if not user_text.strip():

            st.warning(
                "Upload a PDF or enter text first."
            )

        elif not question.strip():

            st.warning(
                "Please enter a question."
            )

        else:

            with st.spinner(
                "Finding Answer..."
            ):

                answer = answer_question(
                    question,
                    user_text
                )

            st.success("Answer")

            st.write(answer)