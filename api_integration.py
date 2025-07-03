# api_integration.py - AI Integration for Insights
import requests
import json
import random
import os
from datetime import datetime
from typing import Dict, List, Optional, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class InsightsGenerator:
    """
    Generates AI-powered insights from airline market data.
    Supports OpenAI API integration with fallback to rule-based insights.
    """
    
    def __init__(self, openai_api_key: Optional[str] = None):
        """
        Initialize the InsightsGenerator.
        
        Args:
            openai_api_key: OpenAI API key for AI-powered insights
        """
        self.openai_api_key = openai_api_key or os.getenv('OPENAI_API_KEY')
        self.openai_base_url = "https://api.openai.com/v1/chat/completions"
        self.max_retries = 3
        self.timeout = 30
    
    def generate_insights(self, market_analysis: Dict[str, Any]) -> List[Dict[str, str]]:
        """
        Generate AI-powered insights from market data.
        
        Args:
            market_analysis: Dictionary containing market analysis data
            
        Returns:
            List of insight dictionaries with 'title' and 'content' keys
        """
        try:
            # Validate input data
            if not market_analysis or not isinstance(market_analysis, dict):
                logger.warning("Invalid market analysis data, using fallback insights")
                return self._generate_fallback_insights()
            
            # Try OpenAI API for real insights
            if self._is_openai_configured():
                ai_insights = self._generate_ai_insights(market_analysis)
                if ai_insights:
                    logger.info("Generated AI-powered insights successfully")
                    return ai_insights
            
            # Fallback to rule-based insights
            logger.info("Using rule-based insights generation")
            return self._generate_rule_based_insights(market_analysis)
                
        except Exception as e:
            logger.error(f"Insights generation error: {e}")
            return self._generate_fallback_insights()
    
    def _is_openai_configured(self) -> bool:
        """Check if OpenAI API is properly configured."""
        return (self.openai_api_key and 
                self.openai_api_key != "YOUR_OPENAI_API_KEY" and
                len(self.openai_api_key) > 20)
    
    def _generate_ai_insights(self, data: Dict[str, Any]) -> Optional[List[Dict[str, str]]]:
        """
        Generate insights using OpenAI API.
        
        Args:
            data: Market analysis data
            
        Returns:
            List of AI-generated insights or None if failed
        """
        try:
            headers = {
                'Authorization': f'Bearer {self.openai_api_key}',
                'Content-Type': 'application/json'
            }
            
            # Create comprehensive prompt
            prompt = self._create_analysis_prompt(data)
            
            payload = {
                'model': 'gpt-3.5-turbo',
                'messages': [
                    {
                        'role': 'system',
                        'content': 'You are an expert airline industry analyst. Provide clear, actionable insights based on market data.'
                    },
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ],
                'max_tokens': 800,
                'temperature': 0.7
            }
            
            # Make API request with retries
            for attempt in range(self.max_retries):
                try:
                    response = requests.post(
                        self.openai_base_url,
                        headers=headers,
                        json=payload,
                        timeout=self.timeout
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        insights_text = result['choices'][0]['message']['content']
                        return self._parse_ai_insights(insights_text)
                    elif response.status_code == 429:
                        logger.warning(f"Rate limit hit, attempt {attempt + 1}")
                        if attempt < self.max_retries - 1:
                            import time
                            time.sleep(2 ** attempt)  # Exponential backoff
                    else:
                        logger.error(f"OpenAI API error: {response.status_code}")
                        break
                        
                except requests.exceptions.RequestException as e:
                    logger.error(f"Request error attempt {attempt + 1}: {e}")
                    if attempt < self.max_retries - 1:
                        import time
                        time.sleep(2 ** attempt)
            
            return None
                
        except Exception as e:
            logger.error(f"AI insights error: {e}")
            return None
    
    def _create_analysis_prompt(self, data: Dict[str, Any]) -> str:
        """Create a comprehensive prompt for AI analysis."""
        stats = data.get('statistics', {})
        price_trends = data.get('price_trends', {})
        demand_patterns = data.get('demand_patterns', {})
        
        prompt = f"""
        Analyze this airline market data and provide exactly 4 key insights in the following format:

        **Insight Title 1**
        Detailed analysis content here...

        **Insight Title 2**
        Detailed analysis content here...

        **Insight Title 3**
        Detailed analysis content here...

        **Insight Title 4**
        Detailed analysis content here...

        Market Data:
        - Average Price: ${stats.get('avg_price', 'N/A')}
        - Price Change: {stats.get('price_change', 'N/A')}
        - Demand Score: {stats.get('demand_score', 'N/A')}%
        - Total Routes: {stats.get('total_routes', 'N/A')}
        
        Price Trends (recent weeks): {price_trends.get('prices', [])}
        Weekly Demand Pattern: {demand_patterns.get('bookings', [])}
        
        Focus on:
        1. Market trend analysis and implications
        2. Pricing strategy recommendations
        3. Demand pattern insights and opportunities
        4. Strategic business recommendations
        
        Provide actionable insights that airlines can use for decision-making.
        """
        
        return prompt
    
    def _parse_ai_insights(self, text: str) -> List[Dict[str, str]]:
        """
        Parse AI-generated insights into structured format.
        
        Args:
            text: Raw AI response text
            
        Returns:
            List of structured insights
        """
        insights = []
        lines = text.split('\n')
        
        current_insight = {'title': '', 'content': ''}
        
        for line in lines:
            line = line.strip()
            
            # Check for insight titles (marked with ** or numbered)
            if line.startswith('**') and line.endswith('**'):
                if current_insight['title']:
                    insights.append(current_insight)
                current_insight = {
                    'title': line.replace('**', '').strip(),
                    'content': ''
                }
            elif line and any(line.startswith(f'{i}.') for i in range(1, 10)):
                if current_insight['title']:
                    insights.append(current_insight)
                parts = line.split('.', 1)
                if len(parts) > 1:
                    current_insight = {
                        'title': parts[1].strip(),
                        'content': ''
                    }
            elif line and current_insight['title']:
                current_insight['content'] += line + ' '
        
        # Add the last insight
        if current_insight['title']:
            insights.append(current_insight)
        
        # Clean up content
        for insight in insights:
            insight['content'] = insight['content'].strip()
        
        return insights[:4]  # Return top 4 insights
    
    def _generate_rule_based_insights(self, data: Dict[str, Any]) -> List[Dict[str, str]]:
        """
        Generate insights using rule-based logic.
        
        Args:
            data: Market analysis data
            
        Returns:
            List of rule-based insights
        """
        insights = []
        stats = data.get('statistics', {})
        
        # Price trend insight
        avg_price = stats.get('avg_price', 400)
        price_change = stats.get('price_change', '+0%')
        
        if '+' in str(price_change):
            insights.append({
                'title': 'Price Trend Analysis',
                'content': f'Market prices have increased by {price_change}, indicating strong demand conditions. The current average price of ${avg_price} suggests premium market positioning opportunities. Airlines should consider dynamic pricing strategies to maximize revenue during peak demand periods.'
            })
        else:
            insights.append({
                'title': 'Price Trend Analysis',
                'content': f'Market prices have decreased by {price_change}, indicating potential oversupply or competitive pressure. The current average price of ${avg_price} suggests opportunities for market share growth through competitive pricing and value-added services.'
            })
        
        # Demand pattern insight
        demand_score = stats.get('demand_score', 50)
        
        if demand_score > 75:
            insights.append({
                'title': 'Demand Assessment',
                'content': f'Exceptional demand score of {demand_score}% indicates a seller\'s market with high passenger interest. This presents opportunities for capacity expansion, premium service offerings, and strategic route development. Consider increasing frequency on high-demand routes.'
            })
        elif demand_score > 50:
            insights.append({
                'title': 'Demand Assessment',
                'content': f'Moderate demand score of {demand_score}% suggests balanced market conditions. Focus on operational efficiency, service quality improvements, and competitive positioning. Monitor competitor activities and adjust strategies accordingly.'
            })
        else:
            insights.append({
                'title': 'Demand Assessment',
                'content': f'Lower demand score of {demand_score}% indicates market challenges requiring strategic intervention. Consider promotional campaigns, route optimization, partnership opportunities, or service differentiation to stimulate demand.'
            })
        
        # Route network analysis
        total_routes = stats.get('total_routes', 20)
        popular_routes = data.get('popular_routes', {})
        
        if popular_routes.get('bookings'):
            top_route_bookings = max(popular_routes['bookings']) if popular_routes['bookings'] else 0
            insights.append({
                'title': 'Route Network Optimization',
                'content': f'Network analysis of {total_routes} routes reveals concentrated demand patterns. Top routes generate {top_route_bookings} bookings, indicating hub-and-spoke opportunities. Consider capacity reallocation from underperforming routes to high-demand corridors for improved efficiency.'
            })
        else:
            insights.append({
                'title': 'Route Network Analysis',
                'content': f'Current network spans {total_routes} routes with varying performance levels. Route optimization opportunities exist through data-driven capacity allocation and strategic partnerships on secondary routes.'
            })
        
        # Seasonal and strategic opportunities
        seasonal_data = data.get('seasonal_trends', {})
        if seasonal_data.get('demand'):
            peak_demand = max(seasonal_data['demand']) if seasonal_data['demand'] else 0
            low_demand = min(seasonal_data['demand']) if seasonal_data['demand'] else 0
            seasonality = ((peak_demand - low_demand) / low_demand * 100) if low_demand > 0 else 0
            
            insights.append({
                'title': 'Seasonal Strategy & Growth',
                'content': f'Seasonal demand variation of {seasonality:.0f}% presents revenue management opportunities. Peak periods show {peak_demand} bookings vs {low_demand} in low season. Implement dynamic pricing, advance booking incentives, and targeted marketing campaigns to optimize year-round performance.'
            })
        else:
            insights.append({
                'title': 'Strategic Growth Opportunities',
                'content': 'Market analysis reveals opportunities in dynamic pricing implementation, capacity optimization, and strategic route development. Focus on data-driven decision making and customer experience enhancement to drive sustainable growth.'
            })
        
        return insights
    
    def _generate_fallback_insights(self) -> List[Dict[str, str]]:
        """
        Generate fallback insights when other methods fail.
        
        Returns:
            List of generic but relevant insights
        """
        current_month = datetime.now().month
        
        # Seasonal messaging
        if current_month in [12, 1, 2]:  # Winter
            seasonal_msg = "Winter travel patterns show increased demand for warm destinations and holiday travel."
        elif current_month in [6, 7, 8]:  # Summer
            seasonal_msg = "Summer peak season presents opportunities for leisure route optimization and capacity expansion."
        elif current_month in [3, 4, 5]:  # Spring
            seasonal_msg = "Spring travel uptick indicates recovery in business travel and leisure bookings."
        else:  # Fall
            seasonal_msg = "Fall shoulder season provides opportunities for competitive pricing and route testing."
        
        return [
            {
                'title': 'Market Dynamics Overview',
                'content': f'Current airline market shows typical seasonal patterns with evolving demand structures. {seasonal_msg} Airlines should focus on flexible capacity management and dynamic pricing strategies to optimize revenue across different market segments.'
            },
            {
                'title': 'Revenue Optimization Strategy',
                'content': 'Implement advanced revenue management systems with dynamic pricing capabilities. Focus on demand forecasting, competitor analysis, and customer segmentation to maximize yield. Consider ancillary revenue opportunities and premium service offerings to improve unit economics.'
            },
            {
                'title': 'Network Planning Insights',
                'content': 'Route performance analysis reveals opportunities for network optimization. High-traffic corridors between major cities show consistent demand, while secondary routes may benefit from strategic partnerships, frequency adjustments, or seasonal scheduling modifications.'
            },
            {
                'title': 'Digital Transformation Opportunities',
                'content': 'Modern travelers expect seamless digital experiences and personalized services. Invest in mobile-first booking platforms, AI-powered customer service, and data analytics capabilities to enhance customer satisfaction and operational efficiency while reducing distribution costs.'
            }
        ]
    
    def get_market_sentiment(self, data: Dict[str, Any]) -> str:
        """
        Analyze overall market sentiment based on data.
        
        Args:
            data: Market analysis data
            
        Returns:
            Market sentiment string
        """
        try:
            stats = data.get('statistics', {})
            demand_score = stats.get('demand_score', 50)
            price_change = stats.get('price_change', '+0%')
            
            # Extract numeric value from price change
            if '+' in str(price_change):
                price_trend = 'positive'
            elif '-' in str(price_change):
                price_trend = 'negative'
            else:
                price_trend = 'stable'
            
            # Determine sentiment
            if demand_score > 70 and price_trend == 'positive':
                return 'Bullish - Strong demand with rising prices'
            elif demand_score > 60 and price_trend == 'stable':
                return 'Optimistic - Stable demand with controlled pricing'
            elif demand_score < 40 and price_trend == 'negative':
                return 'Bearish - Weak demand with falling prices'
            elif demand_score < 50:
                return 'Cautious - Below-average demand conditions'
            else:
                return 'Neutral - Balanced market conditions'
                
        except Exception as e:
            logger.error(f"Sentiment analysis error: {e}")
            return 'Neutral - Market analysis in progress'
    
    def generate_recommendations(self, insights: List[Dict[str, str]]) -> List[str]:
        """
        Generate actionable recommendations based on insights.
        
        Args:
            insights: List of generated insights
            
        Returns:
            List of actionable recommendations
        """
        recommendations = []
        
        # Extract key themes from insights
        themes = []
        for insight in insights:
            content = insight.get('content', '').lower()
            if 'price' in content or 'pricing' in content:
                themes.append('pricing')
            if 'demand' in content:
                themes.append('demand')
            if 'route' in content or 'network' in content:
                themes.append('network')
            if 'seasonal' in content:
                themes.append('seasonal')
        
        # Generate recommendations based on themes
        if 'pricing' in themes:
            recommendations.append('Implement dynamic pricing algorithms to optimize revenue based on demand patterns')
        
        if 'demand' in themes:
            recommendations.append('Develop targeted marketing campaigns for underperforming routes and time periods')
        
        if 'network' in themes:
            recommendations.append('Conduct comprehensive route profitability analysis and consider network optimization')
        
        if 'seasonal' in themes:
            recommendations.append('Create seasonal capacity plans and advance booking incentive programs')
        
        # Add general recommendations
        recommendations.extend([
            'Monitor competitor pricing and adjust strategies accordingly',
            'Invest in customer experience improvements to drive loyalty and premium pricing',
            'Leverage data analytics for better demand forecasting and inventory management'
        ])
        
        return recommendations[:5]  # Return top 5 recommendations


# Additional utility functions for API integration
class APIHealthChecker:
    """Monitor API health and performance."""
    
    def __init__(self):
        self.api_status = {}
    
    def check_openai_status(self, api_key: str) -> Dict[str, Any]:
        """Check OpenAI API status and limits."""
        try:
            headers = {'Authorization': f'Bearer {api_key}'}
            response = requests.get(
                'https://api.openai.com/v1/models',
                headers=headers,
                timeout=10
            )
            
            return {
                'status': 'healthy' if response.status_code == 200 else 'error',
                'status_code': response.status_code,
                'response_time': response.elapsed.total_seconds()
            }
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'response_time': None
            }


# Configuration and constants
DEFAULT_CONFIG = {
    'max_insights': 4,
    'max_recommendations': 5,
    'api_timeout': 30,
    'max_retries': 3,
    'fallback_enabled': True
}

# Export main classes
__all__ = ['InsightsGenerator', 'APIHealthChecker', 'DEFAULT_CONFIG']