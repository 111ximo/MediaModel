import dashscope
from dashscope import Generation
from dashscope.api_entities.dashscope_response import Role

import os
from dotenv import load_dotenv
load_dotenv()
dashscope.api_key=os.getenv("DASHSCOPE_API_KEY")

def call_with_messages():
    messages = []
    while True:
        message = input('user:')
        # 将输入信息加入历史对话
        messages.append({'role': Role.USER, 'content': message})
        whole_message = ''
        # 获得模型输出结果
        responses = Generation.call(model='qwen1.5-14b-chat',
                                    messages=messages,
                                    result_format='message',# 设置输出为'message'格式
                                    stream=True, # 设置输出方式为流式输出
                                    incremental_output=True # 增量式流式输出
                                    )
        print('system:',end='')
        for response in responses:
            whole_message += response.output.choices[0]['message']['content']
            print(response.output.choices[0]['message']['content'], end='')
        print()
        # 将输出信息加入历史对话
        messages.append({'role': 'assistant', 'content': whole_message})
        if message == "a":
            break

if __name__ == '__main__':
    call_with_messages()
