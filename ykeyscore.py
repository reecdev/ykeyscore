import requests
import sys
import itertools
import threading
import time
import ollama
import re

loading = False

def scrub(text):
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    text = re.sub(r'!?\[.*?\]\(.*?\)', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def getPosts(username):
    posts = []
    url = f"https://arctic-shift.photon-reddit.com/api/posts/search?author={username}&limit=100"
    
    while url:
        response = requests.get(url).json()
        posts.extend([scrub(post.get("selftext")) for post in response.get("data", []) if post.get("selftext")])
        url = response.get("metadata", {}).get("next_url")
    
    return posts

def loader_ui(text):
    spinner = itertools.cycle(['/', '-', '\\', '|'])
    
    while loading == True:
        sys.stdout.write(f"\r{next(spinner)} {text}")
        sys.stdout.flush()
        time.sleep(0.1)
    
    print("")

def loader(text):
    time.sleep(0.1)
    global loading
    loading = True
    threading.Thread(target=loader_ui, args=(text,)).start()

print("=" * 52)
print("  YKEYSCORE beta - nothing is private~")
print("=" * 52)
print()
username = input("enter reddit username> ")
print()

loader(f"collecting {username}")

posts = getPosts(username)
loading = False

loader(f"reading {len(posts)} posts")

summary = ""

for i, post in enumerate(posts):
    loading = False
    loader(f"extracting information from post {i+1}")
    try:
        summary = re.search(r"<summary>(.*?)</summary>", ollama.chat(model="qwen3:1.7b", messages=[
            {"role": "user", "content": f"""Here is the new post:
```
{post}
```

Here is your current summary:
```
{summary}
```

You are a data analysis agent.
Your job is to analyze the text provided and your current summary and draw conclusions from what the user is likely into or what they do, information about them, exc.
You must update the summary provided with new information you learned from the new piece of information.
If nothing new is learned, simply DO NOT change the summary at all and output the old summary.
Format summaries as bullet points.

You must ALWAYS respond in this format:
<summary>
SUMMARY GOES HERE. IF NOTHING NEW IS LEARNED, PUT OLD SUMMARY HERE
</summary>
    """}
        ])["message"]["content"], re.DOTALL).group(1).strip()
    except:
        continue

loading = False

print()
print("=" * 53)
print("  YKEYSCORE beta - nothing is private~")
print("=" * 52)
print("Extracted information:")
print(summary)