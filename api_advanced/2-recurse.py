#!/usr/bin/python3
"""
Recursively queries the Reddit API for all hot article titles of a subreddit.
"""
import requests


def recurse(subreddit, hot_list=[], after=None):
    """Returns a list of titles of all hot articles for a given subreddit"""
    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {"User-Agent": "python:recurse.hot:v1.0 (by /u/yourusername)"}
    params = {"after": after, "limit": 100}

    try:
        response = requests.get(
            url, headers=headers, params=params, allow_redirects=False
        )
        if response.status_code != 200:
            return None

        data = response.json().get("data", {})
        posts = data.get("children", [])
        for post in posts:
            hot_list.append(post.get("data", {}).get("title"))

        after = data.get("after")
        if after is not None:
            return recurse(subreddit, hot_list, after)
        return hot_list
    except Exception:
        return None
