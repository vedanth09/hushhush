import requests
import time
import re
import csv

# Function to fetch user data from the Stack Exchange API
def fetch_stack_overflow_data(page):
    base_url = f'https://api.stackexchange.com/2.3/users'
    params = {
        'page': page,
        'pagesize': 100,
        'order': 'desc',
        'sort': 'modified',
        'site': 'stackoverflow',
        'filter': '!56ApJn82ELRG*IWQxo6.gXu9qS90qXxNmY8e9b'
    }
    response = requests.get(base_url, params=params)
    return response.json()

# Initialize a list to save user records
user_records = []
print("fetching data")

# Fetch data until page 15
for page_number in range(1, 15):
    # Print status
    print(f"Requesting page {page_number}/15")

    # Get Data
    response_data = fetch_stack_overflow_data(page_number)

    # Save the users
    for user in response_data['items']:  # Indentation fixed here
        # Extract user_id and replace it with _id for compatibility
        user['_id'] = user.pop('user_id')
        
        # Clean display name and create email
        email_name = re.sub(r'[^a-zA-Z0-9 \n\.]', '', user['display_name'])
        user['email'] = 'perfectpatterns+' + email_name.replace(' ', '') + '@gmail.com'

        # Extract additional fields
        user['badge_counts'] = user.get('badge_counts', {'gold': 0, 'silver': 0, 'bronze': 0})
        user['view_count'] = user.get('view_count', 0)
        user['answer_count'] = user.get('answer_count', 0)
        user['question_count'] = user.get('question_count', 0)
        user['reputation_change_quarter'] = user.get('reputation_change_quarter', 0)
        user['reputation'] = user.get('reputation', 0)
        user['link'] = user.get('link', '')
        
        # Append to records
        user_records.append(user)

    # If the result is not in cache, sleep to avoid throttling
    if response_data.get('has_more', False):
        time.sleep(11)
    else:
        break

# Save user records to a CSV file
csv_filename = '/Users/vedanth/Desktop/HushHush/stackoverflow_users.csv'
with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = user_records[0].keys()
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    for user in user_records:
        writer.writerow(user)

print(f"Data saved to {csv_filename}")
