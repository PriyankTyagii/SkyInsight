
# ✈️ SkyInsight : Airline Booking Market Demand Web App

## 🚀 Overview
The **Airline Booking Market Demand Web App** is a Python-based interactive dashboard that gathers, analyzes, and visualizes market trends in the airline booking industry.  
It helps hostel groups and travel businesses monitor **real-time demand, price trends, and popular routes** to make informed decisions.

This project integrates **live data sources, APIs, web scraping, AI-powered insights, and interactive visualizations** to deliver a seamless and actionable user experience.

---

## 🎯 Key Features
- ✅ Real-time airline booking market data via APIs and web scraping
- ✅ Price trends, peak travel periods, and demand forecasts
- ✅ AI-powered market insights using OpenAI GPT
- ✅ Interactive dashboards with Plotly & Chart.js
- ✅ Responsive UI/UX for desktop and mobile
- ✅ API caching to reduce rate limits and ensure fast loading
- ✅ Clean, modular, and scalable Python backend

---

## 🏗️ Project Structure
```text
airline_demand_app/
├── app.py                 # Main Flask application
├── data_scraper.py        # Web scraping functions
├── data_processor.py      # Data processing and analysis
├── api_integration.py     # API integration for external sources
├── templates/             # HTML templates
│   ├── index.html
├── data/
│   └── cached_data.json   # Cached API and scraped data
├── .env.example           # Environment variable template
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation
```

---

## ⚙️ Tech Stack
- **Backend:** Python, Flask  
- **Frontend:** HTML, CSS, JavaScript (Plotly, Chart.js)  
- **Data Sources:** Amadeus API, Skyscanner API, Web Scraping  
- **AI Integration:** OpenAI GPT API  
- **Deployment:** Local / Heroku / Railway / Render  

---

## 📦 Setup Instructions

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/PriyankTyagii/SkyInsight.git
cd SkyInsight
```

### 2️⃣ Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate    # For Linux/Mac
venv\Scripts\activate       # For Windows
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Configure Environment Variables
Create a `.env` file based on the provided `.env.example`:
```dotenv
AMADEUS_API_KEY=your_amadeus_api_key
AMADEUS_API_SECRET=your_amadeus_api_secret
SKYSCANNER_API_KEY=your_skyscanner_api_key
OPENAI_API_KEY=your_openai_api_key
```

### 5️⃣ Run the Application
```bash
python app.py
```
Visit `http://127.0.0.1:5000` in your browser to explore the dashboard.

---

## 🌐 API and Data Sources
- **Amadeus for Developers API**: Flight offers, destination insights  
- **Skyscanner Rapid API**: Flight search, market insights  
- **Web Scraping**: Google Flights, Kayak (terms permitting)

---

## 💡 AI-Powered Insights
Leverages the **OpenAI GPT API** to:
- Analyze demand trends
- Forecast market shifts
- Provide actionable travel insights

---

## 📊 Visualizations
- Route popularity charts
- Price trend graphs
- Demand heatmaps
- Real-time filtering

---

## 🔐 Best Practices
- API keys secured with environment variables
- Caching to handle rate limits
- Ethical web scraping with rate limiting and robots.txt compliance
- Modular code structure for easy maintenance and scalability

---

## 🛠️ Development Timeline
| Phase | Duration |
|-------|----------|
| Setup & Configuration | 2 Hours |
| API & Web Scraper Development | 2 Hours |
| Data Processing Engine | 2 Hours |
| Web Interface & Dashboard | 2 Hours |
| AI Integration | 2 Hours |
| Testing & Deployment | 2 Hours |

---

## 🚀 Deployment Options
- ✅ Local server via Flask
- ✅ Heroku (Free tier)
- ✅ Railway / Render / PythonAnywhere

---

## 🔍 Future Enhancements
- Real-time flight data streaming
- Machine learning-based price prediction
- Multi-city demand comparison
- PDF/Excel report exports
- User authentication for personalized dashboards

---

## 🤝 Contribution Guidelines
We welcome contributions! Please:
- Fork the repository
- Create a new branch
- Submit a pull request with detailed changes


## 📞 Contact
**Priyank Tyagi**  
📧 Email: priyanktyagi404.com  
💼 LinkedIn: [Your LinkedIn](https://www.linkedin.com/in/priyank-tyagi-3a3a10259/)
