import dashscope
from dashscope import Generation
from dashscope.api_entities.dashscope_response import Role
import os
from dotenv import load_dotenv
from flask import Flask, request, Response, stream_with_context
from flask_cors import CORS

# 加载环境变量
load_dotenv()
dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")

# 创建 Flask 应用
app = Flask(__name__)
CORS(app, resources={r"/chat": {"origins": "http://localhost:5173"}})


@app.route("/chat", methods=["POST"])
def chat_post():
    user_message = request.json.get("message")
    messages = [{"role": Role.USER, "content": user_message}]

    def generate():
        accumulated_messages = []  # 用于累积消息
        print("Generating response...")
        try:
            responses = Generation.call(
                model="qwen1.5-14b-chat",
                messages=messages,
                result_format="message",
                stream=True,
                incremental_output=True,
            )
            for response in responses:
                content = response.output.choices[0]["message"]["content"]
                accumulated_messages.append(content)  # 累积消息

            # 最后一次性返回所有消息
            combined_message = "\n".join(accumulated_messages)
            yield f"data: {combined_message}\n\n"

        except Exception as e:
            print(f"Error occurred: {str(e)}")
            yield f"data: Error occurred: {str(e)}\n\n"

    return Response(stream_with_context(generate()), mimetype="text/event-stream")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
