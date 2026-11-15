import csv
import sys
import os

def load_raw_data(filename):
    """
    Loads the CSV file into a list of dictionaries exactly as it is (messy).
    """
    if not os.path.exists(filename):
        print(f"Error: The file '{filename}' was not found.")
        sys.exit(1)
        
    raw_tweets = []
    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            raw_tweets.append(row)
            
    return raw_tweets


def is_blank(value):
    """Helper: True if a field is missing (None) or only spaces."""
    return value is None or str(value).strip() == ""


def to_number(value):
    """
    Helper: convert a field to an int.
    Returns (number, was_fixed). Blank or non-numeric values become 0.
    """
    if is_blank(value):
        return 0, True
    try:
        return int(float(str(value).strip())), False
    except ValueError:
        return 0, True


def clean_data(tweets):
    """
    QUEST 1: Handle missing fields.
    Check for missing text, and replace empty likes/retweets with 0.
    Return a clean list of tweets.
    """
    clean_tweets = []
    removed = 0
    fixed = 0

    for tweet in tweets:
        # Missing Text -> remove the tweet
        if is_blank(tweet.get("Text")):
            removed += 1
            continue

        # Missing Likes / Retweets -> replace with 0 (and convert to int)
        likes, likes_fixed = to_number(tweet.get("Likes"))
        retweets, retweets_fixed = to_number(tweet.get("Retweets"))
        tweet["Likes"] = likes
        tweet["Retweets"] = retweets

        if likes_fixed or retweets_fixed:
            fixed += 1

        clean_tweets.append(tweet)

    print("--- Quest 1: Data Auditor ---")
    print(f"Rows removed (missing Text): {removed}")
    print(f"Rows fixed (missing Likes/Retweets set to 0): {fixed}")
    print(f"Total bad rows handled: {removed + fixed}")
    print(f"Clean tweets remaining: {len(clean_tweets)}\n")
    return clean_tweets


def find_viral_tweet(tweets):
    """
    QUEST 2: Loop through the list to find the tweet with the highest 'Likes'.
    Do not use the max() function.
    """
    print("--- Quest 2: The Viral Post ---")
    if len(tweets) == 0:
        print("No tweets available.\n")
        return None

    viral = tweets[0]
    for tweet in tweets:
        if tweet["Likes"] > viral["Likes"]:
            viral = tweet

    print(f"Username: {viral['Username']}")
    print(f"Likes   : {viral['Likes']}")
    print(f"Text    : {viral['Text']}\n")
    return viral


def custom_sort_by_likes(tweets):
    """
    QUEST 3: Implement Bubble Sort or Selection Sort to sort the list 
    by 'Likes' in descending order. NO .sort() allowed!
    """
    # Build a copy with append() so the original list keeps its order
    sorted_tweets = []
    for tweet in tweets:
        sorted_tweets.append(tweet)

    n = len(sorted_tweets)
    # Selection Sort: on each pass, find the tweet with the most Likes
    # in the unsorted part and swap it into position i.
    for i in range(n):
        max_index = i
        for j in range(i + 1, n):
            if sorted_tweets[j]["Likes"] > sorted_tweets[max_index]["Likes"]:
                max_index = j
        sorted_tweets[i], sorted_tweets[max_index] = sorted_tweets[max_index], sorted_tweets[i]

    return sorted_tweets


def search_tweets(tweets, keyword):
    """
    QUEST 4: Search for a keyword and extract matching tweets into a new list.
    """
    matches = []
    for tweet in tweets:
        if keyword.lower() in tweet["Text"].lower():
            matches.append(tweet)
    return matches


if __name__ == "__main__":
    # Load the messy data
    dataset = load_raw_data("twitter_dataset.csv")
    print(f"Loaded {len(dataset)} raw tweets.\n")
    
    # Quest 1: clean the data
    clean_dataset = clean_data(dataset)

    # Quest 2: viral tweet
    find_viral_tweet(clean_dataset)

    # Quest 3: top 10 most liked tweets
    print("--- Quest 3: Top 10 Most Liked Tweets ---")
    sorted_dataset = custom_sort_by_likes(clean_dataset)
    top_10 = sorted_dataset[:10]
    rank = 1
    for tweet in top_10:
        print(f"{rank}. @{tweet['Username']} - {tweet['Likes']} likes")
        print(f"   {tweet['Text']}")
        rank += 1
    print()

    # Quest 4: search
    print("--- Quest 4: The Content Filter ---")
    keyword = input("Enter a search word (e.g. tax, hard, development): ").strip()
    if keyword == "":
        print("Error: you didn't type anything. Please enter a word such as 'tax'.")
    else:
        results = search_tweets(clean_dataset, keyword)
        print(f"\n{len(results)} tweet(s) matched '{keyword}'.")
        for tweet in results:
            print(f"- @{tweet['Username']} ({tweet['Likes']} likes): {tweet['Text']}")
