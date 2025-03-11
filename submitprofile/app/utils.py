import re

def clean_text(text):
    #print("******** Start of clean text ********")
    # Remove HTML tags
    text = re.sub(r'<[^>]*?>','',text)
    # Remove URLs
    text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+','',text)
    # Remove special charecters
    text = re.sub(r'[^a-zA-Z0-9 ]','',text)
    # Remove multiple spaces
    text = re.sub(r'\s{2,}',' ',text)
    # Remove leading and trailing spaces
    text = text.strip()
    # Remove extra whitespaces
    text = ' '.join(text.split())
    #print("******** End of clean text ********")
    return text

