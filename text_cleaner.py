from html.parser import HTMLParser
import html
import re


class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.fed = []

    def handle_date(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def clean_text(text):
    text = html.unescape(text)  # Unescape string
    text = strip_tags(text)  # Remove HTML
    text = re.sub('(ht|f)tp[s]?://\S+', '', text)  # Remove links
    text = re.sub('\S*@\S*\s?', '', text)  # Remove e-mail addresses
    text = text.replace("'", '').replace('’', '').replace('‘', '')  # Preserve contractions
    text = re.sub('([^\s\w]|_)+', ' ', text)  # Remove remaining punctuation
    text = text.strip().lower()  # Strip all leading and trailing whitespace and make all lowercase
    text = text.replace('œ', ' ')  # This character exists between two words with no space so replacing with space instead of removing completely
    text = ' '.join([re.sub(r'[^a-zA-Z0-9]', '', w) for w in text.split(' ')])  # Remove special characters
    text = text.replace('\r\n', '')  # This is present only in the abuse queue posts
    text = re.sub('\s{2,}', ' ', text)  # Repalce multiple spaces with one space
    text = text.strip()  # Strip all leading and trailing whitespace that might have been added
    return text
