import { createApp } from 'vue'

//导入ElementPlus组件库
import ElementPlus from 'element-plus';//导入ElementPlus组件库的所有模块和功能
import 'element-plus/dist/index.css';//导入ElementPlus组件所需的全局Css样式
import * as ElementPlusIconsVue from '@element-plus/icons-vue';//导入ElementPlus组件库的图标库

import App from './App.vue'
const app=createApp(App)

for (const[key,component] of Object.entries(ElementPlusIconsVue)){
    app.component(key,component)
}
app.use(ElementPlus)
app.mount('#app')
