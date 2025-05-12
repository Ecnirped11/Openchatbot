import requests

url = "https://text.pollinations.ai/openai'"

class ChatBotResponse:
  
  def __init__(self , prompt):
    self.prompt = prompt
    self.status = False
    
  def post_content(self) -> str:
    data = {
      "model" : 'openai-gpt-3',
      "messages": [{ 'role': 'user','content': self.prompt }]
    }
    headers = {
      'content-type' : 'application/json',
    }
    
    try:
      response = requests.post(url , headers=headers , json=data)
      return response.json()
    except requests.RequestException as e:
      print(f'error : {e}')
    
  def response(self) -> str:
    result = self.post_content()
    pick = result['choices'][0]['message']['content']
    return pick

  