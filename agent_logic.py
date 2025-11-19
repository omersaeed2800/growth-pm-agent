import os
import json
from anthropic import Anthropic

class ContentStrategyAgent:
    """
    AI Agent that generates comprehensive content strategies using Claude API.
    
    This agent performs 5 key tasks:
    1. Analyzes target audience
    2. Researches trending topics
    3. Suggests blog topics
    4. Generates content outlines
    5. Provides SEO recommendations
    """
    
    def __init__(self):
        """Initialize the Claude API client."""
        # Get API key from environment variable
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            raise ValueError(
                "ANTHROPIC_API_KEY not found in environment variables. "
                "Please create a .env file with your API key."
            )
        
        self.client = Anthropic(api_key=api_key)
        self.model = "claude-sonnet-4-20250514"  # Latest Claude Sonnet model
    
    def generate_strategy(
        self,
        business_type: str,
        target_audience: str,
        industry: str,
        content_goals: str,
        keywords: str = None,
        content_type: str = "Mixed",
        num_topics: int = 5
    ) -> dict:
        """
        Generate a comprehensive content strategy.
        
        Args:
            business_type: Type of business (e.g., "SaaS startup")
            target_audience: Description of target audience
            industry: Industry or niche
            content_goals: What they want to achieve
            keywords: Optional target keywords
            content_type: Preferred content type
            num_topics: Number of topic suggestions
        
        Returns:
            Dictionary containing strategy components
        """
        
        # Build the prompt for Claude
        prompt = self._build_prompt(
            business_type=business_type,
            target_audience=target_audience,
            industry=industry,
            content_goals=content_goals,
            keywords=keywords,
            content_type=content_type,
            num_topics=num_topics
        )
        
        # Call Claude API
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4000,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            # Extract the response text
            response_text = response.content[0].text
            
            # Parse the structured response
            strategy = self._parse_response(response_text)
            
            return strategy
            
        except Exception as e:
            raise Exception(f"Error calling Claude API: {str(e)}")
    
    def _build_prompt(
        self,
        business_type: str,
        target_audience: str,
        industry: str,
        content_goals: str,
        keywords: str,
        content_type: str,
        num_topics: int
    ) -> str:
        """Build the detailed prompt for Claude."""
        
        prompt = f"""You are an expert content strategist and SEO specialist. I need you to create a comprehensive content strategy based on the following information:

**Business Information:**
- Business Type: {business_type}
- Industry/Niche: {industry}
- Target Audience: {target_audience}
- Content Goals: {content_goals}
"""
        
        if keywords:
            prompt += f"- Target Keywords: {keywords}\n"
        
        prompt += f"- Preferred Content Type: {content_type}\n"
        
        prompt += f"""
Please provide a detailed content strategy that includes:

1. **AUDIENCE ANALYSIS** (2-3 paragraphs)
   - Deep dive into the target audience's demographics, psychographics, pain points, and needs
   - What keeps them up at night?
   - What solutions are they searching for?
   - What content formats do they prefer?

2. **TRENDING TOPICS** (2-3 paragraphs)
   - Current trending topics in the {industry} industry
   - Emerging trends and conversations
   - Seasonal opportunities
   - Content gaps in the market

3. **BLOG TOPIC SUGGESTIONS** ({num_topics} topics)
   For each topic, provide:
   - A compelling, SEO-friendly title
   - Rationale: Why this topic is valuable (2-3 sentences)
   - Target keyword phrase
   - Estimated search volume category (High/Medium/Low)
   - Detailed outline with 5-7 section headings
   - 3-5 specific SEO recommendations for that post

4. **GENERAL SEO STRATEGY** (5-7 recommendations)
   - Overall SEO tactics for the content strategy
   - Link building opportunities
   - Content distribution strategies
   - Technical SEO considerations

Format your response EXACTLY as follows (this is critical for parsing):

AUDIENCE_ANALYSIS:
[Your analysis here]

TRENDING_TOPICS:
[Your trending topics analysis here]

BLOG_TOPICS:
---TOPIC_START---
TITLE: [Title here]
RATIONALE: [Rationale here]
KEYWORD: [Primary keyword]
SEARCH_VOLUME: [High/Medium/Low]
OUTLINE:
- [Section 1]
- [Section 2]
- [Section 3]
- [Section 4]
- [Section 5]
SEO_RECOMMENDATIONS:
- [Recommendation 1]
- [Recommendation 2]
- [Recommendation 3]
---TOPIC_END---

[Repeat for all {num_topics} topics]

GENERAL_SEO:
- [Recommendation 1]
- [Recommendation 2]
- [Recommendation 3]
- [Recommendation 4]
- [Recommendation 5]

Be specific, actionable, and data-driven. Focus on topics that will drive traffic and conversions."""

        return prompt
    
    def _parse_response(self, response_text: str) -> dict:
        """
        Parse Claude's structured response into a dictionary.
        
        Args:
            response_text: Raw text response from Claude
        
        Returns:
            Structured dictionary with all strategy components
        """
        
        strategy = {
            'audience_analysis': '',
            'trending_topics': '',
            'blog_topics': [],
            'general_seo': []
        }
        
        try:
            # Extract audience analysis
            if 'AUDIENCE_ANALYSIS:' in response_text:
                start = response_text.index('AUDIENCE_ANALYSIS:') + len('AUDIENCE_ANALYSIS:')
                end = response_text.index('TRENDING_TOPICS:')
                strategy['audience_analysis'] = response_text[start:end].strip()
            
            # Extract trending topics
            if 'TRENDING_TOPICS:' in response_text:
                start = response_text.index('TRENDING_TOPICS:') + len('TRENDING_TOPICS:')
                end = response_text.index('BLOG_TOPICS:')
                strategy['trending_topics'] = response_text[start:end].strip()
            
            # Extract blog topics
            topic_sections = response_text.split('---TOPIC_START---')[1:]
            
            for section in topic_sections:
                if '---TOPIC_END---' not in section:
                    continue
                
                section = section.split('---TOPIC_END---')[0]
                
                topic = {
                    'title': '',
                    'rationale': '',
                    'keyword': '',
                    'search_volume': '',
                    'outline': [],
                    'seo_recommendations': []
                }
                
                # Parse title
                if 'TITLE:' in section:
                    title_start = section.index('TITLE:') + len('TITLE:')
                    title_end = section.index('RATIONALE:')
                    topic['title'] = section[title_start:title_end].strip()
                
                # Parse rationale
                if 'RATIONALE:' in section:
                    rat_start = section.index('RATIONALE:') + len('RATIONALE:')
                    rat_end = section.index('KEYWORD:')
                    topic['rationale'] = section[rat_start:rat_end].strip()
                
                # Parse keyword
                if 'KEYWORD:' in section:
                    key_start = section.index('KEYWORD:') + len('KEYWORD:')
                    key_end = section.index('SEARCH_VOLUME:')
                    topic['keyword'] = section[key_start:key_end].strip()
                
                # Parse search volume
                if 'SEARCH_VOLUME:' in section:
                    vol_start = section.index('SEARCH_VOLUME:') + len('SEARCH_VOLUME:')
                    vol_end = section.index('OUTLINE:')
                    topic['search_volume'] = section[vol_start:vol_end].strip()
                
                # Parse outline
                if 'OUTLINE:' in section:
                    out_start = section.index('OUTLINE:') + len('OUTLINE:')
                    out_end = section.index('SEO_RECOMMENDATIONS:')
                    outline_text = section[out_start:out_end].strip()
                    
                    # Split by lines and filter bullet points
                    for line in outline_text.split('\n'):
                        line = line.strip()
                        if line.startswith('-'):
                            topic['outline'].append(line[1:].strip())
                
                # Parse SEO recommendations
                if 'SEO_RECOMMENDATIONS:' in section:
                    seo_start = section.index('SEO_RECOMMENDATIONS:') + len('SEO_RECOMMENDATIONS:')
                    seo_text = section[seo_start:].strip()
                    
                    for line in seo_text.split('\n'):
                        line = line.strip()
                        if line.startswith('-'):
                            topic['seo_recommendations'].append(line[1:].strip())
                
                strategy['blog_topics'].append(topic)
            
            # Extract general SEO recommendations
            if 'GENERAL_SEO:' in response_text:
                seo_start = response_text.index('GENERAL_SEO:') + len('GENERAL_SEO:')
                seo_text = response_text[seo_start:].strip()
                
                for line in seo_text.split('\n'):
                    line = line.strip()
                    if line.startswith('-'):
                        strategy['general_seo'].append(line[1:].strip())
        
        except Exception as e:
            # If parsing fails, return raw response in a readable format
            print(f"Warning: Error parsing response: {str(e)}")
            strategy['audience_analysis'] = response_text[:500] + "..."
            strategy['trending_topics'] = "See full response above"
        
        return strategy
