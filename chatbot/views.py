from django.shortcuts import render
from django.http import HttpResponse
import openai
# from openai import OpenAI

# Create your views here.

client = openai.OpenAI(api_key=<Openai API Key>)


openai_api_key = <Openai API Key>

def ask_openai(message):
    response = client.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages = [{"role": "user", "content": message}],
        # max_tokens=150,
        # n=1,
        # stop=None,
        # temperature=0.7,
        )
    return response.choices[0].message.content



def chatbot(request):
	return render(request, 'chatbot.html', {'title': 'Chatbot'})

def getResponse(request):

	userMessage = request.GET.get('userMessage')
	response_openai = ask_openai(userMessage)
	return HttpResponse(response_openai)
