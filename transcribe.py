import instaloader
import streamlit as st
from moviepy import VideoFileClip
import os
import assemblyai as aai
from dotenv import load_dotenv
try:
    import whisper
except ImportError:
    st.error("OpenAI Whisper not installed. Please run `pip install openai-whisper`")
    whisper = None # Handle missing whisper gracefully

from database import DatabaseManager

# Load environment variables
env_path = "/Users/jaydengle/Transcribe-Reels/.env"
load_dotenv(dotenv_path=env_path)

# Ensure external tools (ffmpeg) are found
os.environ["PATH"] += os.pathsep + "/opt/homebrew/bin" + os.pathsep + "/usr/local/bin"

# Set AssemblyAI API key
aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")

# Initialize Database
db_manager = DatabaseManager()
db_connected = db_manager.connect()

if not db_connected:
    st.warning("Could not connect to Supabase. Transcripts will not be saved.")

# Function to download Instagram Reel
def download_reel(url):
    try:
        if not os.path.exists('reel'):
            os.makedirs('reel')
        
        loader = instaloader.Instaloader()
        shortcode = url.split('/')[-2]
        loader.download_post(instaloader.Post.from_shortcode(loader.context, shortcode), target='reel')
        
        video_files = [f for f in os.listdir('reel') if f.endswith('.mp4')]
        if not video_files:
            return None
        
        return os.path.join('reel', video_files[0])
    except Exception as e:
        st.error(f"Error downloading reel: {e}")
        return None

# Function to convert video to audio
def convert_video_to_audio(video_file):
    clip = VideoFileClip(video_file)
    clip.audio.write_audiofile("audio.wav", codec='pcm_s16le', ffmpeg_params=["-ac", "1", "-ar", "16000"]) 
    clip.close()
    return "audio.wav"

# Function to transcribe utilizing Whisper (Local)
def transcribe_with_whisper(audio_file, model_size="base"):
    if whisper is None:
        st.error("Whisper library not found.")
        return None
    
    model = whisper.load_model(model_size)
    result = model.transcribe(audio_file)
    return result

# Function to transcribe utilizing AssemblyAI (API)
def transcribe_with_assemblyai(audio_file):
    transcriber = aai.Transcriber()
    config = aai.TranscriptionConfig(
        speaker_labels=True,
        speech_models=["universal-2"],
        language_detection=True
    )
    with open(audio_file, "rb") as f:
        transcript = transcriber.transcribe(f, config)
    return transcript

# Initialize OpenAI
openai_api_key = os.getenv("OPENAI_API_KEY")
if openai_api_key:
    from openai import OpenAI
    openai_client = OpenAI(api_key=openai_api_key)
else:
    openai_client = None

