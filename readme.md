# 📝 Content Strategy Agent - Production Deployment Guide

An AI-powered content strategy agent that helps content teams plan their content in minutes instead of days. Built with Streamlit and Claude API.

## 🎯 Problem & Solution

**PROBLEM:** Content teams spend days planning what to write, researching topics, and developing strategies.

**SOLUTION:** An AI agent that:
1. Analyzes target audience
2. Researches trending topics  
3. Suggests blog topics
4. Generates content outlines
5. Provides SEO recommendations

## 📊 Growth Metrics Tracked

The application tracks four key product metrics:

1. **Activation Rate**: % of users who actually use the tool
2. **Engagement**: Number of content strategies created
3. **1-Week Retention**: % of users who return after 1 week
4. **Satisfaction**: Average user rating (1-5 stars)

All metrics are automatically tracked and visualized in the built-in dashboard.

## 🚀 Quick Start (5 Minutes)

### Prerequisites
- Python 3.9 or higher
- Anthropic API key ([Get one here](https://console.anthropic.com/))

### Local Setup

1. **Clone or download the project files**
```bash
# You should have these files:
# - app.py
# - agent_logic.py
# - utils.py
# - metrics.csv
# - requirements.txt
# - README.md
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up your API key**

Create a `.env` file in the project root:
```bash
ANTHROPIC_API_KEY=your_api_key_here
```

Alternatively, set it as an environment variable:
```bash
# On Mac/Linux
export ANTHROPIC_API_KEY='your_api_key_here'

# On Windows
set ANTHROPIC_API_KEY=your_api_key_here
```

4. **Run the application**
```bash
streamlit run app.py
```

5. **Open your browser**
The app should automatically open at `http://localhost:8501`

## ☁️ Deploy to Streamlit Cloud (Free)

Streamlit Cloud offers free hosting for public apps!

### Step-by-Step Deployment

1. **Push code to GitHub**
   - Create a new GitHub repository
   - Push all project files (app.py, agent_logic.py, utils.py, requirements.txt, metrics.csv)
   - Don't push your .env file!

2. **Go to Streamlit Cloud**
   - Visit [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub

3. **Deploy your app**
   - Click "New app"
   - Select your repository
   - Main file path: `app.py`
   - Click "Deploy"

4. **Add your API key**
   - Go to app settings (⚙️ icon)
   - Click "Secrets"
   - Add: `ANTHROPIC_API_KEY = "your_api_key_here"`
   - Save

5. **Your app is live!**
   - You'll get a URL like: `your-app-name.streamlit.app`
   - Share it with your team

## 📁 Project Structure

```
content-strategy-agent/
├── app.py                  # Main Streamlit application
├── agent_logic.py          # Claude API integration & AI logic
├── utils.py                # Metrics tracking utilities
├── metrics.csv             # Metrics storage (auto-generated)
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── .env                   # API key (don't commit!)
```

## 🔧 How It Works

### 1. User Flow
```
User Input → AI Agent → Claude API → Structured Output → Display Results → Track Metrics
```

### 2. Agent Logic (`agent_logic.py`)
- Constructs detailed prompts for Claude
- Calls Anthropic API with user inputs
- Parses structured responses
- Returns organized strategy data

### 3. Metrics Tracking (`utils.py`)
- Tracks events to CSV file
- Calculates growth metrics
- Provides dashboard data

### 4. Frontend (`app.py`)
- User-friendly Streamlit interface
- Three main pages:
  - Content Strategy Generator
  - Metrics Dashboard
  - About/Documentation
- Real-time metrics updates

## 📊 Understanding the Metrics

### Activation Rate
- **What it measures**: Did users actually try the tool?
- **How it's tracked**: First time a user generates a strategy
- **Good benchmark**: >40% is excellent

### Engagement (Strategies Created)
- **What it measures**: How much is the tool being used?
- **How it's tracked**: Every time "Generate Strategy" is clicked
- **Good benchmark**: 2+ strategies per activated user

### 1-Week Retention
- **What it measures**: Do users come back?
- **How it's tracked**: Users who return 7+ days after first use
- **Good benchmark**: >20% is good, >40% is excellent

### Satisfaction Rating
- **What it measures**: Are users happy with the output?
- **How it's tracked**: Star ratings (1-5) after each strategy
- **Good benchmark**: Average >4.0 is excellent

## 🎨 Customization Guide

### Change the Number of Topics
In `app.py`, modify the slider:
```python
num_topics = st.slider(
    "Number of Topic Suggestions",
    min_value=3,
    max_value=15,  # Increase max
    value=5
)
```

### Add More Content Types
In `app.py`, update the selectbox:
```python
content_type = st.selectbox(
    "Preferred Content Type",
    ["Blog Posts", "How-to Guides", "Listicles", 
     "Case Studies", "News/Trends", "Videos", "Podcasts", "Mixed"]
)
```

### Customize the Prompt
In `agent_logic.py`, modify the `_build_prompt()` method to adjust how the AI generates strategies.

### Change Colors/Theme
In `app.py`, update the CSS in the `st.markdown()` section:
```python
st.markdown("""
    <style>
    .main-header {
        color: #your_color_here;
    }
    </style>
""", unsafe_allow_html=True)
```

## 🐛 Troubleshooting

### "ANTHROPIC_API_KEY not found"
- Make sure you created a `.env` file with your API key
- Or set it as an environment variable
- For Streamlit Cloud, add it in the Secrets settings

### "Error calling Claude API"
- Check that your API key is valid
- Ensure you have API credits available
- Check your internet connection

### Metrics not showing
- Make sure `metrics.csv` exists in the same directory
- Check file permissions (needs write access)
- Try deleting `metrics.csv` - it will regenerate automatically

### Parsing errors
- The agent expects a specific format from Claude
- If parsing fails, the raw response is still shown
- Check `agent_logic.py` `_parse_response()` method

## 💡 Tips for Best Results

### For Users:
1. **Be specific** - The more details you provide, the better the strategy
2. **Define clear goals** - What success looks like for your content
3. **Know your audience** - Be detailed about who you're targeting
4. **Try different keywords** - Experiment with various keyword combinations

### For Developers:
1. **Monitor API usage** - Claude API has rate limits and costs
2. **Test with real users** - Get feedback early and often
3. **Track metrics consistently** - Use the dashboard to identify trends
4. **Iterate on prompts** - The AI prompt is key to output quality

## 🔒 Security & Privacy

- **API Keys**: Never commit `.env` files to Git
- **User Data**: Anonymous IDs only, no personal info collected
- **Metrics**: Stored locally in CSV files
- **Content**: Processed by Claude API (see [Anthropic's privacy policy](https://www.anthropic.com/privacy))

## 📈 Scaling Considerations

### Current Setup (Good for 0-1000 users/month)
- CSV-based metrics storage
- Single Streamlit instance
- Suitable for MVP/testing

### Future Improvements (1000+ users)
- Migrate to PostgreSQL or MongoDB for metrics
- Add user authentication
- Implement caching for common queries
- Use async API calls for better performance
- Add A/B testing capabilities

## 🤝 Contributing

Found a bug? Have an idea? Here's how to improve this project:

1. Test the feature locally
2. Update relevant files
3. Update this README if needed
4. Share your improvements!

## 📚 Resources

- [Streamlit Documentation](https://docs.streamlit.io)
- [Anthropic API Docs](https://docs.anthropic.com)
- [Claude Prompt Engineering Guide](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview)

## 💬 Support

### Common Questions

**Q: How much does this cost to run?**
A: Streamlit Cloud is free for public apps. Claude API costs ~$3 per 1M input tokens, $15 per 1M output tokens. Typical strategy costs $0.01-0.03.

**Q: Can I use this for commercial purposes?**
A: Yes! Just ensure you have appropriate API access and follow Anthropic's terms of service.

**Q: How do I export metrics data?**
A: Use the download button in the Metrics Dashboard, or directly access `metrics.csv`.

**Q: Can I customize the AI responses?**
A: Absolutely! Edit the prompt in `agent_logic.py` to change how Claude generates strategies.

## 🎉 Success Stories

Track your success with the metrics dashboard and see:
- How many strategies you're creating
- User satisfaction trends
- Engagement over time
- Retention improvements

---

**Built with ❤️ using Claude Sonnet 4 and Streamlit**

Ready to revolutionize content planning? Start generating strategies now! 🚀