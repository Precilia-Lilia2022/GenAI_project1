
import streamlit as st  # type: ignore
from shot import FewShotPosts 


def main():
    st.title("LinkedIn Post Generator")
    col1, col2, col3 = st.columns(3)
    fs = FewShotPosts()
    with col1:
        selected_title = st.selectbox("Title", options=fs.get_tags())
        
    with col2:
        selected_language = st.selectbox("Language", options=["English", "French"])
    
    with col3:
        selected_length = st.selectbox("Length", options=["Short", "Medium", "Long"])
        
    if st.button("Generate Post"):
        st.write("Generating post...")

if __name__ == "__main__":
    main()