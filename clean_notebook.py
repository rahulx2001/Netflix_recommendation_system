"""
Script to clean the Netflix notebook - remove emojis and make code look human-written
"""
import json
import re

notebook_path = '/Users/rahulkumarsinghj/Library/Containers/net.whatsapp.WhatsApp/Data/tmp/documents/B14FAEE7-F13E-45E4-92CD-4F8F0B0D71F2/Netflix_Clustering_Analysis.ipynb'

with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Emoji pattern to remove common emojis
emoji_pattern = re.compile("["
    u"\U0001F300-\U0001F9FF"  # symbols & pictographs
    u"\U00002702-\U000027B0"
    u"\U000024C2-\U0001F251"
    u"\U00002600-\U000026FF"  # misc symbols
    u"\U00002700-\U000027BF"  # dingbats
    u"\U0001F1E0-\U0001F1FF"  # flags
    u"\U00002500-\U00002BEF"  # various
    u"\U0001F900-\U0001F9FF"  # supplemental
    "]+", flags=re.UNICODE)

# Also remove printed emojis like ✅ ❌ 📊 etc
text_emojis = ['✅', '❌', '📊', '📋', '🔎', '🔢', '👀', '📂', '🔍', '🎯', '🎬', '⏱️', '🔄', '💾',
               '📈', '📉', '🔶', '🔷', '⚠️', '✨', '💡', '🚀', '📌', '🎉', '🧹', '🔧', '📝', 
               '🏷️', '📁', '🗂️', '📑', '📃', '🔔', '💬', '🔗', '📤', '📥', '🎞️', '📺', '🎬',
               '🗓️', '🗺️', '🌍', '🌎', '🌏', '⭐', '🍿', '🎭', '🎪', '🎨', '🎵', '🎶', '💯']

def clean_text(text):
    """Remove emojis and clean up text"""
    # Remove emoji patterns
    text = emoji_pattern.sub('', text)
    
    # Remove text emojis
    for emoji in text_emojis:
        text = text.replace(emoji, '')
    
    # Clean up extra spaces
    text = re.sub(r' +', ' ', text)
    text = text.strip()
    
    return text

count = 0
for i, cell in enumerate(nb['cells']):
    source = cell.get('source', [])
    if isinstance(source, list):
        new_source = []
        for line in source:
            cleaned = clean_text(line)
            new_source.append(cleaned)
        if source != new_source:
            cell['source'] = new_source
            count += 1
    elif isinstance(source, str):
        cleaned = clean_text(source)
        if source != cleaned:
            cell['source'] = cleaned
            count += 1
    
    # Also clean outputs
    outputs = cell.get('outputs', [])
    for output in outputs:
        if 'text' in output:
            if isinstance(output['text'], list):
                output['text'] = [clean_text(t) for t in output['text']]
            elif isinstance(output['text'], str):
                output['text'] = clean_text(output['text'])

# Save the cleaned notebook
with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=2)

print(f"Cleaned {count} cells")
print(f"Saved to: {notebook_path}")
