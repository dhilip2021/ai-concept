from django.shortcuts import render
import pywhatkit
import datetime
import wikipedia
import pyjokes
import keyboard
import requests
import json
import webbrowser
import os
import sqlite3
from pywikihow import RandomHowTo, search_wikihow
from googlesearch import search
from .models import Flash_news
from django.utils import timezone
from googlesearch import search
import requests
import json
from transformers import pipeline
from newsapi import NewsApiClient
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="xformers")
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification



#------------------------------------------------------------------------------------------------



# listener = sr.Recognizer()
# engine = pyttsx3.init('sapi5')
# voices = engine.getProperty('voices')
# tamil_voice_index = None
# for index, voice in enumerate(voices):
#     if 'Tamil' in voice.name:
#         tamil_voice_index = index
#         break
# if tamil_voice_index is not None:
#     engine.setProperty('voice', voices[tamil_voice_index].id)
#     print("Tamil voice set successfully.")
# else:
#     engine.setProperty('voice', voices[1].id)
#     print("English voice set successfully.")
# #--------------------------------------------------------------------
# # talk function
# def talk(text):
#     if not engine.isBusy():
#         engine.say(text)
#         engine.runAndWait()
#----------------------------------------------------------------------

#Voice Listening function
def jarvas_view(request):
    if request.method == 'POST':
        text_comment = request.POST.get('text_comment')
        voice_comment = request.FILES.get('voice_comment')
        # if voice_comment:
        #     voice_text = transcribe_voice_comment(voice_comment)
        #     # Process the voice_text further as needed
        #     print("Transcribed Voice Comment:", voice_text)

    else:
        text_comment = None
        voice_comment = None
    #----------------------------------------------------------------------------------
    flash_news = None
    weather_report = None
    location = None
    current_time = None
    wikipedia_result = None
    youtube_results = None
    song_played = None
    google_search_results=None
    tamil_news_results=None
    result=None
    #----------------------------------------------------------------------------------
    if text_comment:
        # play song
        if 'play' in text_comment:# play song 
            song = text_comment.replace('play', '')
            song_played = song
            #talk('playing ' + song)
            pywhatkit.playonyt(song)
        #-----------------------------------------------
        #Flash news
        if 'flash news' in text_comment:
            flash_news = get_flash_news()
            #talk(flash_news)
        #----------------------------------------------
        #News
        if 'news' in text_comment:
            field = extract_news_field(text_comment)
            if field:
                results = latestnews(field)
                if results:
                    return render(request, 'jarvas.html', {'results': results})
        #-----------------------------------------------------------------------
        #weather
        elif 'weather' in text_comment:
            weather_report = get_weather_report(text_comment)
            #talk(weather_report)
        #-----------------------------------------------------------------------
        #Location
        elif 'location' in text_comment:
            location = My_Location()
            print(location)
            #talk(location)
        #-----------------------------------------------------------------------
        #Time
        elif 'time' in text_comment:# time
            current_time = datetime.datetime.now().strftime('%I:%M %p')
            #talk('Current time is ' + current_time)
            print(current_time)
            #talk(current_time)
        #----------------------------------------------------------------------
        #Wikipedia Search
        elif 'wikipedia' in text_comment:
            text_comment =text_comment.replace("wikipedia", "")
            try:
                result = wikipedia.summary(text_comment, sentences=5)
                print("According to Wikipedia:")
                print(result)
                #talk("According to Wikipedia")
                #talk(result)
                wikipedia_result = result
            except wikipedia.exceptions.DisambiguationError as e:
                print("There are multiple options. Please specify your search term.")
                #talk("There are multiple options. Please specify your search term.")
            except wikipedia.exceptions.PageError as e:
                print("The requested page does not exist.")
                #talk("The requested page does not exist.")
        #-------------------------------------------------------------------------------
        #youtube search
        elif 'youtube ' in text_comment:
            search_query = text_comment.replace("jarvis", "").replace("youtube search", "")
            youtube_results = YouTubeSearch(search_query)
        #----------------------------------------------------------------------------------
        # Google search
        elif 'google' in text_comment or 'search' in text_comment:
            search_query = text_comment.replace('Google', '').replace('search', '')
            num_results = 5
            google_search_results = google_search(search_query,num_results = 5)
            #talk("According to Wikipedia")
            #talk(google_search_results)
        #----------------------------------------------------------------------------------
        # Tamil News                                                                                                      
        if 'tamil news' in text_comment:
            tamil_news_results = latest_tamil_news(num_articles=5)
            if tamil_news_results:
                for result in tamil_news_results:
                 print(result['title'], result['url'])
                 

 #---------------------------------------------------------------------------------------------------       
    if voice_comment:
        voice_text = transcribe_voice_comment(voice_comment)
        print("Transcribed Voice Comment:", voice_text)
        #------------------------------------------------------
        if 'play' in voice_text:
            song = voice_text.replace('play', '')
            song_played = song
            pywhatkit.playonyt(song)
        #--------------------------------------------------------
        elif 'flash news' in voice_text:
            flash_news = get_flash_news()
            #talk(flash_news)
            print(flash_news)
        #---------------------------------------------------------
        elif 'weather' in voice_text:
            weather_report = get_weather_report(voice_text)
            #talk(weather_report)
        #---------------------------------------------------------
        elif 'location' in voice_text:
            location = My_Location()
            #talk(location)
            print(location)
        #--------------------------------------------------------
        elif 'time' in voice_text:
            current_time = datetime.datetime.now().strftime('%I:%M %p')
            #talk(current_time)
            print(current_time)
        #----------------------------------------------------------------
        elif 'wikipedia' in voice_text:
            commend = voice_text.replace("wikipedia", "")
            try:
                result = wikipedia.summary(commend, sentences=10)
                print("According to Wikipedia:")
                print(result)
                #talk("According to Wikipedia:")
                #talk(result)
                wikipedia_result = result
            except wikipedia.exceptions.DisambiguationError as e:
                print("There are multiple options. Please specify your search term.")
            except wikipedia.exceptions.PageError as e:
                print("The requested page does not exist.")
        #--------------------------------------------------------------------------------
        elif 'youtube' in voice_text:
            search_query = voice_text.replace("jarvis", "").replace("youtube search", "")
            youtube_results = YouTubeSearch(search_query)
        #--------------------------------------------------------------------------------        
        if 'google' in voice_text or 'search' in voice_text:
            search_query = voice_text.replace('Google', '').replace('search', '')
            num_results = 5
            google_search_results = google_search(search_query,num_results = 5)
            #talk(google_search_results)
            print(google_search_results)
        
    #-----------------------------------------------------------------------------------------------------------
    
    context = {
        'flash_news': flash_news,
        'weather_report': weather_report,
        'location':location,
        'current_time': current_time,
        'wikipedia_result': wikipedia_result,
        'youtube_results': youtube_results,
        'song_played': song_played,
        'google_search_results': google_search_results,
        'tamil_news_results':tamil_news_results,
        'result':result,
        
    }
    
    return render(request, 'jarvas.html', context)

