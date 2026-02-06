"""
econdata_gemini: An AI Agent using FRED and Google Gemini API 
================================================================================
The  workflow of this agent:
1. Understand the question (Think)
2. Fetch the relevant economic data (Act)
3. Analyze results (Observe)
4. Generate an answer (Respond)

Setup:
1. pip install google-genai fredapi python-dotenv colorama
2. Get API keys from:
   - FRED: https://fred.stlouisfed.org/docs/api/api_key.html
   - Google AI Studio: https://aistudio.google.com/app/apikey
3. .env file with API keys:
   FRED_API_KEY=[enter key]
   GOOGLE_API_KEY=[enter key]
"""

import os
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv
from fredapi import Fred
from google import genai
from google.genai import types
from colorama import init, Fore, Style

load_dotenv()
init()


# Define agent class
class FREDAgent:  
    
    def __init__(self): 
        self.fred = Fred(api_key=os.getenv('FRED_API_KEY'))
        self.client = genai.Client(api_key=os.getenv('GOOGLE_API_KEY'))
        # Gemini 2.5 Flash model (recommended for production)
        self.model = 'gemini-2.5-flash'
    



    # Plan what data to fetch from the FRED Database
    def think(self, question):  
        prompt = f"""What FRED series code would help answer the question below?
                Question: {question}

                Common FRED codes: UNRATE (unemployment), FPCPITOTLZGUSA (CPI inflation),
                GDP, DFF (fed funds rate)

                Return ONLY valid JSON in this exact format: {{"explanation": "why this helps", "series_code": "EXACT_FRED_CODE"}}"""
        
        print(f"\n{Fore.CYAN}=== THINK: LLM Call ==={Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Input:{Style.RESET_ALL}\n{prompt}")
        
        # Configure for JSON response using new SDK

        config = types.GenerateContentConfig(response_mime_type="application/json")
        
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=config
        )
        
        output = response.text
        print(f"\n{Fore.YELLOW}Output:{Style.RESET_ALL}\n{output}")
        
        plan = json.loads(output)
        return plan['series_code']
    


    # Fetch requested data from FRED
    def act(self, series_code):  
        print(f"\n{Fore.GREEN}=== ACT: FRED API Call ==={Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Fetching:{Style.RESET_ALL} {series_code}")
        
        # Get series metadata for units
        info = self.fred.get_series_info(series_code)
        units = info['units']
        
        # Get last 4 years of data
        end = datetime.now()
        start = end - timedelta(days=365*4)
        
        print(f"{Fore.YELLOW}Period:{Style.RESET_ALL} {start.date()} to {end.date()}")
        
        data = self.fred.get_series(series_code, start, end)
        print(f"{Fore.YELLOW}Result:{Style.RESET_ALL} {len(data)} data points")
        print(f"  Latest: {data.iloc[-1]:.2f} {units} ({data.index[-1].date()})")
        
        return data, units
    


    # Analyze fetched data
    def observe(self, data, units): 
        observations = {
            "current_value": float(data.iloc[-1]),
            "current_date": data.index[-1].strftime("%Y-%m-%d"),
            "units": units
        }
        
        print(f"\n{Fore.MAGENTA}=== OBSERVE: Data Analysis ==={Style.RESET_ALL}")
        print(json.dumps(observations, indent=2))
        
        return observations
    

    # Generate natural language response
    def respond(self, question, observations):  
        prompt = f"""Answer this question using the data:
Question: {question}
Data: {json.dumps(observations, indent=2)}

Provide a brief, clear answer citing specific numbers."""
        
        print(f"\n{Fore.CYAN}=== RESPOND: LLM Call ==={Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Input:{Style.RESET_ALL}\n{prompt}")
        
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt
        )
        
        output = response.text
        print(f"\n{Fore.YELLOW}Output:{Style.RESET_ALL}\n{output}")
        
        return output
    


    # Define orchestrator agent
    def answer(self, question): 
        # Think -> Act -> Observe -> Respond
        print(f"\n{Fore.BLUE}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.BLUE}Question: {question}{Style.RESET_ALL}")
        print(f"{Fore.BLUE}{'='*60}{Style.RESET_ALL}")
        
        try:
            series_code = self.think(question)  # Think: What data?
            data, units = self.act(series_code)  # Act: Fetch data
            observations = self.observe(data, units)  # Observe: Analyze data
            response = self.respond(question, observations)  # Respond: Generate an answer
            
            print(f"\n{Fore.GREEN}=== FINAL ANSWER ==={Style.RESET_ALL}")
            print(response)
            
            return response
            
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            print(f"\n{Fore.RED}{error_msg}{Style.RESET_ALL}")
            return error_msg



# Execute agent with interactive prompt
if __name__ == "__main__":  
    agent = FREDAgent()
    
    # Run with and examplele query
    # agent.answer("What is the US inflation rate?")
    # agent.answer("Hows the US house market right now")
    # agent.answer("Whats/Hows the **custom economic question**?")
    
    # Interactive mode
    print(f"\n{Fore.CYAN}Interactive mode{Style.RESET_ALL}")
    question = input(f"\n{Fore.YELLOW}Ask an economic question: {Style.RESET_ALL}")
    agent.answer(question)
