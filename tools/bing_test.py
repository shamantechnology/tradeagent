import requests
from dotenv import load_dotenv
import os

if __name__ == "__main__":
    load_dotenv()
    headers = {"Ocp-Apim-Subscription-Key": os.getenv("BING_SUBSCRIPTION_KEY")}
    params = {"q": "test", "textDecorations": True, "textFormat": "HTML"}
    response = requests.get(
        os.getenv("BING_SEARCH_URL"), 
        headers=headers, 
        params=params
    )
    response.raise_for_status()
    search_results = response.json()
    print(search_results)