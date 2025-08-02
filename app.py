# app.py
import streamlit as st

# --- Page Configuration ---
st.set_page_config(
    page_title="StudyMate AI",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for styling
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        html, body, [class*="st-"] {
            font-family: 'Inter', sans-serif;
            color: #1e293b;
            background-color: #f8fafc;
        }
        .st-emotion-cache-12fmw35 { color: #0f172a; }
        .st-emotion-cache-1s0a3v0 {
            background-color: #fff;
            border-radius: 12px;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
            transition: all 0.3s ease;
        }
        .st-emotion-cache-1s0a3v0:hover { transform: translateY(-4px); }
        .st-emotion-cache-1ghh37k {
            border-radius: 12px;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
            transition: all 0.3s ease;
        }
        .st-emotion-cache-1ghh37k:hover { transform: translateY(-4px); }
        .stButton button {
            transition: all 0.3s ease;
            font-weight: 500;
            border-radius: 6px;
        }
        .stButton button:hover { transform: scale(1.05); }
        .button-hero {
            background-image: linear-gradient(to right, #4f46e5, #7c3aed);
            color: white !important;
            border: none;
            padding: 1rem 2rem;
            font-size: 1.25rem;
            border-radius: 9999px;
            font-weight: bold;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        }
        .button-hero:hover { box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.05); }
        .feature-icon-container {
            width: 48px;
            height: 48px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 1rem;
            transition: transform 0.3s ease;
        }
        .feature-card:hover .feature-icon-container { transform: scale(1.1); }
        .feature-card {
            background-color: white;
            border-radius: 12px;
            padding: 24px;
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
            transition: all 0.3s ease;
        }
        .feature-card:hover {
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
            transform: translateY(-4px);
        }
        .bg-gradient-primary {
            background-image: linear-gradient(to right, #4f46e5, #7c3aed);
        }
        .bg-gradient-subtle {
            background-image: linear-gradient(to right, #f1f5f9, #e2e8f0);
            border-radius: 16px;
            padding: 3rem;
            margin-top: 3rem;
        }
    </style>
""", unsafe_allow_html=True)


st.title("StudyMate AI")
st.markdown("<h2 class='text-center text-3xl font-bold mb-4'>Everything You Need to <span class='bg-gradient-primary bg-clip-text text-transparent'> Learn Smarter</span></h2>", unsafe_allow_html=True)
st.markdown("<p class='text-center text-lg text-muted-foreground max-w-2xl mx-auto'>StudyMate combines multiple AI-powered tools into one seamless learning experience. Transform any PDF into an interactive study session.</p>", unsafe_allow_html=True)

st.markdown("---")

# The features data, with updated titles
features = [
    {"icon": "💬", "title": "Chat with StudyMate", "description": "Ask questions about your PDFs in natural language and get accurate, context-aware answers instantly.", "color": "#3b82f6"},
    {"icon": "🧠", "title": "Custom Quizzes", "description": "Generate personalized quizzes with Easy, Medium, or Hard difficulty levels to test your understanding.", "color": "#a855f7"},
    {"icon": "📝", "title": "Flashcard Generator", "description": "Automatically convert key concepts from your documents into interactive flashcards for quick revision.", "color": "#22c55e"},
    {"icon": "📖", "title": "Summary & Highlights", "description": "Instantly generate comprehensive summaries highlighting key points, formulas, and definitions.", "color": "#6366f1"},
    {"icon": "🎬", "title": "Video Recommendations", "description": "Discover relevant educational videos based on your questions and study topics for deeper learning.", "color": "#ef4444"},
    {"icon": "💡", "title": "Answer Clarification", "description": "Get complex topics explained in simpler terms when you need clarification on any concept.", "color": "#eab308"},
]

# Create a grid of features using Streamlit columns.
cols = st.columns(3)
for i, feature in enumerate(features):
    with cols[i % 3]:
        st.markdown(f"""
            <div class="feature-card">
                <div class="feature-icon-container" style="background-color: {feature['color']}1A;">
                    <span style="font-size: 24px;">{feature['icon']}</span>
                </div>
                <h3 style="font-size: 1.25rem; font-weight: 600; color: #0f172a;">{feature['title']}</h3>
                <p style="color: #64748b;">{feature['description']}</p>
            </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# "How it Works" section with custom styling.
with st.container():
    st.markdown("""
        <div class="bg-gradient-subtle">
            <div style="text-align: center; margin-bottom: 2rem;">
                <h3 style="font-size: 1.875rem; font-weight: 700; color: #0f172a;">How StudyMate Works</h3>
                <p style="color: #64748b; font-size: 1.125rem;">Get started in three simple steps</p>
            </div>
            <div class="grid md:grid-cols-3 gap-8">
    """, unsafe_allow_html=True)

    cols = st.columns(3)
    with cols[0]:
        st.markdown("""
            <div style="text-align: center;">
                <div style="width: 64px; height: 64px; background-color: #4f46e51a; border-radius: 9999px; display: flex; align-items: center; justify-content: center; margin: auto; margin-bottom: 1rem;">
                    <span style="font-size: 1.5rem; font-weight: bold; color: #4f46e5;">1</span>
                </div>
                <h4 style="font-size: 1.25rem; font-weight: 600; color: #0f172a; margin-bottom: 0.5rem;">Upload</h4>
                <p style="color: #64748b;">Drag and drop your PDF study materials or textbooks</p>
            </div>
        """, unsafe_allow_html=True)
    with cols[1]:
        st.markdown("""
            <div style="text-align: center;">
                <div style="width: 64px; height: 64px; background-color: #7c3aed1a; border-radius: 9999px; display: flex; align-items: center; justify-content: center; margin: auto; margin-bottom: 1rem;">
                    <span style="font-size: 1.5rem; font-weight: bold; color: #7c3aed;">2</span>
                </div>
                <h4 style="font-size: 1.25rem; font-weight: 600; color: #0f172a; margin-bottom: 0.5rem;">Ask</h4>
                <p style="color: #64748b;">Ask questions, request quizzes, or generate flashcards</p>
            </div>
        """, unsafe_allow_html=True)
    with cols[2]:
        st.markdown("""
            <div style="text-align: center;">
                <div style="width: 64px; height: 64px; background-color: #4f46e51a; border-radius: 9999px; display: flex; align-items: center; justify-content: center; margin: auto; margin-bottom: 1rem;">
                    <span style="font-size: 1.5rem; font-weight: bold; color: #4f46e5;">3</span>
                </div>
                <h4 style="font-size: 1.25rem; font-weight: 600; color: #0f172a; margin-bottom: 0.5rem;">Learn</h4>
                <p style="color: #64748b;">Get instant answers and interactive study materials</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)