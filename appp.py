from flask import Flask, request, render_template
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
import os

# Azureの設定を環境変数から読み込む
key = os.environ["COMPUTER_VISION_SUBSCRIPTION_KEY"]
endpoint = os.environ["COMPUTER_VISION_ENDPOINT"]

# Azureのコンピュータービジョンクライアントを初期化
computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(key))

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
        if file:
            analysis = computervision_client.analyze_image_in_stream(file.stream, visual_features=[VisualFeatureTypes.tags])
            story = generate_complex_story(analysis.tags)
            return "Generated Story: " + story
    return render_template('upload.html')

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

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    app.run(host ='0.0.0.0',port = port)
