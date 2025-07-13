#!/usr/bin/python3
"""
Module to recursively query the Reddit API and return a list of all hot article titles
for a given subreddit. If no results are found or the subreddit is invalid, returns None.

Usage:
    python3 2-recurse.py <subreddit>

Arguments:
    subreddit (str): The name of the subreddit to query.

Returns:
    list: A list of titles of all hot articles, or None if subreddit is invalid.
"""

import os
import requests
from requests.auth import HTTPBasicAuth

CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')
USERNAME = os.getenv('REDDIT_USERNAME')
PASSWORD = os.getenv('REDDIT_PASSWORD')
USER_AGENT = f"ubuntu:alu-scripting:v1.0 (by /u/{USERNAME})"


def get_token():
    """Get OAuth2 token using Reddit script app password grant."""
    auth = HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
    data = {
        'grant_type': 'password',
        'username': USERNAME,
        'password': PASSWORD
    }
    headers = {'User-Agent': USER_AGENT}
    res = requests.post(
        'https://www.reddit.com/api/v1/access_token',
        auth=auth, data=data, headers=headers
    )
    if res.status_code != 200:
        return None
    return res.json().get('access_token')


def recurse(subreddit, hot_list=None, after=None):
    """
    Recursively queries the Reddit API to gather all hot post titles.

    Args:
        subreddit (str): The name of the subreddit to query.
        hot_list (list): Accumulator for titles during recursion.
        after (str): Pagination token for Reddit API.

    Returns:
        list: A list of titles of all hot articles, or None if subreddit is invalid.
    """
    if hot_list is None:
        hot_list = []

    token = get_token()
    if not token:
        return None

    headers = {'Authorization': f"bearer {token}", 'User-Agent': USER_AGENT}
    params = {'limit': 100, 'after': after} if after else {'limit': 100}
    url = f'https://oauth.reddit.com/r/{subreddit}/hot'

    try:
        res = requests.get(url, headers=headers, params=params, allow_redirects=False)
        if res.status_code != 200:
            return None

        data = res.json().get('data', {})
        children = data.get('children', [])
        if not children:
            return hot_list if hot_list else None

        for post in children:
            title = post.get('data', {}).get('title')
            if title:
                hot_list.append(title)

        next_after = data.get('after')
        if next_after:
            return recurse(subreddit, hot_list, next_after)
        return hot_list

    except requests.RequestException:
        return None


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <subreddit>")
        sys.exit(1)

    titles = recurse(sys.argv[1])
    print(len(titles)) if titles is not None else print("None")
