import requests
import os
import time
from typing import Dict, List, Optional
from collections import defaultdict
from dotenv import load_dotenv

class PostmanAPI:
    def __init__(self, api_key: str):
        """
        Initialize the Postman API client
        """
        self.api_key = api_key
        self.base_url = "https://api.getpostman.com"
        self.headers = {
            "X-Api-Key": self.api_key,
            "Content-Type": "application/json"
        }
        self.delay = 1  # Default delay between requests in seconds
    
    def _make_request(self, endpoint: str, error_context: str = "") -> Optional[Dict]:
        """Make API request with rate limit handling"""
        while True:
            try:
                response = requests.get(endpoint, headers=self.headers)
                
                if response.status_code == 429:  # Rate limit exceeded
                    retry_after = int(response.headers.get('Retry-After', 60))
                    print(f"\nRate limit exceeded. Waiting {retry_after} seconds...")
                    time.sleep(retry_after)
                    continue
                
                if response.status_code != 200:
                    print(f"Error {error_context}: {response.status_code}")
                    print(f"Response: {response.text}")
                    return None
                
                time.sleep(self.delay)  # Add delay between successful requests
                return response.json()
                
            except requests.exceptions.RequestException as e:
                print(f"Error {error_context}: {str(e)}")
                return None
    
    def get_workspaces(self) -> Optional[List[Dict]]:
        """Get all workspaces the user has access to"""
        data = self._make_request(
            f"{self.base_url}/workspaces",
            "fetching workspaces"
        )
        return data.get('workspaces', []) if data else None

    def get_workspace_members(self, workspace_id: str, workspace_name: str) -> Optional[List[Dict]]:
        """Get members for a specific workspace"""
        data = self._make_request(
            f"{self.base_url}/workspaces/{workspace_id}",
            f"fetching members for workspace {workspace_name}"
        )
        
        if not data:
            return None
            
        workspace = data.get('workspace', {})
        members = workspace.get('members', [])
        
        # Add workspace name to each member record
        for member in members:
            member['workspace_name'] = workspace_name
            
        return members

def process_members(all_members: List[Dict]) -> Dict[str, Dict]:
    """
    Process members list to combine duplicates and track workspaces
    Returns dict with user ID as key and user details + workspace list as value
    """
    user_data = defaultdict(lambda: {
        'name': '',
        'email': '',
        'roles': set(),
        'workspaces': set()
    })
    
    for member in all_members:
        user = member.get('user', {})
        user_id = user.get('id')
        if not user_id:
            continue
            
        user_data[user_id]['name'] = user.get('name', 'N/A')
        user_data[user_id]['email'] = user.get('email', 'N/A')
        user_data[user_id]['roles'].add(member.get('role', 'N/A'))
        user_data[user_id]['workspaces'].add(member.get('workspace_name', 'N/A'))
    
    return user_data

def main():
    # Load environment variables
    load_dotenv()
    
    # Get API key
    api_key = os.getenv('POSTMAN_API_KEY')
    if not api_key:
        api_key = input("Please enter your Postman API key: ")
    
    print(f"Using API key: {api_key[:4]}...{api_key[-4:]}")
    
    # Initialize client
    client = PostmanAPI(api_key)
    
    # Get all workspaces
    print("\nFetching workspaces...")
    workspaces = client.get_workspaces()
    if not workspaces:
        print("Failed to fetch workspaces")
        return
    
    # Get members from each workspace
    print(f"\nFetching members from {len(workspaces)} workspaces (with rate limiting)...")
    all_members = []
    for i, workspace in enumerate(workspaces, 1):
        workspace_id = workspace.get('id')
        workspace_name = workspace.get('name', 'Unknown Workspace')
        print(f"Processing workspace {i}/{len(workspaces)}: {workspace_name}")
        
        members = client.get_workspace_members(workspace_id, workspace_name)
        if members:
            all_members.extend(members)
    
    if not all_members:
        print("No members found in any workspace")
        return
    
    # Process and combine member data
    user_data = process_members(all_members)
    
    # Display results
    print("\nUnique Members Across All Workspaces:")
    print("=====================================")
    for user_id, data in user_data.items():
        print(f"Name: {data['name']}")
        print(f"Email: {data['email']}")
        print(f"Roles: {', '.join(data['roles'])}")
        print("Workspaces:")
        for workspace in sorted(data['workspaces']):
            print(f"  - {workspace}")
        print("-------------------------------------")
    
    # Print summary
    print(f"\nSummary:")
    print(f"Total unique users: {len(user_data)}")
    print(f"Total workspaces: {len(workspaces)}")

if __name__ == "__main__":
    main()