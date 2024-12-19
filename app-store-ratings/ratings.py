import requests
from bs4 import BeautifulSoup
import json

# https://apps.apple.com/us/app/prosper-invest/id1294834607
# https://play.google.com/store/apps/details?id=com.prosper.android.investorapp&hl=en_US&gl=US&pli=1

# Function to get Google Play Store app rating
def get_google_play_rating(app_id):
    url = f"https://play.google.com/store/apps/details?id={app_id}&hl=en"
    response = requests.get(url)
    #print(f"response: {response.text}")
    soup = BeautifulSoup(response.text, 'html.parser')
    rating = soup.find('div', class_='TT9eCd').text
    clean_rating = rating.replace("star", "")
    count = soup.find('div', class_='g1rdde').text
    return clean_rating, count
    
def get_apple_store_rating(bundle_id):
	# http://itunes.apple.com/lookup?bundleId=com.yelp.yelpiphone
    url = f"https://itunes.apple.com/lookup?bundleId={bundle_id}"
    response = requests.get(url).json()
    #print(f"response: {response}")
    rating = response['results'][0]['averageUserRating']
    count = response['results'][0]['userRatingCount'] 
    #rating = 1
    return (rating, count)

def process_apps():
    with open('apps.json', 'r') as file:
        data = json.load(file)
        
    for app in data['apps']:
        print(f"\nProcessing ratings for {app['name']}:")
        
        google_rating, google_count = get_google_play_rating(app['google_play_id'])
        apple_rating, apple_count = get_apple_store_rating(app['apple_store_id'])
        
        print(f"Google Play Rating: {google_rating} Count: {google_count}")
        print(f"Apple App Store Rating: {apple_rating} Count: {apple_count}")

if __name__ == "__main__":
    process_apps()