# Custom CSS for "Jay's Cheat Model" Theme (Red/Black Hacker Vibe)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Mono:ital,wght@0,400;0,700;1,400&display=swap');

    /* Main Background - Dark Cyber */
    .stApp {
        background-color: #000000;
        background-image: radial-gradient(circle at 50% 50%, #1a0000 0%, #000000 100%);
        color: #ffcccc;
        font-family: 'Space Mono', monospace;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #050000;
        border-right: 1px solid #330000;
    }
    
    /* Card/Container Glassmorphism - Red Hint */
    div.css-1r6slb0.e1tzin5v2, [data-testid="stExpander"] {
        background: rgba(20, 0, 0, 0.7);
        backdrop-filter: blur(5px);
        border: 1px solid #ff0000;
        border-radius: 4px; /* Sharper edges for tech feel */
        box-shadow: 0 0 15px rgba(255, 0, 0, 0.1);
    }
    
    /* Glitch Title Style */
    .glitch-title {
        font-size: 3rem;
        font-weight: bold;
        text-transform: uppercase;
        position: relative;
        text-shadow: 0.05em 0 0 #00fffc, -0.03em -0.04em 0 #fc00ff,
                     0.025em 0.04em 0 #fffc00;
        animation: glitch 725ms infinite;
        color: #ffffff;
    }
    
    @keyframes glitch {
        0% { text-shadow: 0.05em 0 0 #00fffc, -0.03em -0.04em 0 #fc00ff, 0.025em 0.04em 0 #fffc00; }
        15% { text-shadow: 0.05em 0 0 #00fffc, -0.03em -0.04em 0 #fc00ff, 0.025em 0.04em 0 #fffc00; }
        16% { text-shadow: -0.05em -0.025em 0 #00fffc, 0.025em 0.035em 0 #fc00ff, -0.05em -0.05em 0 #fffc00; }
        49% { text-shadow: -0.05em -0.025em 0 #00fffc, 0.025em 0.035em 0 #fc00ff, -0.05em -0.05em 0 #fffc00; }
        50% { text-shadow: 0.05em 0.035em 0 #00fffc, 0.03em 0 0 #fc00ff, 0 -0.04em 0 #fffc00; }
        99% { text-shadow: 0.05em 0.035em 0 #00fffc, 0.03em 0 0 #fc00ff, 0 -0.04em 0 #fffc00; }
        100% { text-shadow: -0.05em 0 0 #00fffc, -0.025em -0.04em 0 #fc00ff, -0.04em -0.025em 0 #fffc00; }
    }
    
    /* Headers - Red Gradient */
    h1, h2, h3 {
        background: linear-gradient(90deg, #ff0000, #ff4d4d);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Space Mono', monospace !important;
        letter-spacing: -1px;
    }
    
    /* Buttons - Red Neon */
    .stButton > button {
        background: #000000;
        color: #ff0000;
        border: 1px solid #ff0000;
        border-radius: 0px; /* Cyberpunk style */
        padding: 0.5rem 1rem;
        font-weight: bold;
        text-transform: uppercase;
        transition: all 0.2s ease;
        box-shadow: 0 0 10px rgba(255, 0, 0, 0.2);
    }
    .stButton > button:hover {
        background: #ff0000;
        color: #000000;
        box-shadow: 0 0 20px rgba(255, 0, 0, 0.8);
    }
    
    /* Input Fields */
    .stTextInput > div > div > input {
        background-color: #0a0000;
        color: #ff0000;
        border: 1px solid #330000;
        border-radius: 0px;
        font-family: 'Space Mono', monospace;
    }
    .stTextInput > div > div > input:focus {
        border-color: #ff0000;
        box-shadow: 0 0 10px rgba(255, 0, 0, 0.4);
    }
    
    /* Expander Transitions */
    .streamlit-expanderHeader {
        background-color: transparent;
        color: #ffcccc;
        font-family: 'Space Mono', monospace;
    }
</style>
""", unsafe_allow_html=True)

# Main UI Structure
# Use custom HTML for the Glitch Title Logo
st.markdown('<h1 class="glitch-title">JAY\'S COOL INSTAGRAM<br>CHEAT MODEL 💀</h1>', unsafe_allow_html=True)

# Sidebar for controls (restoring missing settings)
st.sidebar.header("SYSTEM CONFIG")
transcription_engine = st.sidebar.selectbox("ENGINE CORE", ["OpenAI Whisper (Local - Better Quality)", "AssemblyAI (Cloud)"])
model_size = "base"
if transcription_engine == "OpenAI Whisper (Local - Better Quality)":
    model_size = st.sidebar.selectbox("MODEL SIZE", ["tiny", "base", "small", "medium", "large"], index=2)

# Layout: 3 Columns (Sources, Chat/Main, Studio)
file_col, chat_col, studio_col = st.columns([1, 2, 1])

# --- Column 1: Sources (Library) ---
with file_col:
    st.markdown("### 💾 DATA SOURCE")
    
    # Add Source
    with st.expander("➕ Add Source", expanded=True):
        url = st.text_input("Reel URL", placeholder="Paste Instagram Link...")
        if st.button("Add to Memory"):
            if url:
                with st.spinner("Processing..."):
                    video_file = download_reel(url)
                    if video_file:
                        audio_file = convert_video_to_audio(video_file)
                        transcript_text = ""
                        # Default to AssemblyAI for stability in this demo unless Whisper is forced
                        if transcription_engine == "OpenAI Whisper (Local - Better Quality)" and whisper:
                             res = transcribe_with_whisper(audio_file, model_size)
                             if res: transcript_text = res["text"]
                        else:
                             res = transcribe_with_assemblyai(audio_file)
                             if res: transcript_text = res.text
                        
                        if transcript_text and db_connected:
                             db_manager.save_transcript(url, transcript_text, metadata={"engine": "auto"})
                             st.success("Added!")
                        
                        # Cleanup
                        if os.path.exists(video_file): os.remove(video_file)
                        if os.path.exists(audio_file): os.remove(audio_file)

    # List Sources
    if db_connected:
        sources = db_manager.get_all_transcripts()
        selected_source = None
        
        # Display as a radio list or buttons for selection
        source_options = [f"{s.get('created_at', '')[:10]} - {s.get('url', '')[-15:]}" for s in sources]
        if source_options:
            selected_idx = st.radio("Your Reels", range(len(source_options)), format_func=lambda x: source_options[x], label_visibility="collapsed")
            selected_source = sources[selected_idx]

# --- Column 2: Main / Chat Area ---
with chat_col:
    if selected_source:
        st.subheader("📝 Transcript View")
        st.info(f"Source: {selected_source.get('url')}")
        
        # Editable Transcript Text
        text_area_height = 500
        edit_text = st.text_area("Content", value=selected_source.get('text', ''), height=text_area_height)
        
        # --- Advanced Chat System (Multi-Mode) ---
        st.divider()
        st.subheader("💬 Neural Chat Link")
        
        # 1. Chat Mode Selector
        chat_mode = st.selectbox("PROTOCOL SELECTION", 
            ["🧠 ANALYSIS (General)", "♟️ STRATEGY PLANNER", "🎣 VIRAL HOOKS GEN"], 
            format_func=lambda x: x.split(" (")[0],
            key="chat_mode_select"
        )
        
        # 2. Initialize Session State for *each* mode independently
        mode_key = f"messages_{chat_mode}"
        if mode_key not in st.session_state:
            # Set distinct system prompts for each mode
            system_prompt = "You are a helpful AI assistant analyzing this transcript."
            if "STRATEGY" in chat_mode:
                system_prompt = "You are a Master Strategist. Your goal is to convert this content into a concrete 3-step execution plan. Focus on 'How-To', 'distribution', and 'monetization'."
            elif "HOOKS" in chat_mode:
                system_prompt = "You are a Viral Content Expert. Generate catchy, clickbaity, and curiosity-inducing hooks based on this transcript. Format as a list of 5 variations."
            
            st.session_state[mode_key] = [{"role": "system", "content": system_prompt}]

        # 3. Display Chat History for current mode
        for msg in st.session_state[mode_key]:
            if msg["role"] != "system":
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])

        # 4. Chat Input & Processing
        if prompt := st.chat_input("Input command..."):
            if not openai_client:
                st.error("SYSTEM ERROR: OpenAI API Key Missing.")
            else:
                # Add User Message
                st.session_state[mode_key].append({"role": "user", "content": prompt})
                with st.chat_message("user"):
                    st.markdown(prompt)

                # Generate Response
                with st.chat_message("assistant"):
                    message_placeholder = st.empty()
                    full_response = ""
                    
                    # Prepare context (Transcript + History)
                    # We inject the transcript as specific context for the *current* turn if it's the first query, 
                    # OR we can append it to the system prompt. 
                    # Better: Prepend text to the prompt context without adding to visible history
                    
                    messages_to_send = [st.session_state[mode_key][0]] # System prompt
                    messages_to_send.append({"role": "system", "content": f"TRANSCRIPT CONTEXT:\n{selected_source.get('text')}"})
                    messages_to_send.extend(st.session_state[mode_key][1:]) # Rest of history
                    
                    try:
                        stream = openai_client.chat.completions.create(
                            model="gpt-4",
                            messages=messages_to_send,
                            stream=True
                        )
                        
                        for chunk in stream:
                            if chunk.choices[0].delta.content is not None:
                                full_response += chunk.choices[0].delta.content
                                message_placeholder.markdown(full_response + "▌")
                        
                        message_placeholder.markdown(full_response)
                        
                        # Add Assistant Message to History
                        st.session_state[mode_key].append({"role": "assistant", "content": full_response})
                        
                        # Sync "Global" messages for the Slide Generator (use Strategy mode as priority, else current)
                        # We'll just set a pointer validation
                        st.session_state["messages"] = st.session_state[mode_key]

                    except Exception as e:
                        st.error(f"NEURAL HANDSHAKE FAILED: {e}")

    else:
        st.markdown("### 👋 Welcome to Memory Engine\nSelect a source from the left to view content or start a chat.")

# --- Column 3: Studio (Actions) ---
with studio_col:
    st.markdown("### 🛠️ CREATOR STUDIO")
    
    if selected_source:
        
        # --- 1. Audio & Briefing ---
        with st.expander("🎙️ AUDIO & BRIEFING", expanded=False):
            if st.button("🎙 Audio Overview"):
                 if openai_client:
                    with st.spinner("Generating Audio Overview (this may take a moment)..."):
                        try:
                            # 1. Generate Script
                            web_summary_prompt = f"Create a short, engaging podcast-style script summarizing this transcript. Keep it under 200 words. Use a conversational tone.\n\nTranscript: {selected_source.get('text')}"
                            script_response = openai_client.chat.completions.create(
                                model="gpt-4", 
                                messages=[{"role": "user", "content": web_summary_prompt}]
                            )
                            script_text = script_response.choices[0].message.content
                            
                            # 2. Convert to Audio
                            response = openai_client.audio.speech.create(
                                model="tts-1",
                                voice="alloy",
                                input=script_text
                            )
                            
                            # 3. Stream/Save
                            audio_path = "overview_audio.mp3"
                            response.stream_to_file(audio_path)
                            
                            st.success("Audio Generated!")
                            st.audio(audio_path)
                            st.markdown(f"**Script:**\n{script_text}")
                            
                        except Exception as e:
                            st.error(f"Error generating audio: {e}")
                 else:
                     st.error("OpenAI API Key required.")
            
            if st.button("📝 Briefing Doc"):
                 if openai_client:
                    with st.spinner("Drafting Briefing Document..."):
                        prompt = f"Create a comprehensive briefing document from this transcript, including key takeaways, target audience, and potential content angles:\n{selected_source.get('text')}"
                        response = openai_client.chat.completions.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}])
                        st.markdown(response.choices[0].message.content)

        # --- 5. Visual Studio ---
        with st.expander("🎨 VISUAL STUDIO", expanded=False):
            # Style Selector
            ppt_style = st.selectbox("Presentation Style", 
                ["Cyberpunk Matrix (Green/Black)", "Neon Synthwave (Pink/Purple)", "Corporate Clean (White/Blue)", "Dark Mode (Minimal)", "Golden Luxury (Black/Gold)"])
            
            if st.button("🖼 Generate Cover Art & Assets"):
                 # Matrix Loading Effect
                 with st.spinner("INITIATING NEURAL LINK..."):
                     progress_bar = st.progress(0)
                     import time
                     for i in range(100):
                         time.sleep(0.01)
                         progress_bar.progress(i + 1)
                     
                     try:
                         # 1. Create a Prompt from Transcript
                         if openai_client:
                             style_prompt = ""
                             if "Cyberpunk" in ppt_style: style_prompt = "green matrix code digital rain, hacker workspace, ultra realistic, 8k"
                             elif "Neon" in ppt_style: style_prompt = "synthwave vaporwave sunset grid, neon pink and blue, retro 80s"
                             elif "Corporate" in ppt_style: style_prompt = "clean modern office skyscraper abstract, white and blue geometric"
                             elif "Golden" in ppt_style: style_prompt = "black marble with gold veins, luxury minimal elegant"
                             else: style_prompt = "dark minimal tech abstract background"

                             img_prompt_req = f"Create a simple vivid AI image prompt for a presentation background based on this text. Integrate this style: {style_prompt}.\n\nText: {selected_source.get('text')}"
                             resp = openai_client.chat.completions.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": img_prompt_req}])
                             image_prompt = resp.choices[0].message.content
                         else:
                             image_prompt = f"Abstract background representing {selected_source.get('url')}, 4k"

                         # 2. Call Pollinations API (Free, No Key)
                         import random
                         seed = random.randint(0, 10000)
                         import urllib.parse
                         encoded_prompt = urllib.parse.quote(image_prompt)
                         image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?nologo=true&seed={seed}&model=flux&width=1920&height=1080"
                         
                         st.image(image_url, caption=f"AI Generated Asset ({ppt_style})")
                         st.session_state['generated_image'] = image_url 
                         st.session_state['ppt_style'] = ppt_style
                         st.success("Visuals Generated!")
                         
                     except Exception as e:
                         st.error(f"Image Gen Error: {e}")

            # --- PowerPoint Deck (Enhanced) ---
            if st.button("📊 Create Slide Deck (PPTX)"):
             if openai_client:
                 with st.spinner("Compiling Deck..."):
                    try:
                        from pptx import Presentation
                        from pptx.util import Inches, Pt
                        from pptx.dml.color import RGBColor
                        import io
                        import requests
                        import json

                        # 1. Generate Outline (WITH CHAT CONTEXT & STRATEGY)
                        full_context = f"Transcript:\n{selected_source.get('text')}\n\n"
                        
                        # Add Chat History context if available
                        if "messages" in st.session_state:
                             chat_log = "\n".join([f"{msg['role']}: {msg['content']}" for msg in st.session_state.messages])
                             full_context += f"\n\n--- BRAINSTORMING STRATEGY SESSION ---\n{chat_log}\n\n"
                             instruction = "Create a powerful 7-slide presentation outline based on the TRANSCRIPT and the refined STRATEGY discussed above. Prioritize hooks and marketing angles developed in the chat. Return a JSON list of objects only."
                        else:
                             instruction = "Create a powerful 7-slide presentation outline based on this text. Return a JSON list of objects only."

                        ppt_prompt = f"{instruction} \n\nCONTEXT:\n{full_context}"
                        response = openai_client.chat.completions.create(model="gpt-4", response_format={ "type": "json_object" }, messages=[{"role": "user", "content": ppt_prompt}])
                        import json
                        slides_data = json.loads(response.choices[0].message.content)
                        
                        # 2. Build PPTX
                        prs = Presentation()
                        prs.slide_width = Inches(16)
                        prs.slide_height = Inches(9)

                        # Define Colors based on Style
                        bg_color = RGBColor(0, 0, 0)
                        text_color = RGBColor(255, 255, 255)
                        accent_color = RGBColor(255, 0, 0) # Default Red

                        current_style = st.session_state.get('ppt_style', "Dark Mode")
                        if "Cyberpunk" in current_style:
                            accent_color = RGBColor(0, 255, 0)
                        elif "Neon" in current_style:
                             accent_color = RGBColor(255, 0, 255)
                        elif "Corporate" in current_style:
                             bg_color = RGBColor(255, 255, 255)
                             text_color = RGBColor(0, 0, 0)
                             accent_color = RGBColor(0, 0, 255)
                        elif "Golden" in current_style:
                             accent_color = RGBColor(218, 165, 32)
                        
                        # -- Title Slide --
                        blank_slide_layout = prs.slide_layouts[6] 
                        slide = prs.slides.add_slide(blank_slide_layout)
                        
                        # Background Image Logic
                        if 'generated_image' in st.session_state:
                            img_url = st.session_state['generated_image']
                            response = requests.get(img_url)
                            if response.status_code == 200:
                                image_data = io.BytesIO(response.content)
                                slide.shapes.add_picture(image_data, 0, 0, width=prs.slide_width, height=prs.slide_height)

                        # Title Box
                        textbox = slide.shapes.add_textbox(Inches(1), Inches(3), Inches(14), Inches(2))
                        tf = textbox.text_frame
                        p = tf.add_paragraph()
                        p.text = "REEL INSIGHTS"
                        p.font.size = Pt(80)
                        p.font.color.rgb = text_color
                        p.font.bold = True
                        
                        # Content Slides
                        if "slides" in slides_data: 
                            slides_list = slides_data["slides"]
                        else:
                            slides_list = slides_data.values() 

                        for slide_info in list(slides_list)[:7]: 
                            slide = prs.slides.add_slide(blank_slide_layout)
                            
                            # Solid Background for Content Slides relative to theme
                            background = slide.background
                            fill = background.fill
                            fill.solid()
                            fill.fore_color.rgb = bg_color

                            # Header
                            shapes = slide.shapes
                            title_box = shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(15), Inches(1.5))
                            tf = title_box.text_frame
                            p = tf.add_paragraph()
                            p.text = slide_info.get("title", "Insight").upper()
                            p.font.size = Pt(44)
                            p.font.color.rgb = accent_color
                            p.font.bold = True
                            
                            # Content
                            content_box = shapes.add_textbox(Inches(1), Inches(2.5), Inches(14), Inches(5))
                            tf = content_box.text_frame
                            content = slide_info.get("content", [])
                            
                            if isinstance(content, list):
                                for point in content:
                                    p = tf.add_paragraph()
                                    p.text = f"• {point}"
                                    p.font.size = Pt(28)
                                    p.font.color.rgb = text_color
                                    p.space_after = Pt(20)
                            else:
                                p = tf.add_paragraph()
                                p.text = str(content)
                                p.font.size = Pt(28)
                                p.font.color.rgb = text_color

                        # 3. Save to Buffer
                        pptx_stream = io.BytesIO()
                        prs.save(pptx_stream)
                        pptx_stream.seek(0)
                        
                        st.download_button(
                            label="📥 DOWNLOAD DECK",
                            data=pptx_stream,
                            file_name="reel_insights.pptx",
                            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
                        )
                        st.success("MISSION COMPLETE")

                    except Exception as e:
                        st.error(f"PPTX Error: {e}")

        # --- Data Charts ---
        if st.button("📈 Extract & Chart Data"):
            if openai_client:
                with st.spinner("Analyzing for Data..."):
                    try:
                        # 1. Extract Data
                        data_prompt = f"Extract any numerical data, trends, or stats from this text. If none, invent plausible engagement metrics (Views, Likes, Shares) based on the content tone. Return a simple JSON key-value pair for a bar chart. JSON ONLY.\n\nText: {selected_source.get('text')}"
                        response = openai_client.chat.completions.create(model="gpt-3.5-turbo", response_format={ "type": "json_object" }, messages=[{"role": "user", "content": data_prompt}])
                        import json
                        chart_data = json.loads(response.choices[0].message.content)
                        
                        # 2. Render Chart
                        st.bar_chart(chart_data)
                        st.caption("Data extracted or estimated from transcript context.")
                        
                    except Exception as e:
                        st.error(f"Chart Error: {e}")
