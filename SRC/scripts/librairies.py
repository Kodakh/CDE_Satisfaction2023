# Ce fichier .py regroupe l'ensemble des bibliothèques dont nous aurons besoin pour le bon fonctionnement des scripts et fonctions

import csv
import pandas as pd 
from bs4 import BeautifulSoup as bs
import requests 
import time
import os
import re
import ast
import csv
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from textblob import TextBlob
import spacy
from spacy.training import Example
from spacy.util import minibatch
import random