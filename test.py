import google.generativeai as genai

gemini_api_key = "AIzaSyCFguD8TZHEO02XSs4kwcJ-ioFxbBcgA6E"
genai.configure(api_key=gemini_api_key)

model =genai.GenerativeModel("gemini-2.0-flash")

chat = model.start_chat()
response = chat.send_message("Hello")
print("gemini:", response.text)