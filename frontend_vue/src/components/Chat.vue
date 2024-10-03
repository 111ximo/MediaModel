<script setup>
import { ref } from 'vue';
import { Top, House, User } from '@element-plus/icons-vue';
const userMessage = ref('');//存储用户输入的消息
const messages = ref([]);//存储所有的聊天记录

const sendMessage = async () => {
    if (!userMessage.value) return;
    //添加用户消息到聊天记录
    messages.value.push({ role: 'User', content: userMessage.value });

    const response = await fetch('http://localhost:5000/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: userMessage.value }),
    });

    if (response.ok) {
        const reader = response.body.getReader();
        const decoder = new TextDecoder("utf-8");
        let done, value;

        while ({ done, value } = await reader.read(), !done) {
            const chunk = decoder.decode(value, { stream: true });
            const newMessages = chunk.split("\n\n").filter(Boolean);
            for (const message of newMessages) {
                if (message.startsWith("data: ")) {
                    const content = message.substring(6);
                    messages.value.push({ role: 'Assistant', content });
                }
            }
        }
    }

    userMessage.value = '';
};

</script>

<template>
    <div class="container">
        <div class="aside">
            <el-button class="button">
                <el-icon class="icon">
                    <House />
                </el-icon>
                <span class="button-text">MediaChat</span></el-button><br />
            <el-button class="button">
                <el-icon class="icon">
                    <User />
                </el-icon>
                <span class="button-text">Chat</span></el-button>
        </div>
        <div class="chat-container">
            <div class="messages">
                <div v-for="(msg, index) in messages" :key="index"
                    :class="['message', msg.role === 'User' ? 'user-message' : 'assistant-message']">
                    <strong>{{ msg.role }}:</strong> {{ msg.content }}
                </div>
            </div>
            <div class="input_container">
                <el-input class="input" v-model="userMessage" @keyup.enter="sendMessage"
                    placeholder="Type your message..." />

                <el-button @click="sendMessage" class="input-button" icon="Top" />


            </div>
        </div>
    </div>
</template>



<style>
.container {
    display: flex;
    height: 96vh;
    /* 使容器占满整个视口高度 */
}


.aside {
    display: flex;
    flex-direction: column;
    /* 改为纵向排列 */
    width: 15%;
    height: 100%;
    background-color: rgba(249, 249, 249, 1);
    align-items: center;
    /* 子元素居中 */
    justify-content: flex-start;
    /* 子元素从顶部开始排列 */

}

.aside .icon {
    margin-right: 8px;
}


.button {
    width: 100%;
    /* 确保按钮占满一行的宽度 */
    height: 50px;
    margin: 0;
    /* 调整垂直间距 */
    background-color: rgba(249, 249, 249, 1);
    text-align: left;
    /* 文本左对齐 */
    border: none;
}

.button:hover {
    background-color: rgba(236, 236, 236, 255);
    color: black;
}

.chat-container {
    flex: 1;
    display: flex;
    margin: 0;
    max-width: 85%;
    height: 100%;
    border: none;
    padding: 10px;
    flex-direction: column;
    /* 使子元素垂直排列 */
}

.messages {
    flex: 1;
    overflow-y: auto;
    margin-bottom: 10px;
}

.user-message {
    margin:20px 0;
    width:30%;
    border-radius: 5px;
    /* User 消息的背景色 */
    margin-left: auto;
    /* 向右对齐 */
    text-align: right;
}

.assistant-message {
    margin: 5px 0;
    /* Assistant 消息的背景色 */
    margin-right: auto;
    /* 向左对齐 */
    text-align: left;
}

.input_container {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 0;

    /* 添加顶部边框 */
    justify-content: center;
}

.input {
    width: 300px;
    height: 50px;
    border: none;
    padding: 5px;
    color: rgba(244, 244, 244, 255);

}

.input-button {
    background-color: #ccc;
    height: 40px;
    color: white;
    border: none;
    cursor: pointer;
    border-radius: 5px;
}

.input-button:hover {
    background-color: #999;
    color: black;
}
</style>
