

# pdf文本复制翻译小插件



### Version 2.0

- [x] UI界面完善
- [x] 自动检测txt中的key，选择可用翻译器
- [x] 使用说明
- [x] 翻译开关，格式转换开关
- [x] 复制按钮
- [ ] 翻译对比

------



#### 一、申请API：

（Rapid API、有道翻译API、百度翻译API，申请其中一个即可使用该插件）

（1）Rapid API：[API Hub - Free Public & Open Rest APIs | Rapid (rapidapi.com)](https://rapidapi.com/hub)

- 注册账号
- 搜索 Text Translator、Microsoft Translator Text、Google Translator
- 点击进入对应API界面
- 点击Subscribe to Test

![API_leader](C:\Users\zjx\Desktop\API_leader.png)

- 选择免费方案，点击Subscribe 

  <img src="https://pasery-markdown-image.oss-cn-hangzhou.aliyuncs.com/img/202304192145852.png" alt="API_leader1" style="zoom:67%;" />

- 显示如下界面则表示订阅成功，点击 API Documentation，进入API使用文档界面

  <img src="https://pasery-markdown-image.oss-cn-hangzhou.aliyuncs.com/img/202304192148531.png" alt="API_leader2" style="zoom:67%;" />

- 复制key

  <img src="https://pasery-markdown-image.oss-cn-hangzhou.aliyuncs.com/img/202304192149080.png" alt="API_leader3" style="zoom:67%;" />

- 粘贴到txt文件内的Other_API_Key中。

**注意，该网站的API是通用的，因此只需要复制一个即可，但是本插件中 Text Translator、Microsoft Translator Text、Google Translator三个翻译器必须都要订阅才能使用。**



（2）有道API申请：[有道智云AI开放平台 (youdao.com)](https://ai.youdao.com/?keyfrom=fanyi-new-nav#/)

（3）百度API申请：[百度翻译开放平台 (baidu.com)](https://fanyi-api.baidu.com/?fr=pcHeader)



***APIKey.txt需要与exe放在同一文件夹下***

------



#### 二、使用说明：

<img src="https://pasery-markdown-image.oss-cn-hangzhou.aliyuncs.com/img/202304192155032.png" alt="API_leader4" style="zoom:50%;" />

- 打开插件时，默认为翻译模式，使用有道翻译。
- 在翻译模式下，只需要复制文本内容即可完成翻译。复制的pdf文本内容将会首先进行格式转换，去掉换行符，然后自动完成翻译。
- 在仅转换复制格式的模式下，复制pdf内容后仅会进行格式转换，去掉换行符，并将转换内容覆盖剪切板当前内容，不会执行翻译任务，此模式下，可直接复制pdf内容到其他在线翻译器中完成翻译。（在使用Deepl等API付费翻译器，或已有API用量不足时可使用该模式）。
- 点击复制按钮可复制翻译完毕的内容，注意不要手动选中文本框中的内容复制，否则又会将复制内容进行翻译。



#### 三、查看API用量：

Rapid API：[Billing, Subscriptions And Usage | Rapid API Hub | Developer Dashboard](https://rapidapi.com/developer/billing/subscriptions-and-usage)

有道翻译：[有道智云控制台 (youdao.com)](https://ai.youdao.com/console/#/)

百度翻译：[百度翻译开放平台 (baidu.com)](https://fanyi-api.baidu.com/api/trans/product/desktop?fr=pcHeader)



## 特别注意，使用时请勿开启代理，否则可能会出错