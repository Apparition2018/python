from flask import Flask, request, jsonify

# 创建 Flask 应用实例
app = Flask(__name__)

# 注册路由 /dingtalk
@app.route('/dingtalk', methods=['POST'])
def handle_receive_message():
    data = request.get_json()
    print(f'接收到的钉钉消息：\n{data}')
    return jsonify(data), 200

# 当此脚本直接运行时（而非被导入），启动应用
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9527)


# apt install python3 -y
# apt install python3-pip
# apt install python3.12-venv
# python3 -m venv dingTalk
# source dingTalk/bin/activate
# pip3 install flask
# python3 dingtalk_webhook.py
# curl -X POST http://103.217.186.118:9527/dingtalk -H "Content-Type: application/json" -d "{\"msgtype\": \"text\", \"text\": {\"content\": \"test\"}}"
