from datasets import load_dataset
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import pickle
import numpy as np


def load_wikiart_dataset():
    dataset = load_dataset("huggan/wikiart", streaming=True, split="train")
    return dataset
