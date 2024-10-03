import boto3

client = boto3.client("bedrock-runtime", region_name="us-west-2")

streaming_response = client.converse_stream(
    modelId = "anthropic.claude-3-5-sonnet-20240620-v1:0",
    messages = [
        {
            "role": "user", 
            "content": [
                {
                    "text": "夏の俳句を1句詠んで"
                }
            ]
        }
    ],
)

for chunk in streaming_response["stream"]:
    if "contentBlockDelta" in chunk:
        text = chunk["contentBlockDelta"]["delta"]["text"]
        print(text, end="")

# import json
# import boto3

# client = boto3.client("bedrock-runtime", region_name="us-west-2")

# # リクエストボディの作成
# streaming_response = client.converse_stream(
#     modelId="anthropic.claude-3-5-sonnet-20240620-v1:0",
#     messages=[
#         {
#             "role": "user",
#             "content": [
#                 {
#                     "text": "夏の俳句を詠んで"
#                 }
#             ]
#         }
#     ],
#     inferenceConfig={
#         "maxTokens": 10  # max_tokensの設定を追加
#     }
# )

# # streaming_response = client.converse_stream(**request_body)

# for chunk in streaming_response["stream"]:
#     if "contentBlockDelta" in chunk:
#         text = chunk["contentBlockDelta"]["delta"]["text"]
#         print(text, end="")
