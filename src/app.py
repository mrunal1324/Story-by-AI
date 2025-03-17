import streamlit as st
import time
from story_engine import generate_story
from story_brancher import generate_plot_twist
# from image_engine import generate_image
from audio_engine import text_to_speech
import os
# from story_engine import get_story_model
# get_story_model()  # Preload model early

# Page configuration
st.set_page_config(
    page_title="AI Story Generator",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {margin-bottom: 0px;}
    .sub-header {margin-top: 0px;}
    .story-container {
        background-color: #212121;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #4CAF50;
        margin-bottom: 20px;
    }
    .twist-container {
        background-color: #212121;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #FF5722;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'story' not in st.session_state:
    st.session_state.story = ""
if 'plot_twist' not in st.session_state:
    st.session_state.plot_twist = ""
if 'generation_time' not in st.session_state:
    st.session_state.generation_time = 0

# App title
st.markdown("<h1 class='main-header'>📖 AI Story Generator with Plot Twist & Imagery</h1>", unsafe_allow_html=True)

# Sidebar
st.sidebar.markdown("## 🧠 Prompt Inputs")

# Tips
with st.sidebar.expander("Tips for better results", expanded=False):
    st.markdown("""
    * Be specific about settings, characters, and themes
    * Include genre information (fantasy, sci-fi, romance, etc.)
    * Mention time period or setting details
    """)

# Example prompts
with st.sidebar.expander("Example prompts", expanded=False):
    genre_examples = st.selectbox(
        "Genre examples",
        ["Fantasy", "Sci-Fi", "Romance", "Mystery", "Historical", "Horror"],
        label_visibility="collapsed"
    )
    
    example_prompts = {
        "Fantasy": "A young apprentice discovers a forbidden spellbook in an ancient library.",
        "Sci-Fi": "On a distant space colony, a scientist discovers an alien artifact that defies physics.",
        "Romance": "Two strangers keep missing each other by minutes until fate finally brings them together.",
        "Mystery": "A detective receives cryptic letters predicting crimes that haven't happened yet.",
        "Historical": "During the Renaissance, an artist's apprentice uncovers a conspiracy involving powerful families.",
        "Horror": "A family moves into a house where previous residents have mysteriously disappeared."
    }
    
    if st.button("Use Example"):
        st.session_state.prompt = example_prompts[genre_examples]

# Story prompt input
prompt = st.sidebar.text_area(
    "Enter your story prompt:",
    value=st.session_state.get('prompt', ""),
    height=100
)

# Options
st.sidebar.markdown("### Generation Options")
add_plot_twist = st.sidebar.checkbox("Add a plot twist", value=True)
# generate_imagery = st.sidebar.checkbox("Generate Story Image", value=False)
generate_audio = st.sidebar.checkbox("Generate Audio Narration", value=False)

# Advanced settings
with st.sidebar.expander("Advanced Settings", expanded=False):
    story_length = st.select_slider(
        "Story Length",
        options=["Short", "Medium", "Long"],
        value="Medium"
    )
    
    creativity = st.slider(
        "Creativity Level",
        min_value=0.1,
        max_value=1.0,
        value=0.85,
        step=0.05
    )
    
    use_ai_model = st.checkbox("Use AI Model (Slower)", value=False)

# Generate button
generate_button = st.sidebar.button("✨ Generate Story", use_container_width=True)

# Main content area
if generate_button:
    if not prompt:
        st.error("Please enter a story prompt before generating.")
    else:
        # Save prompt to session state
        st.session_state.prompt = prompt
        
        # Create a progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Update status
        status_text.text("Analyzing prompt...")
        progress_bar.progress(10)
        time.sleep(0.3)
        
        # Generate story
        start_time = time.time()
        status_text.text("Creating your story...")
        progress_bar.progress(30)
        
        story = generate_story(
            prompt, 
            length=story_length, 
            creativity=creativity,
            use_ai=use_ai_model
        )

        
        st.session_state.story = story
        st.session_state.generation_time = time.time() - start_time
        
        progress_bar.progress(70)
        status_text.text("Finalizing story...")
        time.sleep(0.3)
        
        # Generate plot twist if requested
        if add_plot_twist:
            status_text.text("Creating plot twist...")
            progress_bar.progress(85)
            plot_twist = generate_plot_twist(story, creativity=creativity)
            st.session_state.plot_twist = plot_twist
        
        # Complete
        progress_bar.progress(100)
        status_text.text("Story complete!")
        time.sleep(0.3)
        
        # Clear progress indicators
        progress_bar.empty()
        status_text.empty()

# Display story if available
if st.session_state.story:
    st.markdown("<h2 class='sub-header'>📘 Your AI-Generated Story:</h2>", unsafe_allow_html=True)
    st.markdown(f"<div class='story-container'>{st.session_state.story}</div>", unsafe_allow_html=True)
    st.caption(f"Generation time: {st.session_state.generation_time:.2f} seconds")
    
    # Display plot twist if available
    if st.session_state.plot_twist and add_plot_twist:
        st.markdown("---")
        st.markdown("<h2 class='sub-header'>🌀 Plot Twist:</h2>", unsafe_allow_html=True)
        st.markdown(f"<div class='twist-container'>{st.session_state.plot_twist}</div>", unsafe_allow_html=True)
    
    # # Generate image if requested
    # if generate_imagery:
    #     st.markdown("---")
    #     st.subheader("🖼️ Story Visualization:")
    #     with st.spinner("Creating image..."):
    #         try:
    #             image = generate_image(prompt)
    #             st.image(image, caption="AI-generated visualization", use_column_width=True)
    #         except Exception as e:
    #             st.error(f"Failed to generate image: {str(e)}")
    
    # Generate audio if requested
    if generate_audio:
        st.markdown("---")
        st.subheader("🔊 Story Audio:")
        with st.spinner("Generating audio..."):
            try:
                audio_path = text_to_speech(st.session_state.story)
                audio_file = open(audio_path, 'rb')
                audio_bytes = audio_file.read()
                st.audio(audio_bytes, format='audio/wav')
                audio_file.close()
                # Clean up temp file
                os.remove(audio_path)
            except Exception as e:
                st.error(f"Failed to generate audio: {str(e)}")

# Footer
st.markdown("---")
st.caption("AI Story Generator uses local language models (Ollama / fallback) for story generation and plot twists.")