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
    # Clean up the count string
    clean_count = count.replace(" reviews", "").replace("reviews", "").replace(",", "").strip()
    if 'K' in clean_count:
        clean_count = float(clean_count.replace('K', '')) * 1000
        clean_count = int(clean_count)
    return clean_rating, clean_count
    
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
        print(f"\n{app['name']}")
        print("| App    | Ratings | Reviews |")
        print("| ------ | ------- | ------- |")
        
        google_rating, google_count = get_google_play_rating(app['google_play_id'])
        apple_rating, apple_count = get_apple_store_rating(app['apple_store_id'])
        
        print(f"| Google | {google_rating:<7} | {google_count:<7} |")
        print(f"| Apple  | {apple_rating:<7.2f} | {apple_count:<7} |")

if __name__ == "__main__":
    process_apps()

