import json
import boto3

# boto3クライアントの作成
client = boto3.client("bedrock-runtime", region_name = "us-west-2")

# Bedrockのモデルにリクエストを送信
response = client.invoke_model(
    body = json.dumps(
        {
            #  Anthropic APIのバージョン指定
            "anthropic_version": "bedrock-2023-05-31",
            # 最大トークン数
            "max_tokens": 1000,
            # 出力のランダム性を指定するパラメータ
            "temperature": 0.9,
            # トップPサンプリングのパラメータ（出力候補の上位何％から選ぶかを決定）
            "top_p": 0.9,
            # モデルに与える入力メッセージ
            "messages": [
                {
                    # ユーザーの役割を指定
                    "role": "user",
                    # プロンプトの入力
                    "content": "俳句を一句読んでください",
                }
            ]
        }
    ),
    # モデルIDを指定
    modelId = "anthropic.claude-3-haiku-20240307-v1:0",
    # レスポンスの形式を指定
    accept = "application/json",
    # リクエストの形式を指定
    contentType = "application/json",
)

# responseのbodyから読み取り、JSONとしてロードする
response_body = json.loads(response.get("body").read())
# 回答の内容を抽出
answer = response_body["content"][0]["text"]

# 生成した回答の出力
print(answer)
