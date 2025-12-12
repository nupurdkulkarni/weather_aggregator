from browser_use import Agent, Browser, ChatBrowserUse
import asyncio
from typing import List, Dict, Optional, Tuple
import ast 
import json
import re 

llm = ChatBrowserUse()
json_format = {"city": "Pune", "temperature": 22, "weather_summary": "it is sunny"}


def extract_clean_json_from_result(raw_result: str) -> Optional[Dict]:
    """
    Uses regex and literal evaluation to extract the final clean dictionary
    from the raw AgentHistoryList string.
    """
    dict_pattern = re.compile(r"\{\'city\':.*?\}")
    
    try:
      
        all_dicts = dict_pattern.findall(raw_result)
        
        if not all_dicts:
            return None
            

        final_dict_str = all_dicts[-1]
        weather_data = ast.literal_eval(final_dict_str)
        return weather_data
        
    except (ValueError, SyntaxError) as e:
        print(f"Extraction Error: Could not parse dictionary literal (Error: {e}) from string.")
        return None
    except Exception as e:
        print(f"Extraction Error: An unexpected error occurred: {e}")
        return None



async def get_city_weather(city: str) -> str:
    """
    Sets up an agent to fetch weather data for a city and returns the
    string representation of the AgentHistoryList result.
    """
    browser = Browser()
    weather_checker_agent = Agent(
        task=(f"Get the weather information for the '{city}' and return ONLY in this JSON format {json_format}."),
        llm=llm,
        browser=browser,
    )
    weather_history = await weather_checker_agent.run()
    weather_info = str(weather_history) 
    await browser.stop()
    return weather_info


def filter_warm_cities(json_data: List[Dict], min_temp: float = 10.0) -> List[Dict]:
    """
    Filters a list of clean dictionary objects based on temperature > min_temp.
    """
    warm_cities = []
    
    for weather_data in json_data:
        temperature = weather_data.get("temperature")
        
        if isinstance(temperature, (int, float)) and temperature > min_temp:
            warm_cities.append(weather_data)
            
    return warm_cities



async def get_weather_info() -> Tuple[List[str], List[Dict], List[Dict]]:
    cities = ["Berlin, Germany", "Amsterdam, Netherlands", "Pune, India"]

    tasks = [get_city_weather(city) for city in cities]
    
    raw_results = await asyncio.gather(*tasks)
    
    all_clean_data = [
        data 
        for raw_result in raw_results
        if (data := extract_clean_json_from_result(raw_result)) is not None
    ]
    
    warm_cities = filter_warm_cities(all_clean_data, min_temp=10.0)
    
    return raw_results, all_clean_data, warm_cities


if __name__ == "__main__":
    raw_results, all_clean_data, warm_cities_results = asyncio.run(get_weather_info())
    

    print("## Weather Info for all cities (Extracted) ##")
    for data in all_clean_data:
        print(json.dumps(data, indent=4))
    

    print("## Filtered Cities (Temp > 10°C) ##")
    print(warm_cities_results)


    warm_city_names = [city.get('city') for city in warm_cities_results if city.get('city')]
    print(f"\nCities with temp above 10°C: {warm_city_names}")
    
