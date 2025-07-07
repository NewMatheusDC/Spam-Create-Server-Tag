import requests
import time
import random
import string

# Configuration
DISCORD_TOKEN = "YOUR_TOKEN_HERE"  # Replace with your Discord user token
DESIRED_TAG = "1234"  # Change to the vanity tag you want
DELAY_BETWEEN_ATTEMPTS = 5  # Seconds between attempts to avoid rate limits
MAX_ATTEMPTS = 1000  # Safety limit to prevent infinite loops

def generate_random_name():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))

def create_guild(guild_name):
    headers = {
        "Authorization": DISCORD_TOKEN,
        "Content-Type": "application/json"
    }
    
    payload = {
        "name": guild_name,
        "region": "brazil"  # Optional: set your preferred region
    }
    
    try:
        response = requests.post("https://discord.com/api/v9/guilds", headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error creating guild: {e}")
        return None

def delete_guild(guild_id):
    headers = {
        "Authorization": DISCORD_TOKEN
    }
    
    try:
        response = requests.delete(f"https://discord.com/api/v9/guilds/{guild_id}", headers=headers)
        if response.status_code == 204:
            return True
        else:
            print(f"Failed to delete guild: {response.status_code} - {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Error deleting guild: {e}")
        return False

def check_vanity_tag(guild_id):
    headers = {
        "Authorization": DISCORD_TOKEN
    }
    
    try:
        response = requests.get(f"https://discord.com/api/v9/guilds/{guild_id}", headers=headers)
        if response.status_code == 200:
            data = response.json()
            return data.get('vanity_url_code')
    except requests.exceptions.RequestException as e:
        print(f"Error checking vanity tag: {e}")
    
    return None

def main():
    attempts = 0
    
    print(f"Starting search for guild with vanity tag: {DESIRED_TAG}")
    print(f"Maximum attempts set to: {MAX_ATTEMPTS}")
    
    while attempts < MAX_ATTEMPTS:
        attempts += 1
        guild_name = generate_random_name()
        
        print(f"\nAttempt #{attempts}")
        print(f"Creating guild: {guild_name}")
        
        guild_data = create_guild(guild_name)
        
        if guild_data:
            guild_id = guild_data['id']
            print(f"Guild created with ID: {guild_id}")
            
            current_tag = check_vanity_tag(guild_id)
            
            if current_tag:
                print(f"Current vanity tag: {current_tag}")
                
                if current_tag == DESIRED_TAG:
                    print(f"\n🎉 DESIRED TAG ACQUIRED! 🎉")
                    print(f"Guild ID: {guild_id}")
                    print(f"Vanity URL: discord.gg/{current_tag}")
                    print("KEEPING THIS GUILD!")
                    return
                
            print("Deleting guild...")
            if delete_guild(guild_id):
                print("Guild deleted successfully.")
            else:
                print("Failed to delete guild. Continuing...")
        else:
            print("Failed to create guild. Trying again...")
        
        print(f"Waiting {DELAY_BETWEEN_ATTEMPTS} seconds...")
        time.sleep(DELAY_BETWEEN_ATTEMPTS)
    
    print(f"\nReached maximum attempts ({MAX_ATTEMPTS}) without finding the desired tag.")

if __name__ == "__main__":
    main()
