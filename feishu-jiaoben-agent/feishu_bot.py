import json
import requests
from flask import Flask, request, jsonify
from scripts.structure_parser import GameScriptStructureParser
from scripts.template_generator import GameScriptTemplateGenerator

app = Flask(__name__)

# ================= 极其重要的配置区 =================
FEISHU_APP_ID = "cli_a930d68a7b789cee"
FEISHU_APP_SECRET = "n47cN7zkbrIhlGa3yLTcDf3lWuMu7yLj"
GEMINI_API_KEY = "AIzaSyCLEIfqm5LvrD5qf9VPWYMGkrBLsQKiTH"
# ====================================================

parser = GameScriptStructureParser(api_key=GEMINI_API_KEY)
generator = GameScriptTemplateGenerator()

def get_tenant_access_token():
    url = "[https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal)"
    payload = {"app_id": FEISHU_APP_ID, "app_secret": FEISHU_APP_SECRET}
    res = requests.post(url, json=payload).json()
    return res.get("tenant_access_token")

def send_message(message_id, content):
    token = get_tenant_access_token()
    url = f"[https://open.feishu.cn/open-apis/im/v1/messages/](https://open.feishu.cn/open-apis/im/v1/messages/){message_id}/reply"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    payload = {
        "msg_type": "text", 
        "content": json.dumps({"text": content})
    }
    requests.post(url, headers=headers, json=payload)

@app.route('/webhook', methods=['POST'])
def feishu_event():
    data = request.json
    
    # 1. 应对飞书配置时的 URL 验证挑战
    if "challenge" in data:
        return jsonify({"challenge": data["challenge"]})
    
    # 2. 拦截并处理用户发来的消息
    event = data.get("event", {})
    message = event.get("message", {})
    
    if message.get("message_type") == "text":
        user_text = json.loads(message["content"]).get("text")
        message_id = message["message_id"]
        
        # 发送处理中的提示
        send_message(message_id, "⏳ 脑洞已接收，正在呼叫 AI 拆解美术资源和视频分镜...")
        
        # 核心处理管线
        analysis = parser.analyze_document_structure(user_text)
        final_md = generator.create_lark_document(analysis)
        
        # 发送最终结果
        send_message(message_id, final_md)

    return jsonify({"msg": "success"})

if __name__ == '__main__':
    app.run(port=8000)