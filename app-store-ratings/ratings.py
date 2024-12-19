import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

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

def generate_html(apps_data):
    css = '''
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            max-width: 800px;
            margin: 40px auto;
            padding: 0 20px;
            background: #f5f5f7;
        }
        h1 {
            color: #1d1d1f;
            text-align: center;
            margin-bottom: 40px;
        }
        .app-container {
            background: white;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 30px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .app-name {
            color: #1d1d1f;
            margin-bottom: 20px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 10px;
        }
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #e6e6e6;
        }
        th {
            background-color: #f8f8f8;
            color: #666;
            font-weight: 500;
        }
        .timestamp {
            text-align: center;
            color: #666;
            font-size: 0.9em;
            margin-top: 40px;
        }
    '''
    
    content = []
    for app in apps_data:
        app_html = f'''
        <div class="app-container">
            <h2 class="app-name">{app['name']}</h2>
            <table>
                <thead>
                    <tr>
                        <th>App</th>
                        <th>Ratings</th>
                        <th>Reviews</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>Google</td>
                        <td>{app['google_rating']} ⭐</td>
                        <td>{app['google_count']} 💬</td>
                    </tr>
                    <tr>
                        <td>Apple</td>
                        <td>{app['apple_rating']:.2f} ⭐</td>
                        <td>{app['apple_count']} 💬</td>
                    </tr>
                </tbody>
            </table>
        </div>
        '''
        content.append(app_html)
    
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    html = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>App Store Ratings</title>
        <style>
        {css}
        </style>
    </head>
    <body>
        <h1>App Store Ratings</h1>
        {''.join(content)}
        <div class="timestamp">Last updated: {timestamp}</div>
    </body>
    </html>
    '''
    
    return html

def process_apps():
    with open('apps.json', 'r') as file:
        data = json.load(file)
    
    apps_data = []
    for app in data['apps']:
        print(f"\n{app['name']}")
        print("|        | Ratings | Reviews |")
        print("| ------ | ------- | ------- |")
        
        google_rating, google_count = get_google_play_rating(app['google_play_id'])
        apple_rating, apple_count = get_apple_store_rating(app['apple_store_id'])
        
        print(f"| Google | {google_rating:<7} | {google_count:<7} |")
        print(f"| Apple  | {apple_rating:<7.2f} | {apple_count:<7} |")
        
        apps_data.append({
            'name': app['name'],
            'google_rating': google_rating,
            'google_count': google_count,
            'apple_rating': apple_rating,
            'apple_count': apple_count
        })
    
    # Generate and save HTML
    html_content = generate_html(apps_data)
    with open('index.html', 'w') as f:
        f.write(html_content)

if __name__ == "__main__":
    process_apps()

