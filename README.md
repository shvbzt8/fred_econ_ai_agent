# FRED Economic Data AI Agent 

An AI agent using **Google's GenAI SDK (2025)** to answer economic questions by fetching and analyzing data from FRED.

## Setup Instructions

### 1. Install Dependencies
```bash
pip install google-genai fredapi python-dotenv colorama pandas
```

### 2. Get API Keys

**FRED API Key**
- Go to https://fred.stlouisfed.org/docs/api/api_key.html
- Create a free account and request an API key.

**Google Gemini API Key**
- Go to https://aistudio.google.com/app/apikey
- Sign in with your Google account
- Click "Create API Key" (free tier available)

### 3. Configure Environment Variables

Create a `.env` file:
```bash
FRED_API_KEY = your_actual_fred_api_key
GOOGLE_API_KEY = your_actual_google_api_key
```

### 4. Run the Agent

```bash
python main.py
```

## Features

The agent follows a four-step process:

1. **THINK**: Gemini determines which FRED series code to fetch
2. **ACT**: Retrieves the data from FRED
3. **OBSERVE**: Processes and structures the data
4. **RESPOND**: Gemini generates a natural language answer

## Example Questions that you can ask in the terminal:

- "What is the current unemployment rate?"
- "What is the federal funds rate?"
- "How has GDP changed recently?"
- "What's the latest CPI data?"

## Common FRED Series Codes

- `UNRATE` - Unemployment Rate
- `FPCPITOTLZGUSA` - CPI Inflation
- `GDP` - Gross Domestic Product
- `DFF` - Federal Funds Rate
- `CPIAUCSL` - Consumer Price Index
.....and many more find at https://fred.stlouisfed.org/


## Additional Resources

- [Google GenAI SDK Documentation](https://ai.google.dev/gemini-api/docs)
- [Migration Guide](https://github.com/googleapis/python-genai)
- [Gemini Models Documentation](https://ai.google.dev/gemini-api/docs/models/gemini)
- [FRED API Documentation](https://fred.stlouisfed.org/docs/api/)
