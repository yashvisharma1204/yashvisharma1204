import re
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import subprocess

# Get commit messages
log = subprocess.run(
    ["git", "log", "--pretty=format:%s"],
    stdout=subprocess.PIPE,
    text=True
).stdout

# Clean and split
words = re.findall(r'\b\w+\b', log.lower())
common_words = [w for w in words if w not in {'the', 'and', 'for', 'this', 'that', 'with', 'fix'}]

# Count
counts = Counter(common_words)
most_common = dict(counts.most_common(50))

# Generate word cloud
wc = WordCloud(width=800, height=400, background_color="white").generate_from_frequencies(most_common)
wc.to_file("wordcloud.png")
