"""
UI Components Demo - Streamlit Frontend UI Skills Showcase
============================================================
This file demonstrates various UI component libraries installed in the project.
Run: streamlit run ui_components_demo.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import altair as alt
from datetime import datetime
import matplotlib.pyplot as plt

# Page Configuration
st.set_page_config(
    page_title="UI Components Showcase",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for enhanced styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 2rem 0;
    }
    .feature-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    }
    .code-block {
        background: #1e1e1e;
        padding: 1rem;
        border-radius: 5px;
        color: #d4d4d4;
        font-family: 'Courier New', monospace;
        overflow-x: auto;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">🎨 Frontend UI Skills Showcase</div>', unsafe_allow_html=True)

# Sidebar Navigation
from streamlit_option_menu import option_menu

with st.sidebar:
    selected = option_menu(
        menu_title="Navigation",
        options=["Overview", "Charts", "Data Display", "Interactive Elements", "Forms", "Layouts", "Advanced"],
        icons=["house", "bar-chart", "table", "sliders", "inputs", "grid", "stars"],
        menu_icon="cast",
        default_index=0,
    )

# ==================== OVERVIEW PAGE ====================
if selected == "Overview":
    st.title("📚 Installed UI Libraries")

    st.markdown("### Core Streamlit Components")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Libraries", "15+", "Newly Added")
    with col2:
        st.metric("Chart Types", "5", "Different Libraries")
    with col3:
        st.metric("Components", "50+", "Ready to Use")

    st.markdown("---")

    st.markdown("### 🎯 Installed Libraries")

    libraries = {
        "📊 Data Visualization": [
            "Plotly (Interactive Charts)",
            "Altair (Declarative Visualization)",
            "Seaborn (Statistical Graphics)",
            "Pyecharts (Chinese Charts)",
        ],
        "🧩 UI Components": [
            "Streamlit Extras (20+ Components)",
            "Streamlit Elements (Material UI)",
            "Streamlit AgGrid (Data Grid)",
            "Streamlit Shadcn UI (Modern Components)",
        ],
        "🎨 Interactive": [
            "Streamlit Option Menu (Navigation)",
            "Streamlit Modal (Dialogs)",
            "Streamlit JavaScript (JS Integration)",
            "Streamlit Lottie (Animations)",
        ],
        "🔐 Advanced": [
            "Streamlit Authenticator (Auth)",
            "Extra Streamlit Components",
        ]
    }

    for category, libs in libraries.items():
        with st.expander(f"**{category}**"):
            for lib in libs:
                st.markdown(f"✅ {lib}")

    st.info("💡 **Tip**: Use the sidebar navigation to explore different UI components!")

# ==================== CHARTS PAGE ====================
elif selected == "Charts":
    st.title("📊 Data Visualization Libraries")

    tab1, tab2, tab3, tab4 = st.tabs(["Plotly", "Altair", "Seaborn", "Pyecharts"])

    with tab1:
        st.subheader("📈 Plotly Charts")

        # Generate sample data
        df = pd.DataFrame({
            'x': np.linspace(0, 10, 100),
            'y': np.sin(np.linspace(0, 10, 100)),
            'category': np.random.choice(['A', 'B', 'C'], 100)
        })

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Line Chart**")
            fig_line = px.line(df, x='x', y='y', title='Sine Wave')
            st.plotly_chart(fig_line, use_container_width=True)

        with col2:
            st.markdown("**Scatter Plot**")
            fig_scatter = px.scatter(df, x='x', y='y', color='category', title='Scatter Plot')
            st.plotly_chart(fig_scatter, use_container_width=True)

        # 3D Surface Plot
        st.markdown("**3D Surface Plot**")
        fig_3d = go.Figure(data=[go.Surface(z=np.random.randn(20, 20))])
        fig_3d.update_layout(title='3D Surface', autosize=False)
        st.plotly_chart(fig_3d, use_container_width=True)

    with tab2:
        st.subheader("📊 Altair Charts")

        # Bar Chart
        source = pd.DataFrame({
            'Category': ['A', 'B', 'C', 'D'],
            'Value': [28, 55, 43, 91]
        })

        bar_chart = alt.Chart(source).mark_bar().encode(
            x='Category',
            y='Value',
            color=alt.Color('Category', scale=alt.Scale(scheme='category10'))
        ).properties(width=600, height=400)

        st.altair_chart(bar_chart, use_container_width=True)

        # Scatter Plot with Regression
        scatter_data = pd.DataFrame({
            'x': np.random.randn(100),
            'y': np.random.randn(100)
        })

        scatter_chart = alt.Chart(scatter_data).mark_circle(size=60).encode(
            x='x', y='y', tooltip=['x', 'y']
        ).interactive()

        st.altair_chart(scatter_chart, use_container_width=True)

    with tab3:
        st.subheader("🔥 Seaborn Statistical Charts")

        # Distribution Plot
        fig, ax = plt.subplots()
        sns.histplot(data=np.random.randn(1000), kde=True, ax=ax)
        ax.set_title('Distribution Plot')
        st.pyplot(fig)

        # Heatmap
        fig2, ax2 = plt.subplots(figsize=(8, 6))
        data = np.random.randn(10, 10)
        sns.heatmap(data, annot=True, fmt='.2f', cmap='coolwarm', ax=ax2)
        ax2.set_title('Heatmap')
        st.pyplot(fig2)

    with tab4:
        st.subheader("🇨🇳 Pyecharts (Chinese Charts)")

        from streamlit_echarts import st_echarts
        from pyecharts import options as opts
        from pyecharts.charts import Bar

        # Simple Bar Chart
        options = {
            "xAxis": {
                "type": "category",
                "data": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
            },
            "yAxis": {"type": "value"},
            "series": [{
                "data": [120, 200, 150, 80, 70, 110, 130],
                "type": "bar",
                "itemStyle": {"color": "#667eea"}
            }],
            "tooltip": {"trigger": "axis"}
        }

        st_echarts(options=options, height="400px")

# ==================== DATA DISPLAY PAGE ====================
elif selected == "Data Display":
    st.title("📋 Data Display Components")

    # Sample Data
    df = pd.DataFrame({
        'Name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve'],
        'Age': [25, 30, 35, 28, 32],
        'City': ['NYC', 'LA', 'Chicago', 'Houston', 'Phoenix'],
        'Score': [85, 92, 78, 88, 95]
    })

    tab1, tab2, tab3 = st.tabs(["Basic Tables", "AgGrid", "Styled Dataframe"])

    with tab1:
        st.subheader("📊 Standard Streamlit Tables")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Static Table**")
            st.table(df)

        with col2:
            st.markdown("**Dynamic Dataframe**")
            st.dataframe(df, use_container_width=True)

    with tab2:
        st.subheader("🔲 AgGrid - Advanced Data Grid")

        from st_aggrid import AgGrid, GridUpdateMode, DataReturnMode, GridOptionsBuilder

        gb = GridOptionsBuilder.from_dataframe(df)
        gb.configure_pagination(paginationAutoPageSize=True)
        gb.configure_side_bar()
        gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc='sum', editable=True)
        gb.configure_grid_options(domLayout='normal')
        gridOptions = gb.build()

        AgGrid(
            df,
            gridOptions=gridOptions,
            enable_enterprise_modules=True,
            update_mode=GridUpdateMode.MODEL_CHANGED,
            data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
            height=400,
            theme='streamlit',
            fit_columns_on_grid_load=False
        )

    with tab3:
        st.subheader("🎨 Styled Dataframe")

        styled_df = df.style.applymap(
            lambda x: 'background-color: #ffcccc' if x < 80 else 'background-color: #ccffcc',
            subset=['Score']
        ).format({'Score': '{:.0f}'})

        st.dataframe(styled_df, use_container_width=True)

        # Metric Cards
        st.subheader("📈 Metric Cards")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Records", len(df), "+5%")
        with col2:
            st.metric("Average Age", f"{df['Age'].mean():.1f}", "+2.3")
        with col3:
            st.metric("Max Score", df['Score'].max(), "+8")
        with col4:
            st.metric("Cities", df['City'].nunique(), "Unique")

# ==================== INTERACTIVE ELEMENTS PAGE ====================
elif selected == "Interactive Elements":
    st.title("🎛️ Interactive Components")

    # Streamlit Extras Components
    from streamlit_extras.colored_header import colored_header
    from streamlit_extras.badges import badge
    from streamlit_extras.mention import mention
    from streamlit_extras.card import card
    from streamlit_extras.metric_cards import style_metric_cards

    # Colored Header
    colored_header(
        label="🎨 Streamlit Extras Components",
        description="Enhanced UI components from streamlit-extras",
        color_name="violet-70"
    )

    # Badges
    st.subheader("🏷️ Badges")
    col1, col2, col3 = st.columns(3)
    with col1:
        badge(type="github", name="streamlit-extras")
    with col2:
        badge(type="pypi", name="streamlit")
    with col3:
        badge(type="uv", name="Python 3.9+")

    # Cards
    st.subheader("🃏 Feature Cards")
    col1, col2 = st.columns(2)

    with col1:
        card(
            title="Interactive Charts",
            text="Create beautiful, interactive charts with Plotly, Altair, and more.",
            image="https://via.placeholder.com/300x200"
        )

    with col2:
        card(
            title="Modern UI",
            text="Build modern interfaces with Shadcn UI and Streamlit Elements.",
            image="https://via.placeholder.com/300x200"
        )

    # Styled Metric Cards
    st.subheader("📊 Styled Metrics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Users", "12,345", "+15%")
    col2.metric("Revenue", "$45,678", "+8.2%")
    col3.metric("Growth", "+23.5%", "+2.1%")
    style_metric_cards(background_color="#1e1e1e", border_left_color="#667eea")

    # Sliders and Input
    st.subheader("🎚️ Interactive Controls")

    col1, col2 = st.columns(2)

    with col1:
        value = st.slider(
            "Select a value",
            min_value=0,
            max_value=100,
            value=50,
            step=1
        )
        st.write(f"Selected: {value}")

    with col2:
        options = st.multiselect(
            "Select options",
            ["Option 1", "Option 2", "Option 3", "Option 4"],
            default=["Option 1"]
        )
        st.write(f"Selected: {options}")

    # Toggle Switch (from streamlit-extras)
    from streamlit_extras.toggle_switch import st_toggle_switch

    st.subheader("🔘 Toggle Switches")
    col1, col2, col3 = st.columns(3)
    with col1:
        switch1 = st_toggle_switch("Dark Mode", key="switch1")
    with col2:
        switch2 = st_toggle_switch("Notifications", key="switch2", default_active=True)
    with col3:
        switch3 = st_toggle_switch("Auto-save", key="switch3")

# ==================== FORMS PAGE ====================
elif selected == "Forms":
    st.title("📝 Form Components")

    # Form with Streamlit Authenticator
    st.subheader("🔐 Authentication Form (Demo)")

    col1, col2 = st.columns([1, 1])

    with col1:
        with st.form("login_form"):
            st.markdown("### Login")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            remember = st.checkbox("Remember me")
            submitted = st.form_submit_button("Login")

            if submitted:
                st.success(f"Welcome, {username}! (Demo)")

    with col2:
        with st.form("signup_form"):
            st.markdown("### Sign Up")
            email = st.text_input("Email")
            username2 = st.text_input("Username")
            password2 = st.text_input("Password", type="password")
            confirm = st.text_input("Confirm Password", type="password")

            terms = st.checkbox("I agree to the Terms and Conditions")

            submitted2 = st.form_submit_button("Create Account")

            if submitted2 and terms:
                st.success("Account created! (Demo)")

    # File Upload
    st.subheader("📁 File Upload")
    uploaded_file = st.file_uploader(
        "Choose a file",
        type=['csv', 'xlsx', 'png', 'jpg'],
        accept_multiple_files=True
    )

    if uploaded_file:
        for file in uploaded_file:
            st.write(f"✅ {file.name} ({file.size} bytes)")

    # Text Area with Character Count
    st.subheader("✍️ Text Input")
    from streamlit_extras.word_optimize import optimize_text

    text = st.text_area("Enter your text", height=150)

    if text:
        st.write(f"Character count: {len(text)}")

    # Date and Time Input
    col1, col2, col3 = st.columns(3)
    with col1:
        date = st.date_input("Select Date")
    with col2:
        time = st.time_input("Select Time")
    with col3:
        daterange = st.date_input("Date Range", value=(datetime.now(), datetime.now()))

# ==================== LAYOUTS PAGE ====================
elif selected == "Layouts":
    st.title("📐 Layout Components")

    # Columns Layout
    st.subheader("📊 Columns Layout")
    col1, col2, col3 = st.columns(3, gap="medium")

    with col1:
        st.info("Column 1")
        st.write("Content here")

    with col2:
        st.warning("Column 2")
        st.write("Content here")

    with col3:
        st.error("Column 3")
        st.write("Content here")

    # Tabs Layout
    st.subheader("📑 Tabs Layout")
    tab1, tab2, tab3 = st.tabs(["Tab 1", "Tab 2", "Tab 3"])

    with tab1:
        st.write("Content for Tab 1")
        st.code("print('Hello from Tab 1')")

    with tab2:
        st.write("Content for Tab 2")
        st.balloons()

    with tab3:
        st.write("Content for Tab 3")
        st.snow()

    # Expander and Accordion
    st.subheader("📁 Expanders")

    with st.expander("📖 Click to expand"):
        st.write("This is an expander!")
        st.slider("Slider inside expander", 0, 100, 50)

    with st.expander("🔧 Settings"):
        st.checkbox("Enable notifications")
        st.selectbox("Language", ["English", "Spanish", "French"])

    # Container and Blocks
    st.subheader("📦 Containers")

    with st.container():
        st.markdown("### Container Content")
        st.write("This is inside a container")
        col1, col2 = st.columns(2)
        col1.button("Button 1")
        col2.button("Button 2")

    # Sidebar Content
    st.subheader("🎛️ Sidebar Elements")
    st.write("(See the sidebar for interactive elements)")

# ==================== ADVANCED PAGE ====================
elif selected == "Advanced":
    st.title("🚀 Advanced Components")

    # Modal Dialog
    from streamlit_modal import Modal

    st.subheader("🪟 Modal Dialogs")

    if st.button("Open Modal"):
        modal = Modal(
            key="demo_modal",
            title="This is a Modal!",
            padding="20px",
            max_width="500px"
        )

        if modal.is_open():
            with modal.container():
                st.write("This is a modal dialog!")
                st.slider("Slider in modal", 0, 100, 50)
                if st.button("Close"):
                    modal.close()

    # Lottie Animation
    st.subheader("🎬 Lottie Animations")
    from streamlit_lottie import st_lottie

    lottie_url = "https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json"
    st_lottie(lottie_url, height=200, key="demo")

    # JavaScript Execution
    st.subheader("⚡ JavaScript Integration")
    from streamlit_javascript import st_javascript

    if st.button("Run JavaScript"):
        st_javascript("alert('Hello from JavaScript!')")

    # Progress Bars
    st.subheader("📊 Progress Indicators")

    # Progress bar
    progress = st.progress(0)
    for i in range(100):
        progress.progress(i + 1)

    # Spinner
    with st.spinner('Loading...'):
        import time
        time.sleep(2)
    st.success('Done!')

    # Status Messages
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.info("ℹ️ Info message")
    with col2:
        st.success("✅ Success message")
    with col3:
        st.warning("⚠️ Warning message")
    with col4:
        st.error("❌ Error message")

    # Annotated Text
    from streamlit_extras.annotated_text import annotated_text

    st.subheader("📝 Annotated Text")
    annotated_text(
        "This ",
        ("is", "highlighted", "#faa"),
        ("annotated", "text", "#fea"),
        " example!",
    )

    # Toast Notification
    from streamlit_extras.notify import st_notify

    st.subheader("🔔 Toast Notifications")
    if st.button("Show Notification"):
        st_notify(
            message="This is a notification!",
            type="success",
            duration=3
        )

    # Code Block with Syntax Highlighting
    st.subheader("💻 Code Display")
    st.code("""
import streamlit as st

st.title("Hello World")
st.write("This is a code block!")
    """, language="python")

# ==================== FOOTER ====================
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        <p>🎨 UI Components Demo | Built with Streamlit</p>
        <p>Powered by 15+ UI libraries</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Display Session State
with st.expander("🔧 Debug Info"):
    st.write("### Session State")
    st.json(st.session_state)
