import requests
import os
import json
from dotenv import load_dotenv
from typing import Dict, Optional

class PostmanAPIDebug:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.getpostman.com"
        self.headers = {
            "X-Api-Key": self.api_key,
            "Content-Type": "application/json"
        }

    def debug_team_users(self) -> Optional[Dict]:
        """Get detailed team user information with debug output"""
        endpoint = f"{self.base_url}/users"
        
        print("\n=== Making API Request ===")
        print(f"Endpoint: {endpoint}")
        print(f"Headers: {json.dumps(self.headers, indent=2)}")
        
        try:
            print("\n=== Sending Request ===")
            response = requests.get(endpoint, headers=self.headers)
            
            print("\n=== Response Details ===")
            print(f"Status Code: {response.status_code}")
            print(f"Response Headers: {json.dumps(dict(response.headers), indent=2)}")
            
            try:
                response_json = response.json()
                print("\n=== Response JSON Structure ===")
                print(json.dumps(response_json, indent=2))
                
                if 'users' in response_json:
                    users = response_json['users']
                    print(f"\n=== Users Found: {len(users)} ===")
                    
                    for i, user in enumerate(users, 1):
                        print(f"\nUser {i}:")
                        print(json.dumps(user, indent=2))
                
                return response_json
                
            except json.JSONDecodeError as e:
                print("\n=== Raw Response Content ===")
                print(response.text)
                print(f"\nError decoding JSON: {str(e)}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"\nRequest Exception: {str(e)}")
            return None

def main():
    # Load environment variables
    load_dotenv()
    print("Environment variables loaded")
    
    # Get API key
    api_key = os.getenv('POSTMAN_API_KEY')
    if not api_key:
        api_key = input("Please enter your Postman API key: ")
    
    print(f"\nAPI Key (first/last 4): {api_key[:4]}...{api_key[-4:]}")
    
    # Initialize client and debug team users
    client = PostmanAPIDebug(api_key)
    client.debug_team_users()

if __name__ == "__main__":
    main()
