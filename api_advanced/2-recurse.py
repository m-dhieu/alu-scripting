#!/usr/bin/python3
"""
Module to recursively query Reddit API,
and return a list of all hot article titles for a given subreddit.
"""

import requests


def recurse(subreddit, hot_list=None, after=None):
    """
    Recursively queries the Reddit API.

    Returns a list of titles of all hot articles for a given subreddit.

    Args:
        subreddit (str): Name of the subreddit to query.
        hot_list (list): List accumulating titles during recursion.
        after (str): Pagination token for Reddit API.

    Returns:
        list or None: List of titles of all hot articles, or None if subreddit
        is invalid.
    """
    if hot_list is None:
        hot_list = []

    headers = {
        'User-Agent': 'python:recurse:v1.0 (by /u/yourusername)'
    }
    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    params = {'limit': 100}
    if after:
        params['after'] = after

    try:
        response = requests.get(
            url,
            headers=headers,
            params=params,
            allow_redirects=False
        )
        if response.status_code != 200:
            return None

        data = response.json().get('data', {})
        children = data.get('children', [])
        if not children:
            return hot_list if hot_list else None

        for post in children:
            title = post.get('data', {}).get('title')
            if title:
                hot_list.append(title)

        after = data.get('after')
        if after is None:
            return hot_list

        return recurse(subreddit, hot_list, after)

    except requests.RequestException:
        return None


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Please pass an argument for the subreddit to search.")
        sys.exit(1)

    titles = recurse(sys.argv[1])
    if titles is None:
        print("None")
    else:
        print(len(titles))
