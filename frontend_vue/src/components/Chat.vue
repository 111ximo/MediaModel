<script setup>
import { ref, onBeforeUnmount } from 'vue';

const userMessage = ref('');
const messages = ref([]);

const sendMessage = async () => {
    if (!userMessage.value) return;

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

onBeforeUnmount(() => {
    // 可以在这里关闭连接等清理操作
});
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
