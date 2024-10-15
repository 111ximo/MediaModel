<script setup>
import { ref } from 'vue';
import { Top, Comment, UserFilled } from '@element-plus/icons-vue';
const userMessage = ref('');//存储用户输入的消息
const messages = ref([]);//存储所有的聊天记录
const activeButton=ref('');
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
const setActiveButton = (button) => {
    activeButton.value = button;
};

</script>

<template>
    <div class="container">
        <div class="aside">
            <el-button class="button" :class="{ 'is-active': activeButton === 'chat' }" @click="setActiveButton('chat')">
                <el-icon><Comment /></el-icon>
                <span>对话</span></el-button><br />
            <el-button class="button" :class="{ 'is-active': activeButton === 'user' }" @click="setActiveButton('user')">
                <el-icon :size="30"><UserFilled /></el-icon>
                <span>主页</span></el-button>
        </div>
        <div class="chat-container">
            <div class="background"><el-icon>
                    <Service />
                </el-icon>
                <span class="background-text">What can I help you?</span>
            </div>
            <div class="messages">
                <div v-for="(msg, index) in messages" :key="index"
                    :class="['message', msg.role === 'User' ? 'user-message' : 'assistant-message']">
                    <strong>{{ msg.role }}:</strong> {{ msg.content }}
                </div>
            </div>
            <div class="input_container">
                <input class="input" v-model="userMessage" @keyup.enter="sendMessage"
                    placeholder="Type your message..." />

                <el-button round @click="sendMessage" class="input-button" icon="Top" />


            </div>
        </div>
    </div>
</template>



<style>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    font-family: 'Arial', sans-serif;
    
}
.container {
    display: flex;
    height: 100vh;
    /* 使容器占满整个视口高度 */
    width:100vw;
    background: linear-gradient(to right, #9473f4, #917bf3,#d5daff,#c8c3ff,#d6dbff);
    align-items: center;
}


.aside {
    display: flex;
    flex-direction: column;
    /* 改为纵向排列 */
    width: 5%;
    height: 100%;
    background-color: none;
    align-items: center;
    /* 子元素居中 */
    justify-content: flex-start;
    /* 子元素从顶部开始排列 */
}

.button {
    display: flex;
    flex-direction: column; /* 垂直排列 */
    justify-content: center; /* 水平居中 */
    align-items: center;     /* 垂直居中 */
    width: 100%;
    height: 100px;
    margin: 0;
    background-color: #9473f4;
    color: #c8c3ff;
    text-align: center; /* 确保文字居中 */
    border: none;
}

.button .el-icon {
    margin-bottom: 10px; /* 图标和文字之间的间距 */
    font-size:30px;
    margin-left: 7px;
}

.button span {
    display: block; /* 确保文字单独占一行 */
    font-size:15px;
}

.button:hover {
    background-color: #9473f4;
    color: white;
}
.container .aside .is-active {
    background-color: #9473f4;
    color: white;
}

.chat-container {
    flex: 1;
    display: flex;
    margin: 0;
    max-width: 88%;
    height: 98%;
    border: none;
    padding: 10px;
    flex-direction: column;
    background:white;
    /* 使子元素垂直排列 */
    border-radius: 30px;
}

.background {
    position: absolute;
    top: 50%;
    left: 60%;
    transform: translate(-50%, -50%);
    width: 15%;
    height: 3%;
    z-index: -1;
}

.background-text {
    margin-left: 10px;
    font-size: 20px;
    color: rgba(0, 0, 0, 0.5);
}

.messages {
    flex: 1;
    overflow-y: auto;
    margin-bottom: 10px;
    z-index: 1;
}

.user-message {
    margin: 20px 0;
    width: 30%;
    border-radius: 5px;
    /* User 消息的背景色 */
    margin-left: auto;
    /* 向右对齐 */
    text-align: right;
    margin-right:20%;
    font-size: 20px;
    z-index: 1;
}

.assistant-message {
    margin: 5px 0;
    /* Assistant 消息的背景色 */
    margin-right: auto;
    /* 向左对齐 */
    text-align: left;
    font-size: 20px;
    margin-left:20%;
    z-index: 1;
}

.input_container {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 0;
    /* 添加顶部边框 */
    justify-content: center;
    width:100%;
}

.input {
    flex:1;
    width: 100%;
    height: 50px;
    border: 1px solid #ccc;
    padding: 5px;
    color: rgba(244, 244, 244, 255);
    border-radius: 30px;


}

.input:hover{
    border: 1px solid #9473f4;
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
