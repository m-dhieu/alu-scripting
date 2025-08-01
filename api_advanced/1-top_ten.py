#!/usr/bin/python3
"""
1-top_ten.py
Module with function to print the titles of the first 10 hot posts of a subreddit.
"""

import requests


def top_ten(subreddit):
    """Print the titles of the first 10 hot posts for a given subreddit.
    If subreddit is invalid, print None.
    """
    headers = {'User-Agent': 'ubuntu:api_advanced:v1.0 (by /u/yourusername)'}
    url = f'https://www.reddit.com/r/{subreddit}/hot.json?limit=10'

    try:
        response = requests.get(url, headers=headers, allow_redirects=False)
        if response.status_code != 200:
            print(None)
            return

        data = response.json()
        posts = data.get('data', {}).get('children', [])
        if not posts:
            print(None)
            return

        for post in posts:
            print(post['data']['title'])

    except Exception:
        print(None)
