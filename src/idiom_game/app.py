import random
from datetime import datetime

from cozepy import Coze, TokenAuth, COZE_CN_BASE_URL, Message, ChatStatus
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

COMMON_IDIOMS = ['一心一意', '三心两意']

class IdiomGame:
    def __init__(self):
        self.api_token = 'pat_whdBDYsJ5yf1LRJBAMaYhXHOmTSNA8p8weBMLSoF9pER6D5YYO9tERZzigW1gd0r'
        self.bot_id = '7645743701784002598'
        self.user_id = '572058451'
        self.current_idiom = random.choice(COMMON_IDIOMS)
        self.game_history = []
        self.coze = Coze(auth=TokenAuth(token=self.api_token), base_url=COZE_CN_BASE_URL)

    def add_to_history(self, user_idiom, sdk_response):
        record = {
            "user": user_idiom,
            "ai": sdk_response,
            "timestamp": datetime.now().strftime("%H:%M:%S")
        }
        self.game_history.insert(0, record)
        if len(self.game_history) > 20:
            self.game_history = self.game_history[:20]

    def reset_game(self):
        self.current_idiom = random.choice(COMMON_IDIOMS)
        self.game_history = []
        return {
            'success': True,
            'current_idiom': self.current_idiom,
            'history': self.game_history
        }

    # 获取机器人回复
    def get_bot_response(self, user_input):
        try:
            messages = [
                Message.build_user_question_text(f"成语接龙游戏，上一个成语是: {self.current_idiom}，请接下一个成语"),
                Message.build_user_question_text(user_input),
            ]

            # 向 Coze 机器人发送消息
            chat = self.coze.chat.create(
                bot_id=self.bot_id,
                user_id=self.user_id,
                additional_messages=messages,
                auto_save_history=True
            )

            while chat.status == ChatStatus.IN_PROGRESS:
                chat = self.coze.chat.retrieve(
                    conversation_id=chat.conversation_id,
                    chat_id=chat.id
                )

            if chat.status == ChatStatus.COMPLETED:
                messages = self.coze.chat.messages.list(
                    conversation_id=chat.conversation_id,
                    chat_id=chat.id
                )

                bot_response = None
                for msg in messages:
                    if hasattr(msg, 'role') and msg.role == 'assistant':
                        bot_response = msg.content.strip()
                        print(bot_response)
                        bot_response = "".join(filter(lambda x: '\u4e00' <= x <= '\u9fff', bot_response))
                        break

                if bot_response and len(bot_response) == 4:
                    self.add_to_history(user_input, bot_response)
                    self.current_idiom = bot_response
                    return {
                        'success': True,
                        'bot_response': bot_response,
                        'current_idiom': self.current_idiom,
                        'history': self.game_history
                    }

            return {'success': False, 'error': '输入的词语不是有效成语或AI无法接龙，请重新输入'}
        except Exception as e:
            return {"success": False, "error": str(e)}

game = IdiomGame()


@app.route('/')
def index():
    return render_template('index.html', api_base_url=request.host_url.rstrip('/') + '/api')


@app.route('/api/restart', methods=['POST'])
def restart_game():
    result = game.reset_game()
    return jsonify(result)


# curl -X POST http://127.0.0.1:5000/api/play -H "Content-Type: application/json" -d "{\"idiom\": \"一心一意\"}"
@app.route('/api/play', methods=['POST'])
def play_game():
    data = request.get_json()
    user_input = data.get('idiom', '').strip()
    if len(user_input) != 4:
        return jsonify({'error': '请输入4字成语'})
    result = game.get_bot_response(user_input)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
