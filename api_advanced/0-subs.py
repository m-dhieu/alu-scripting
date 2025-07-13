#!/usr/bin/python3
"""
Module to get the number of subscribers of a given subreddit using Reddit API.
"""

import requests


def number_of_subscribers(subreddit):
    """
    Queries the Reddit API.
    Returns the number of subscribers for a given subreddit.

    Args:
        subreddit (str): The name of the subreddit.

    Returns:
        int: Number of subscribers if subreddit is valid, else 0.
    """
    headers = {'User-Agent': 'ubuntu:alu-scripting:v1.0 (by /u/yourusername)'}
    url = "https://www.reddit.com/r/{}/about.json".format(subreddit)

    try:
        response = requests.get(url, headers=headers, allow_redirects=False)
        if response.status_code == 200:
            data = response.json()
            return data.get('data', {}).get('subscribers', 0)
        else:
            # invalid subreddit or redirect detected
            return 0
    except requests.RequestException:
        return 0


if __name__ == "__main__":
    # example:
    import sys

    if len(sys.argv) != 2:
        print("Usage: {} <subreddit>".format(sys.argv[0]))
        sys.exit(1)

    subreddit = sys.argv[1]
    count = number_of_subscribers(subreddit)
    print(count)