#--------------------------------------------------------------------------------------------------------------------
# Extract News Field
def extract_news_field(text_comment):
    field_keywords = {
        'business': ['business'],
        'entertainment': ['entertainment', 'movies', 'music'],
        'health': ['health', 'wellness'],
        'science': ['science', 'technology'],
        'sports': ['sports', 'games'],
        'education': ['education', 'learning', 'school', 'college', 'university'],
    }

    for field, keywords in field_keywords.items():
        if any(keyword in text_comment.lower() for keyword in keywords):
            return field

    return None
#-----------------------------------------------------------------------------------------------------------------------
#Latest News catagery 
def latestnews(field, num_articles=10):
    api_dict = {
        "business": "https://newsapi.org/v2/top-headlines?country=in&category=business&apiKey=3eadf74d5da9499d88532c77b5520641",
        "entertainment": "https://newsapi.org/v2/top-headlines?country=in&category=entertainment&apiKey=3eadf74d5da9499d88532c77b5520641",
        "health": "https://newsapi.org/v2/top-headlines?country=in&category=health&apiKey=3eadf74d5da9499d88532c77b5520641",
        "science": "https://newsapi.org/v2/top-headlines?country=in&category=science&apiKey=3eadf74d5da9499d88532c77b5520641",
        "sports": "https://newsapi.org/v2/top-headlines?country=in&category=sports&apiKey=3eadf74d5da9499d88532c77b5520641",
        "technology": "https://newsapi.org/v2/top-headlines?country=in&category=technology&apiKey=3eadf74d5da9499d88532c77b5520641",
        "education": "https://newsapi.org/v2/top-headlines?country=in&category=education&apiKey=3eadf74d5da9499d88532c77b5520641",
    }

    url = api_dict.get(field.lower())
    if url:
        print("URL found:", url)
        news = requests.get(url).json()
        if news['status'] == 'ok' and news['totalResults'] > 0:
            articles = news['articles'][:num_articles]
            results = []
            for article in articles:
                article_title = article['title']
                article_url = article['url']
                results.append({'title': article_title, 'url': article_url})
            return results
        else:
            print("No news articles found.")
            return None
    else:
        print("Invalid field of news.")
        return None
