import streamlit as st
import pandas as pd
from datetime import datetime
import uuid
from agent_logic import ContentStrategyAgent
from utils import track_metric, load_metrics, save_feedback
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="Content Strategy Agent",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for user tracking
if 'user_id' not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())
if 'strategies_created' not in st.session_state:
    st.session_state.strategies_created = 0
if 'has_used_tool' not in st.session_state:
    st.session_state.has_used_tool = False

# Custom CSS for better UI
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .stButton>button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
        font-weight: bold;
        padding: 0.5rem;
        border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar navigation
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2920/2920277.png", width=100)
    st.title("Navigation")
    page = st.radio("Go to", ["Content Strategy Generator", "Metrics Dashboard", "About"])
    
    st.markdown("---")
    st.markdown("### 📊 Your Session Stats")
    st.metric("Strategies Created", st.session_state.strategies_created)

# Main content area
if page == "Content Strategy Generator":
    st.markdown('<div class="main-header">📝 Content Strategy Agent</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">AI-powered content planning in minutes, not days</div>', unsafe_allow_html=True)
    
    # Input form
    with st.form("strategy_form"):
        st.subheader("Tell us about your content needs")
        
        col1, col2 = st.columns(2)
        
        with col1:
            business_type = st.text_input(
                "Business/Website Type",
                placeholder="e.g., SaaS startup, E-commerce store, Personal blog",
                help="What kind of business or website do you have?"
            )
            
            target_audience = st.text_area(
                "Target Audience",
                placeholder="e.g., Small business owners, Tech enthusiasts, Fitness beginners",
                help="Who are you trying to reach with your content?",
                height=100
            )
        
        with col2:
            industry = st.text_input(
                "Industry/Niche",
                placeholder="e.g., Digital Marketing, Health & Wellness, Finance",
                help="What industry or niche do you operate in?"
            )
            
            content_goals = st.text_area(
                "Content Goals",
                placeholder="e.g., Increase organic traffic, Build brand authority, Generate leads",
                help="What do you want to achieve with your content?",
                height=100
            )
        
        # Additional optional parameters
        with st.expander("Advanced Options (Optional)"):
            keywords = st.text_input(
                "Target Keywords (comma-separated)",
                placeholder="e.g., content marketing, SEO tips, social media strategy",
                help="Any specific keywords you want to target?"
            )
            
            content_type = st.selectbox(
                "Preferred Content Type",
                ["Blog Posts", "How-to Guides", "Listicles", "Case Studies", "News/Trends", "Mixed"]
            )
            
            num_topics = st.slider(
                "Number of Topic Suggestions",
                min_value=3,
                max_value=10,
                value=5,
                help="How many blog topic ideas do you want?"
            )
        
        submit_button = st.form_submit_button("🚀 Generate Content Strategy")
    
    # Process form submission
    if submit_button:
        # Validation
        if not business_type or not target_audience or not industry:
            st.error("⚠️ Please fill in all required fields: Business Type, Target Audience, and Industry")
        else:
            # Track activation metric (first use)
            if not st.session_state.has_used_tool:
                track_metric(
                    user_id=st.session_state.user_id,
                    metric_type='activation',
                    value=1
                )
                st.session_state.has_used_tool = True
            
            # Track engagement metric (strategy created)
            track_metric(
                user_id=st.session_state.user_id,
                metric_type='engagement',
                value=1
            )
            st.session_state.strategies_created += 1
            
            # Show loading message
            with st.spinner("🤖 AI Agent is analyzing your audience and researching trending topics..."):
                try:
                    # Initialize agent and generate strategy
                    agent = ContentStrategyAgent()
                    
                    strategy = agent.generate_strategy(
                        business_type=business_type,
                        target_audience=target_audience,
                        industry=industry,
                        content_goals=content_goals,
                        keywords=keywords if keywords else None,
                        content_type=content_type,
                        num_topics=num_topics
                    )
                    
                    # Display results
                    st.success("✅ Your content strategy is ready!")
                    
                    # Audience Analysis
                    st.markdown("## 🎯 Audience Analysis")
                    st.info(strategy['audience_analysis'])
                    
                    # Trending Topics
                    st.markdown("## 📈 Trending Topics in Your Industry")
                    st.warning(strategy['trending_topics'])
                    
                    # Blog Topic Suggestions
                    st.markdown("## 💡 Blog Topic Suggestions")
                    for i, topic in enumerate(strategy['blog_topics'], 1):
                        with st.expander(f"📝 Topic {i}: {topic['title']}", expanded=(i==1)):
                            st.markdown(f"**Rationale:** {topic['rationale']}")
                            st.markdown(f"**Target Keyword:** `{topic['keyword']}`")
                            st.markdown(f"**Estimated Search Volume:** {topic['search_volume']}")
                            
                            st.markdown("### Outline")
                            for section in topic['outline']:
                                st.markdown(f"- {section}")
                            
                            st.markdown("### SEO Recommendations")
                            for rec in topic['seo_recommendations']:
                                st.markdown(f"- {rec}")
                    
                    # General SEO Recommendations
                    st.markdown("## 🔍 General SEO Strategy")
                    for rec in strategy['general_seo']:
                        st.markdown(f"- {rec}")
                    
                    # Satisfaction rating
                    st.markdown("---")
                    st.markdown("### 📊 How helpful was this strategy?")
                    
                    col1, col2, col3, col4, col5 = st.columns(5)
                    with col1:
                        if st.button("⭐ 1"):
                            save_feedback(st.session_state.user_id, 1)
                            st.success("Thanks for your feedback!")
                    with col2:
                        if st.button("⭐⭐ 2"):
                            save_feedback(st.session_state.user_id, 2)
                            st.success("Thanks for your feedback!")
                    with col3:
                        if st.button("⭐⭐⭐ 3"):
                            save_feedback(st.session_state.user_id, 3)
                            st.success("Thanks for your feedback!")
                    with col4:
                        if st.button("⭐⭐⭐⭐ 4"):
                            save_feedback(st.session_state.user_id, 4)
                            st.success("Thanks for your feedback!")
                    with col5:
                        if st.button("⭐⭐⭐⭐⭐ 5"):
                            save_feedback(st.session_state.user_id, 5)
                            st.success("Thanks for your feedback!")
                
                except Exception as e:
                    st.error(f"❌ An error occurred: {str(e)}")
                    st.info("Please check your API key in the .env file or try again.")

