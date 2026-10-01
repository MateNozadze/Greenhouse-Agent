import requests

def fetch_wikipedia_summary(disease_name: str) -> str:
    """Fetches a brief summary from Wikipedia for a given disease name."""
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{disease_name.replace(' ', '_')}"
    headers = {'User-Agent': 'GreenhouseMonitoringAgent/1.0'}
    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            return response.json().get("extract", "Wikipedia details not found.")
        return "No additional details found on Wikipedia."
    except Exception as e:
        return f"Error fetching Wikipedia data: {str(e)}"