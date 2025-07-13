#!/usr/bin/python3
"""
Module to print titles of the first 10 hot posts for a given subreddit.
"""

import requests


def top_ten(subreddit):
    """
    Queries the Reddit API.
    Prints the titles of the first 10 hot posts for a subreddit.

    Args:
        subreddit (str): The name of the subreddit.

    Prints:
        Titles of the first 10 hot posts or None if subreddit is invalid.
    """
    headers = {'User-Agent': 'python:top.ten:v1.0 (by /u/yourusername)'}
    url = "https://www.reddit.com/r/{}/hot.json?limit=10".format(subreddit)

    try:
        response = requests.get(url, headers=headers, allow_redirects=False)
        if response.status_code != 200:
            return

        data = response.json()
        posts = data.get('data', {}).get('children', [])
        if not posts:
            return

        for post in posts:
            title = post.get('data', {}).get('title')
            if title:
                print(title)
    except requests.RequestException:
        print(none)