elif page == "Metrics Dashboard":
    st.markdown('<div class="main-header">📊 Growth Metrics Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Track your product\'s performance</div>', unsafe_allow_html=True)
    
    try:
        # Load metrics data
        df = load_metrics()
        
        if df.empty:
            st.info("📭 No metrics data yet. Start generating content strategies to see your metrics here!")
        else:
            # Key Metrics Overview
            st.markdown("## 🎯 Key Performance Indicators")
            
            col1, col2, col3, col4 = st.columns(4)
            
            # Activation Rate
            total_users = df['user_id'].nunique()
            activated_users = df[df['metric_type'] == 'activation']['user_id'].nunique()
            activation_rate = (activated_users / total_users * 100) if total_users > 0 else 0
            
            with col1:
                st.metric(
                    "Activation Rate",
                    f"{activation_rate:.1f}%",
                    help="Percentage of users who used the tool"
                )
            
            # Total Strategies Created
            total_strategies = df[df['metric_type'] == 'engagement']['value'].sum()
            
            with col2:
                st.metric(
                    "Strategies Created",
                    f"{int(total_strategies)}",
                    help="Total number of content strategies generated"
                )
            
            # Retention Rate (users who came back after 1 week)
            retention_users = df[df['metric_type'] == 'retention']['user_id'].nunique()
            retention_rate = (retention_users / activated_users * 100) if activated_users > 0 else 0
            
            with col3:
                st.metric(
                    "1-Week Retention",
                    f"{retention_rate:.1f}%",
                    help="Percentage of users returning after 1 week"
                )
            
            # Average Satisfaction
            satisfaction_df = df[df['metric_type'] == 'satisfaction']
            avg_satisfaction = satisfaction_df['value'].mean() if not satisfaction_df.empty else 0
            
            with col4:
                st.metric(
                    "Avg. Satisfaction",
                    f"{avg_satisfaction:.2f} / 5.0",
                    help="Average user satisfaction rating"
                )
            
            st.markdown("---")
            
            # Visualizations
            col1, col2 = st.columns(2)
            
            with col1:
                # Strategies over time
                st.markdown("### 📈 Strategies Created Over Time")
                engagement_df = df[df['metric_type'] == 'engagement'].copy()
                engagement_df['date'] = pd.to_datetime(engagement_df['timestamp']).dt.date
                daily_strategies = engagement_df.groupby('date')['value'].sum().reset_index()
                
                if not daily_strategies.empty:
                    fig = px.line(
                        daily_strategies,
                        x='date',
                        y='value',
                        title='Daily Content Strategies Generated',
                        labels={'value': 'Strategies', 'date': 'Date'}
                    )
                    fig.update_traces(line_color='#1f77b4', line_width=3)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No engagement data yet")
            
            with col2:
                # Satisfaction distribution
                st.markdown("### ⭐ Satisfaction Rating Distribution")
                if not satisfaction_df.empty:
                    rating_counts = satisfaction_df['value'].value_counts().sort_index()
                    
                    fig = go.Figure(data=[
                        go.Bar(
                            x=[f"{int(x)} Stars" for x in rating_counts.index],
                            y=rating_counts.values,
                            marker_color='#ff7f0e'
                        )
                    ])
                    fig.update_layout(
                        title='User Satisfaction Ratings',
                        xaxis_title='Rating',
                        yaxis_title='Count'
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No satisfaction ratings yet")
            
            # Detailed metrics table
            st.markdown("### 📋 Detailed Metrics Log")
            with st.expander("View Raw Data"):
                st.dataframe(
                    df.sort_values('timestamp', ascending=False),
                    use_container_width=True
                )
                
                # Download button
                csv = df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Metrics CSV",
                    data=csv,
                    file_name=f"metrics_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
    
    except Exception as e:
        st.error(f"Error loading metrics: {str(e)}")

else:  # About page
    st.markdown('<div class="main-header">ℹ️ About Content Strategy Agent</div>', unsafe_allow_html=True)
    
    st.markdown("""
    ## 🎯 What is this?
    
    The Content Strategy Agent is an AI-powered tool that helps content teams plan their content strategy in minutes instead of days.
    
    ## ✨ Features
    
    1. **Audience Analysis** - Understand your target audience's needs, pain points, and preferences
    2. **Trend Research** - Discover what's trending in your industry right now
    3. **Topic Suggestions** - Get data-driven blog topic ideas with high potential
    4. **Content Outlines** - Receive structured outlines for each topic
    5. **SEO Recommendations** - Get actionable SEO tips to rank higher
    
    ## 🚀 How to Use
    
    1. Navigate to the **Content Strategy Generator**
    2. Fill in your business details, target audience, and goals
    3. Click "Generate Content Strategy"
    4. Review your personalized strategy
    5. Rate your experience to help us improve
    
    ## 📊 Growth Metrics
    
    We track four key metrics to improve the product:
    
    - **Activation**: % of users who try the tool
    - **Engagement**: Number of strategies created
    - **Retention**: % of users returning after 1 week
    - **Satisfaction**: Average user rating (1-5)
    
    ## 🔧 Technical Stack
    
    - **Frontend**: Streamlit
    - **AI Agent**: Claude API (Anthropic)
    - **Deployment**: Streamlit Cloud
    - **Metrics**: CSV-based tracking
    
    ## 🤝 Feedback
    
    Your feedback helps us improve! Please rate each strategy you generate.
    
    ---
    
    **Built with ❤️ using Claude AI**
    """)
    
    st.markdown("### 🔒 Privacy & Data")
    st.info("""
    - We generate anonymous user IDs for tracking
    - No personal information is collected
    - Metrics are stored locally in CSV files
    - Your content strategy inputs are processed by Claude API
    """)