#------------------------------------------------------------------------------------------------------------------------------------
#Latest tamil News
import requests
def latest_tamil_news(num_articles=10):
    api_key = '3eadf74d5da9499d88532c77b5520641'
    url = f'https://newsapi.org/v2/top-headlines?country=in&language=ta&apiKey={api_key}'

    news = requests.get(url).json()
    if news['status'] == 'ok' and news['totalResults'] > 0:
        articles = news['articles'][:num_articles]
        results = []
        for article in articles:
            article_title = article['title']
            article_url = article['url']
            results.append({'title': article_title, 'url': article_url})
        return results
    else:
        print("No Tamil news articles found.")
        return None
#---------------------------------------------------------------------------------------------------------------------------------------
# Google Search
def google_search(query,num_results):
    api_key ="AIzaSyAN8vaS6wzJ77TRuEns8ehyIs-J8DRYUtU"
    
    search_url = f"https://www.google.com/search?q={query}"
    response = requests.get(search_url)
    search_results = response.text
    return search_results
#---------------------------------------------------------------------------------------------------------------------------------------
# Youtube Search
def YouTubeSearch(term):
    result = "https://www.youtube.com/results?search_query=" + term
    webbrowser.open(result)
    #talk("This Is What I Found For Your Search .")
    pywhatkit.playonyt(term)
    #talk("This May Also Help You Sir .")
#--------------------------------------------------------------------------------------------------------------------------------------
#To find location
def My_Location(city=None):
    if city is not None:
        url = f'https://geocode.xyz/{city}?json=1'
        geo_q = requests.get(url)
        geo_d = geo_q.json()
        
        if 'error' in geo_d:
            print(f"Failed to retrieve location information for {city}.")
            return None
        
        latitude = geo_d.get('latt', '')
        longitude = geo_d.get('longt', '')
        location = f"You are currently in {city}."
        map_url = f"https://www.google.com/maps/search/?api=1&query={latitude},{longitude}"
        print("Opening Google Maps...")
        webbrowser.open(map_url)
        return location
    else:
        try:
            response = requests.get('https://ipinfo.io/json')
            data = response.json()
            city = data.get('city', '')
            region = data.get('region', '')
            country = data.get('country', '')
            location = f"You are currently in {city}, {region}, {country}."
            map_url = f"https://www.google.com/maps/search/?api=1&query={city}+{region}+{country}"
            print("Opening Google Maps...")
            webbrowser.open(map_url)
            return location
        except requests.exceptions.RequestException as e:
            print(f"Failed to retrieve location information. Error: {str(e)}")
            return None
#------------------------------------------------------------------------------------------------------------------------------------------
# to get weather report
def get_weather_report(text_comment):
    city = text_comment.replace('weather', '').strip()
    return fetch_weather_report(city)

