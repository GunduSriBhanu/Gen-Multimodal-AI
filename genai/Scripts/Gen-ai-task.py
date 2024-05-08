#Gen-ai-task.py

# Install **pip install -U "anthropic[bedrock]"** 

import boto3
import json
import os
import base64
import requests
import spacy
from dotenv import load_dotenv
load_dotenv()

#image_path = r"C:\Users\SGundu\Generative AI\genai\Image_Page6_v17.png"
image_path = r"C:\Users\SGundu\Textract-Research\myenv\Scripts\demo-bucket-ifc_reducing_valve\Image_Page2_v5.png"

# Load the English language model
nlp = spacy.load("en_core_web_sm")

bedrock = boto3.client(service_name="bedrock-runtime",aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("AWS_SECRET_KEY"),
    region_name=os.getenv("AWS_REGION"))

body = json.dumps({
    "prompt": "\n\nHuman: explain black holes to 8th graders\n\nAssistant:",
    "max_tokens_to_sample": 300,
    "temperature": 0.1,
    "top_p": 0.9,
})

modelId = 'anthropic.claude-v2'
accept = 'application/json'
contentType = 'application/json'

response = bedrock.invoke_model(body=body, modelId=modelId, accept=accept, contentType=contentType)

response_body = json.loads(response.get('body').read())

# text
#print(response_body.get('completion'))

stream = response.get('body')
if stream:
    for event in stream:
        chunk = event.get('chunk')
        #if chunk:
            #print(json.loads(chunk.get('bytes').decode()))
            
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

base64_image = encode_image(image_path)

def invoke_claude_3_multimodal(prompt, base64_image_data):
        """
        Invokes Anthropic Claude 3 Sonnet to run a multimodal inference using the input
        provided in the request body.

        :param prompt:            The prompt that you want Claude 3 to use.
        :param base64_image_data: The base64-encoded image that you want to add to the request.
        :return: Inference response from the model.
        """

        # Initialize the Amazon Bedrock runtime client
        

        # Invoke the model with the prompt and the encoded image
        model_id = "anthropic.claude-3-sonnet-20240229-v1:0"
        request_body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 2048,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt,
                        },
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/png",
                                "data": base64_image_data,
                            },
                        },
                    ],
                }
            ],
        }

        try:
            response = bedrock.invoke_model(
                modelId=model_id,
                body=json.dumps(request_body),
            )

            # Process and print the response
            result = json.loads(response.get("body").read())
            input_tokens = result["usage"]["input_tokens"]
            output_tokens = result["usage"]["output_tokens"]
            output_list = result.get("content", [])

            #print("Invocation details:")
            #print(f"- The input length is {input_tokens} tokens.")
            #print(f"- The output length is {output_tokens} tokens.")

            #print(f"- The model returned {len(output_list)} response(s):")
            #for output in output_list:
                #print(output["text"])

            return output_list #result
        except ClientError as err:
            logger.error(
                "Couldn't invoke Claude 3 Sonnet. Here's why: %s: %s",
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise

           
sentence_label = invoke_claude_3_multimodal("what the image is about based on labeling in a single sentence?", base64_image)    
sentence_component = invoke_claude_3_multimodal("what the image is about based on product component in a single word?", base64_image)     

sentence = sentence_label[0]['text'] 

# Process the sentence using spaCy
doc = nlp(sentence)

# Extract common nouns
common_nouns = [token.text for token in doc if token.pos_ == "NOUN"]

# Print the extracted common nouns
print("Common Nouns:", common_nouns)

print(invoke_claude_3_multimodal("what is the summary of image?", base64_image)[0]['text'])
