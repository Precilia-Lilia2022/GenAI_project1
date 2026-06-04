
import streamlit as st  # type: ignore
from shot import FewShotPosts 
from post_generator import generate_post

# Page config
st.set_page_config(page_title="LinkedIn Post Generator", layout="wide")

# Initialize session state
if "history" not in st.session_state:
    st.session_state.history = []

def main():
    st.title("LinkedIn Post Generator")
    st.markdown("Generate professional LinkedIn posts with AI")
    
    # Sidebar settings
    st.sidebar.title("⚙️ Settings")
    creativity = st.sidebar.slider("Creativity Level", 0.0, 1.0, 0.7, help="Higher = more creative")
    include_hashtags = st.sidebar.checkbox("Include hashtags", value=True)
    include_emoji = st.sidebar.checkbox("Include emojis", value=True)
    
    # Main content with tabs
    tab1, tab2, tab3 = st.tabs(["📝 Generate", "📋 History", "ℹ️ About"])
    
    fs = FewShotPosts()
    
    with tab1:
        st.subheader("Create Your Post")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            selected_title = st.selectbox("Topic", options=fs.get_tags())
            
        with col2:
            selected_language = st.selectbox("Language", options=["English", "French", "Spanish"])
        
        with col3:
            selected_length = st.selectbox("Length", options=["Short", "Medium", "Long"])
        
        st.divider()
        
        # Generate options
        col_gen1, col_gen2 = st.columns(2)
        
        with col_gen1:
            if st.button("✨ Generate Single Post", use_container_width=True):
                with st.spinner("Generating your post..."):
                    try:
                        post = generate_post(selected_length, selected_language, selected_title)
                        st.session_state.history.insert(0, {"post": post, "topic": selected_title, "language": selected_language})
                        st.success("Post generated!")
                        st.write(post)
                        st.code(post, language="markdown")
                        
                        # Copy and download buttons
                        col_btn1, col_btn2 = st.columns(2)
                        with col_btn1:
                            st.download_button(
                                label="⬇️ Download Post",
                                data=post,
                                file_name="linkedin_post.txt",
                                use_container_width=True
                            )
                        with col_btn2:
                            st.button("📋 Copy to Clipboard", use_container_width=True)
                    except Exception as e:
                        st.error(f"Error generating post: {e}")
        
        with col_gen2:
            if st.button("🔀 Generate 3 Variants", use_container_width=True):
                with st.spinner("Generating variants..."):
                    try:
                        for i in range(3):
                            post = generate_post(selected_length, selected_language, selected_title)
                            st.session_state.history.insert(0, {"post": post, "topic": selected_title, "language": selected_language})
                            with st.expander(f"Variant {i+1}", expanded=(i==0)):
                                st.write(post)
                                st.code(post, language="markdown")
                        st.success(f"Generated 3 variants!")
                    except Exception as e:
                        st.error(f"Error generating variants: {e}")
    
    with tab2:
        st.subheader("Generated Posts History")
        if st.session_state.history:
            for idx, item in enumerate(st.session_state.history):
                with st.expander(f"Post {idx+1} - {item['topic']} ({item['language']})"):
                    st.write(item['post'])
                    col_del1, col_del2 = st.columns([3, 1])
                    with col_del2:
                        if st.button("🗑️ Delete", key=f"del_{idx}"):
                            st.session_state.history.pop(idx)
                            st.rerun()
            
            # Clear all button
            if st.button("🗑️ Clear All History"):
                st.session_state.history = []
                st.rerun()
        else:
            st.info("No posts generated yet. Start from the Generate tab!")
    
    with tab3:
        st.subheader("About This App")
        st.markdown("""
        ### 🎯 Purpose
        Generate engaging LinkedIn posts using AI (Llama 3.3 via Groq)
        
        ### ✨ Features
        - **Multiple Languages**: English, French, Spanish
        - **Post Length**: Short, Medium, Long
        - **Topics**: Auto-detected from processed data
        - **Multiple Variants**: Generate 3 versions at once
        - **History**: Keep track of all generated posts
        - **Customization**: Adjust creativity level
        
        ### 📚 Technology Stack
        - **Streamlit**: Web framework
        - **LangChain**: LLM orchestration
        - **Groq**: Fast LLM inference
        - **Llama 3.3**: Language model
        
        ### 🔗 Data Pipeline
        1. Posts processed and tagged
        2. Few-shot learning examples extracted
        3. AI generates new posts based on patterns
        """)

if __name__ == "__main__":
    main()
