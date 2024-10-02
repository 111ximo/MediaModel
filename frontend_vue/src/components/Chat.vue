<script>
export default {
    data() {
        return {
            userMessage: '',
            messages: [],
            eventSource: null
        };
    },
    methods: {
        async sendMessage() {
    if (!this.userMessage) return;

    this.messages.push({ role: 'User', content: this.userMessage });

    // 发送 POST 请求，后台将开始流式输出
    const response = await fetch('http://localhost:5000/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: this.userMessage }),
    });

    // 处理流式响应
    if (response.ok) {
        const reader = response.body.getReader();
        const decoder = new TextDecoder("utf-8");
        let done, value;

        // 持续读取数据
        while ({ done, value } = await reader.read(), !done) {
            const chunk = decoder.decode(value, { stream: true });
            // 处理接收到的每一块数据
            const messages = chunk.split("\n\n").filter(Boolean);
            for (const message of messages) {
                if (message.startsWith("data: ")) {
                    const content = message.substring(6); // 去掉前缀
                    this.messages.push({ role: 'Assistant', content });
                }
            }
        }
    }

    // 清空输入框
    this.userMessage = '';
}
    },
    beforeDestroy() {
        if (this.eventSource) {
            this.eventSource.close(); // 组件销毁时关闭连接
        }
    }
};
</script>

<template>
    <div class="chat-container">
        <div class="messages">
            <div v-for="(msg, index) in messages" :key="index" class="message">
                <strong>{{ msg.role }}:</strong> {{ msg.content }}
            </div>
        </div>
        <input v-model="userMessage" @keyup.enter="sendMessage" placeholder="Type your message..." />
    </div>
</template>



<style>
.chat-container {
    max-width: 600px;
    margin: auto;
    border: 1px solid #ccc;
    padding: 10px;
}

.messages {
    max-height: 400px;
    overflow-y: auto;
    margin-bottom: 10px;
}

.message {
    margin: 5px 0;
}
</style>