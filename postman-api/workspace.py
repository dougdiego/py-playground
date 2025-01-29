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

    def debug_workspace(self, workspace_id: str) -> Optional[Dict]:
        """Get detailed workspace information with debug output"""
        endpoint = f"{self.base_url}/workspaces/{workspace_id}"
        
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
                
                if 'workspace' in response_json:
                    workspace = response_json['workspace']
                    print("\n=== Workspace Details ===")
                    print(f"Name: {workspace.get('name', 'N/A')}")
                    print(f"ID: {workspace.get('id', 'N/A')}")
                    print(f"Type: {workspace.get('type', 'N/A')}")
                    
                    members = workspace.get('members', [])
                    print(f"\n=== Members Found: {len(members)} ===")
                    
                    for i, member in enumerate(members, 1):
                        print(f"\nMember {i}:")
                        print(json.dumps(member, indent=2))
                
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
    
    # Get workspace ID
    workspace_id = os.getenv('POSTMAN_WORKSPACE_ID')
    if not workspace_id:
        workspace_id = input("Please enter the workspace ID to debug: ")
    
    print(f"Workspace ID: {workspace_id}")
    
    # Initialize client and debug workspace
    client = PostmanAPIDebug(api_key)
    client.debug_workspace(workspace_id)

if __name__ == "__main__":
    main()