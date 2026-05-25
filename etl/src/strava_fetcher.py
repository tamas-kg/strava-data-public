import requests
import time, json
from src.logger import setup_logger

logger = setup_logger("StravaFetcher")

class StravaFetcher:
    def __init__(self, client_id:str, client_secret:str):
        self.base_url = "https://www.strava.com/api/v3"
        self.client_id = client_id
        self.client_secret = client_secret
        self.headers = self.refresh_api_token()

    def refresh_api_token(self) -> dict[str, str]:
        """Refresh token"""
        with open("tokens.json") as f:
            tokens = json.load(f)

        if time.time() > tokens["expires_at"]:
            logger.info("Access token expired, refreshing...")

            response = requests.post("https://www.strava.com/oauth/token", data={
                'client_id':self.client_id,
                'client_secret':self.client_secret,
                'grant_type':'refresh_token',
                'refresh_token':tokens["refresh_token"]
            })

            new_tokens = response.json()

            with open("tokens.json", "w") as f:
                json.dump(new_tokens, f)

            access_token = new_tokens["access_token"]

        else:
            access_token = tokens["access_token"]

        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        return headers
    
    def get_activities(self, headers:dict[str, str], historical_load:bool=False) -> list[dict]:

        url = f"{self.base_url}/activities/"

        if historical_load:
            # Set pagination parameters
            per_page = 200  # You can fetch up to 200 activities per page
            page = 1        # Start from the first page

            activities = []

            while True:
                params = {
                    'per_page': per_page,
                    'page': page
                }
                response = requests.get(url, headers=headers, params=params)

                if response.status_code == 200:
                    activities = activities + response.json()

                    if not response.json():  # If no activities are returned, stop pagination
                        logger.info("No more activities found")
                        break
                    
                    # Move to the next page
                    page += 1

                else:
                    logger.exception(f"Error: Failed to fetch data from Strava API. Status code {response.status_code}")
                    break
        else:
            response = requests.get(url, headers=headers)
            activities = response.json()

        return activities
    
    def get_activity(self, id:int) -> list[dict]:

        url = f"{self.base_url}/activities/{id}"

        response = requests.get(url, headers=self.headers)
        activity = response.json()

        return activity

    
    def get_starred_segments(self, headers:str, historical_load:bool=False) -> list[dict]:
        """Fetch starred segments from Strava."""

        url = f"{self.base_url}/segments/starred"

        params = {
                    'per_page': 200,
                    'page': 1
                }
        
        response = requests.get(url, headers=headers, params=params)

        starred_segments = response.json()

        logger.info("Fetched starred segments", extra={"count": len(starred_segments)})

        return starred_segments
