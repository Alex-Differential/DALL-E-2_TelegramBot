import openai
openai.api_key = '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'
openai.Model.list()

photo = openai.Image.create(
        prompt = "Biden play in poker on the beach",
        n = 2,
        size = "1024x1024"
        )
print(photo)
#image_url = photo['data'][0]['url']