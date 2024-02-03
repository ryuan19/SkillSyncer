import requests
import base64

def usegpt4v(api_key0, prompt0, image_path0):
  #encode img
  def encode_image(image_path0):
    with open(image_path0, "rb") as image_file:
      return base64.b64encode(image_file.read()).decode('utf-8')

  # get base64 string
  base64_image = encode_image(image_path0)

  headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key0}"
  }

  payload = { #can change hyperparams here
    "model": "gpt-4-vision-preview",
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": prompt0
          },
          {
            "type": "image_url",
            "image_url": {
              "url": f"data:image/jpeg;base64,{base64_image}"
            }
          }
        ]
      }
    ],
    "max_tokens": 300
  }

  response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
  return response.json()

sample_resume = "/Users/royyuan/Desktop/resumes/olivia.png"
prompt = "Here is an image of a resume, summarize it for me."
api_key = "ENTER OUR API KEY"
res = usegpt4v(api_key, prompt, sample_resume)
print(res['choices'][0]['message']['content'])
