import google.generativeai as genai
genai.configure(api_key="your_api_key_here")  
model = genai.GenerativeModel("gemini-2.5-pro")
response = model.generate_content("i am a virtual assistant, how can i help you?")
print(response.text)


