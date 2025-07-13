#!/usr/bin/python3
"""
Module to print titles of the first 10 hot posts for a given subreddit.
"""

import requests
from requests.auth import HTTPBasicAuth

CLIENT_ID = 'YOUR_CLIENT_ID'
CLIENT_SECRET = 'YOUR_CLIENT_SECRET'
REDDIT_USERNAME = 'YOUR_USERNAME'
REDDIT_PASSWORD = 'YOUR_PASSWORD'

def get_token():
    """
    Obtain OAuth2 access token from Reddit using script app and password grant.
    """
    auth = HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
    data = {
        'grant_type': 'password',
        'username': REDDIT_USERNAME,
        'password': REDDIT_PASSWORD
    }
    headers = {'User-Agent': 'ubuntu:alu-scripting:v1.0 (by /u/' + REDDIT_USERNAME + ')'}
    res = requests.post('https://www.reddit.com/api/v1/access_token',
                        auth=auth, data=data, headers=headers)
    if res.status_code != 200:
        return None
    return res.json().get('access_token')

def top_ten(subreddit):
    """
    Queries the Reddit API.
    Prints the titles of the first 10 hot posts for a subreddit.

    Args:
        subreddit (str): The name of the subreddit.

    Prints:
        Titles of the first 10 hot posts and 'OK' if subreddit is valid,
        or 'None' if subreddit is invalid.
    """
    headers = {'User-Agent': 'ubuntu:alu-scripting:v1.0 (by /u/yourusername)'}
    url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit=10"

    try:
        response = requests.get(url, headers=headers, allow_redirects=False)
        if response.status_code != 200:
            print("None")
            return

        data = response.json()
        posts = data.get('data', {}).get('children', [])
        if not posts:
            print("None")
            return

        for post in posts:
            title = post.get('data', {}).get('title')
            if title:
                print(title)
        print("OK")
    except requests.RequestException:
        print("None")


if __name__ == "__main__":
    # example
    import sys

    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <subreddit>")
        exit(1)

    top_ten(sys.argv[1])

