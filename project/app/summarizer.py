"""Summarizer App that uses nlp + webscraping to summarize and app"""

import nltk
from newspaper import Article


def generate_summary(url: str) -> str:
    article = Article(url)
    article.download()
    article.parse()
    try:
        nltk.data.find("tokenizers/punkt")
    except LookupError:
        nltk.download("punkt")
    finally:
        article.nlp()

    return article.summary
