from calendar import c
from msilib.schema import Error
import string
from django.shortcuts import render

from .forms import RawPhraseForm, RawPhraseForm_Synonym
import requests
import urllib
import json
from dictionary1.settings import SYNONYMS_URL, TRANSLATE_URL, API_KEY

def synonym_view(request):
    send_form = RawPhraseForm_Synonym(request.POST or None)
    synonyms = ''
    if send_form.is_valid():
        word = send_form.cleaned_data['content']
        synonyms = make_request_synonym(word)
    context = {
        'syn_form': send_form,
        'synonyms1': synonyms[0:20],
        'synonyms2': synonyms[20:40],
        'synonyms3': synonyms[40:60],
    }
    return render(request, "synonym.html", context)

def translate_view(request):
    send_form = RawPhraseForm(request.POST or None)
    translated_word = ''
    if send_form.is_valid():
        word = send_form.cleaned_data['content']
        translate_from = send_form.cleaned_data['translate_from']
        translate_to = send_form.cleaned_data['translate_to']
        translated_word = make_request_translate(word, translate_from, translate_to)
    context = {
        'translate_form': send_form,
        'word': translated_word
    }
    return render(request, "translate.html", context)

def make_request_synonym(word):
    word_url_safe = urllib.parse.quote_plus(word)
    payload = "".join([SYNONYMS_URL,word_url_safe])
    headers = {
        "X-RapidAPI-Host": SYNONYMS_URL.replace("https://", ""),
        "X-RapidAPI-Key": API_KEY
    }
    response = requests.request("GET", payload, headers=headers)
    json_response = response.json()
    try:
        synonyms = json_response['synonyms']
    except:
        return ["Incorrect word"]
    return synonyms

def make_request_translate(word: string, translate_from: string, translate_to: string) -> string:
    word_url_safe = urllib.parse.quote_plus(word)
    querystring = {"q": word_url_safe,"langpair": translate_from + "|" + translate_to}
    headers = {
        "X-RapidAPI-Host": TRANSLATE_URL.replace("/api/get", "").replace("https://", ""),
        "X-RapidAPI-Key": API_KEY
    }
    response = requests.request("GET", TRANSLATE_URL, headers=headers, params=querystring)
    json_response = response.json()
    translated_word = json_response['responseData']['translatedText']
    return translated_word.replace('+', " ")
