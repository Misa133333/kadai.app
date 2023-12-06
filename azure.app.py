from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
import os
from PIL import Image
import sys
import time

# APIキーとエンドポイントを環境変数から取得
key = os.environ["COMPUTER_VISION_SUBSCRIPTION_KEY"]
endpoint = os.environ["COMPUTER_VISION_ENDPOINT"]

# クライアントを認証して初期化
computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(key))

# 画像解析用の関数
def analyze_image(image_path):
    # 画像をバイナリファイルとして開く
    with open(image_path, "rb") as image_stream:
        analysis = computervision_client.analyze_image_in_stream(image_stream, visual_features=[VisualFeatureTypes.tags])
    
    # 解析結果を返す
    return analysis

# テスト画像のパス
image_path = "C:\\Users\\nagata\\Desktop\\OIP.jpg"


# 画像解析を実行
analysis_result = analyze_image(image_path)

# 結果の出力
for tag in analysis_result.tags:
    print(f"Tag: {tag.name}, Confidence: {tag.confidence}")

# 物語生成関数
def generate_story(tags):
    # 最初の数個のタグを使って物語を生成
    primary_tags = tags[:5] # 最初の3つのタグを使用
    story = f"In a tranquil scene, a {primary_tags[0].name} gently sways in the breeze, surrounded by {primary_tags[1].name} and {primary_tags[2].name}."
    return story

# 画像解析を実行
analysis_result = analyze_image(image_path)

# 結果の出力
for tag in analysis_result.tags:
    print(f"Tag: {tag.name}, Confidence: {tag.confidence}")

def generate_complex_story(tags):
    # タグをカテゴリーに分類
    nature_tags = ['plant', 'flower', 'tree']
    object_tags = ['car', 'house', 'street']
    
    # ストーリーの初期化
    story = ""

    # 自然に関するタグがある場合のストーリー
    if any(tag.name in nature_tags for tag in tags):
        story += "In a serene forest, surrounded by towering trees and vibrant flowers, a small path winds its way through the underbrush. "

    # 物体に関するタグがある場合のストーリー
    if any(tag.name in object_tags for tag in tags):
        story += "Alongside the path, an old abandoned car lies, its history a mystery to those who stumble upon it. "

    # タグが特定のカテゴリーに当てはまらない場合
    if story == "":
        story = "It's a world full of unexpected wonders and stories untold."

    return story

# 物語を生成
story = generate_complex_story(analysis_result.tags)

# 物語の出力
print("Generated Story:", story)