def fetch_weather_report(city):
    api_key = '10631a030ff7ea30360a0eb6fb4d6b31'
    #url = f'https://api.weatherapi.com/v1/current.json?key={api_key}&q={city}'
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city},IN&appid={api_key}'

    response = requests.get(url)
    weather_data = json.loads(response.text)
    print(response.status_code)
    print(response.text)

    if 'message' in weather_data:
        return None

    temperature = weather_data['main']['temp']
    temperature_celsius = temperature - 273.15  # Convert from Kelvin to Celsius
    condition = weather_data['weather'][0]['description']
    

    weather_report = f'Current Weather in {city}: {temperature_celsius:.1f}°C, {condition}'
    print(weather_report)
    return weather_report
#----------------------------------------------------------------------------------------------------------------------------------------
# to grt flash news

def get_flash_news():
    api_key = '3eadf74d5da9499d88532c77b5520641'
    url = 'https://newsapi.org/v2/top-headlines'
    params = {'country': 'in', 'apiKey': api_key}

    response = requests.get(url, params=params)
    news_data = json.loads(response.text)

    if news_data['status'] == 'ok':
        articles = news_data['articles']
        news_list = []
        for article in articles:
            title = article['title']
            description = article['description']
            source = article['source']['name']

            # Check if description is not None
            if description is not None:
                new_article = Flash_news(
                    title=title,
                    description=description,
                    source=source,
                    created_at=timezone.now() 
                )
                new_article.save()
                news_list.append(f'Title: {title}\n\nDescription: {description}\n\nSource: {source}\n\n---')
                # print(f'Title: {title}')
                # print(f'Description: {description}')
                # print(f'Source: {source}')
                # print('---')
        return news_list
    else:
        print('Failed to fetch news. Please try again.')
        return None
# def get_flash_news():
#     newsapi = NewsApiClient(api_key = '3eadf74d5da9499d88532c77b5520641')
#     url = 'https://newsapi.org/v2/top-headlines'
#     params = {'country': 'in'}
#     news_data = newsapi.get_top_headlines(**params)    
#     from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
#     tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
#     model = DistilBertForSequenceClassification.from_pretrained('distilbert-base-uncased')
#     if news_data['status'] == 'ok':
#         articles = news_data['articles']
#         news_list = []
#         sentiment_analysis = pipeline("sentiment-analysis", model="distilbert-base-uncased")
       


#         for article in articles:
#             title = article['title']
#             description = article['description']
#             source = article['source']['name']

#             # Check if description is not None
#             # if description is not None:
#             #     # Perform sentiment analysis on description
#             #     sentiment = sentiment_analysis(description)[0]
#             #     sentiment_label = sentiment['label']
#             if description is not None:
#                 encoding = tokenizer.encode_plus(
#                     description,
#                     add_special_tokens=True,
#                     truncation=True,
#                     padding='max_length',
#                     max_length=512,
#                     return_tensors='pt'
#                 )
#                 input_ids = encoding['input_ids']
#                 attention_mask = encoding['attention_mask']

#                 with torch.no_grad():
#                     outputs = model(input_ids=input_ids, attention_mask=attention_mask)

#                 sentiment_label = torch.argmax(outputs.logits).item()

#                 new_article = Flash_news(
#                     title=title,
#                     description=description,
#                     source=source,
#                     sentiment=sentiment_label,
#                     created_at=timezone.now()
#                 )
#                 new_article.save()

#                 news_list.append(f'Title: {title}\n\nDescription: {description}\n\nSentiment: {sentiment_label}\n\nSource: {source}\n\n---')

#         return news_list
#     else:
#         print('Failed to fetch news. Please try again.')
#         return None
#--------------------------------------------------------------------------------------------------------------------------------------------
# Transcribe voice comment
def transcribe_voice_comment(voice_file):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak something in Tamil...")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio, language='ta-IN')
        print("You said:", text)
    except sr.UnknownValueError:
        print("Sorry, could not understand your speech.")