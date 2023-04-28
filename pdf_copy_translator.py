import pyperclip
import requests
import json
import uuid
import hashlib
import time
import re
from hashlib import md5
import random
import ttkbootstrap as ttk
from tkinter.font import Font
import tkinter as tk
import tkinter.messagebox

def getAPIKey():
    APIKey_dict = {}
    with open('APIKey.txt', 'r') as f:
        for line in f:
            match = re.search('([^=]*)\s*=\s*"([^"]*)"', line)
            if match:
                key = match.group(1).strip()
                value = match.group(2).strip()
                if value:  # 如果值不为空，则存储到字典对象APIKey_dict中
                    APIKey_dict[key] = value

    return APIKey_dict


def getAvailableTranslateTools(APIKey_dict):
    available_translate_tools = []
    if "Youdao_API_Key" in APIKey_dict and "Youdao_API_secret" in APIKey_dict:
        available_translate_tools.append("youdao")
    if "Other_API_Key" in APIKey_dict:
        available_translate_tools.extend(["Text Translator", "Google Translator", "Microsoft Translator"])
    if "Baidu_API_ID" in APIKey_dict and "Baidu_API_Key" in APIKey_dict:
        available_translate_tools.append("Baidu")
    return available_translate_tools

class TranslateWindow:
    def __init__(self, master, translate_tools, APIKey_dict):
        # API KEY
        self.API_Key = APIKey_dict.get("Other_API_Key", "")
        self.Youdao_API_Key = APIKey_dict.get("Youdao_API_Key", "")
        self.Youdao_API_secret = APIKey_dict.get("Youdao_API_secret", "")
        self.Baidu_API_ID = APIKey_dict.get("Baidu_API_ID", "")
        self.Baidu_API_Key = APIKey_dict.get("Baidu_API_Key", "")

        self.translate_tools = translate_tools
        self.master = master
        self.master.title("复制翻译")
        self.options = {item: index+1 for index, item in enumerate(translate_tools)}
        self.selected_option = ttk.StringVar(self.master)
        self.selected_option.set(translate_tools[0])
        self.selected_option.trace('w', self.optionChanged)
        self.current_option = self.options[self.selected_option.get()]
        self.last_selected_text = ""
        self.translated_text = ""
        self.temp_text = ""
        self.last_option = 1
        self.is_copy = False
        self.createWidgets()
        self.updateClipboard()


    def createWidgets(self):
        font = Font(size=12)
        self.v = tk.StringVar(value="translate") # 创建变量v，用于存储选择的选项
        # 创建两个Radiobutton作为二选一的选择框
        radio_button_translate = ttk.Radiobutton(self.master, text="翻译", variable=self.v, value="translate", bootstyle="info-outline-toolbutton", width=15)
        radio_button_copy = ttk.Radiobutton(self.master, text="仅转换复制格式", variable=self.v, value="copy", bootstyle="info-outline-toolbutton", width=15)
        # 使用网格布局管理控件
        radio_button_translate.grid(row=0, column=0, pady=10, padx=20)
        radio_button_copy.grid(row=0, column=1, pady=10, padx=20)
        self.combo_box = ttk.Combobox(self.master, values=list(self.options.keys()), textvariable=self.selected_option, state="readonly", bootstyle="primary")
        self.combo_box.current(0)
        self.combo_box.bind("<<ComboboxSelected>>", self.optionChanged)
        self.combo_box.grid(row=1, column=0, columnspan=2, pady=15, padx=10)
        self.text_box = ttk.Text(self.master, height=10, width=47)
        self.text_box.grid(row=2, column=0, columnspan=2, pady=15, padx=10)
        self.text_box.configure(font=font,spacing1=10,spacing2=5)
        self.copy_button = ttk.Button(self.master,text="复制",command=self.copyTextBox,width=5)
        self.copy_button.grid(row=1, column=1, pady=15, padx=10, sticky="e")
        
    def copyTextBox(self):
        self.is_copy = True
        self.temp_text = pyperclip.paste()
        pyperclip.copy(self.translated_text)
        self.last_selected_text = pyperclip.paste()

    def transformSelectPdf(self, input_text):
        output_text = re.sub(r'\r\n\s*', ' ', input_text)
        return output_text

    def requestsUrl(self, text, select_translate_tools):
        if select_translate_tools == "Text Translator":
            url = "https://text-translator2.p.rapidapi.com/translate"

            payload = "source_language=en&target_language=zh&text=" + text
            headers = {
                "content-type": "application/x-www-form-urlencoded",
                "X-RapidAPI-Key": self.API_Key,
                "X-RapidAPI-Host": "text-translator2.p.rapidapi.com"
            }

            response = requests.request("POST", url, data=payload, headers=headers)
            json_data = response.json()
            translated_text = json_data["data"]["translatedText"]

        elif select_translate_tools == "Google Translator":
            url = "https://google-translator9.p.rapidapi.com/v2"

            payload = {
                "q": text,
                "source": "en",
                "target": "zh-CN",
                "format": "text"
            }
            headers = {
                "content-type": "application/json",
                "X-RapidAPI-Key": self.API_Key,
                "X-RapidAPI-Host": "google-translator9.p.rapidapi.com"
            }

            response = requests.request("POST", url, json=payload, headers=headers)
            json_data = response.json()
            translated_text = json_data['data']['translations'][0]['translatedText']

        elif select_translate_tools == "Microsoft Translator":
            url = "https://microsoft-translator-text.p.rapidapi.com/translate"

            querystring = {"to[0]": "<REQUIRED>", "api-version": "3.0", "profanityAction": "NoAction",
                           "textType": "plain", "from": "en", 'to': "zh"}

            payload = [{"Text": text}]
            headers = {
                "content-type": "application/json",
                "X-RapidAPI-Key": self.API_Key,
                "X-RapidAPI-Host": "microsoft-translator-text.p.rapidapi.com"
            }

            response = requests.request("POST", url, json=payload, headers=headers, params=querystring)
            data = json.loads(response.text)
            translated_text = data[0]['translations'][0]['text']

        elif select_translate_tools == "Baidu":
            from_lang = 'en'
            to_lang =  'zh'

            endpoint = 'http://api.fanyi.baidu.com'
            path = '/api/trans/vip/translate'
            url = endpoint + path

            query = text

            # Generate salt and sign
            def make_md5(s, encoding='utf-8'):
                return md5(s.encode(encoding)).hexdigest()

            salt = random.randint(32768, 65536)
            sign = make_md5(self.Baidu_API_ID + query + str(salt) + self.Baidu_API_Key)

            # Build request
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            payload = {'appid': self.Baidu_API_ID, 'q': query, 'from': from_lang, 'to': to_lang, 'salt': salt, 'sign': sign}

            # Send request
            r = requests.post(url, params=payload, headers=headers)
            result = r.json()
            translated_text = result['trans_result'][0]['dst']

        else:
            YOUDAO_URL = 'https://openapi.youdao.com/api'

            def encrypt(signStr):
                hash_algorithm = hashlib.sha256()
                hash_algorithm.update(signStr.encode('utf-8'))
                return hash_algorithm.hexdigest()


            def truncate(q):
                if q is None:
                    return None
                size = len(q)
                return q if size <= 20 else q[0:10] + str(size) + q[size - 10:size]


            def do_request(data):
                headers = {'Content-Type': 'application/x-www-form-urlencoded'}
                return requests.post(YOUDAO_URL, data=data, headers=headers)
            
            q = text

            data = {}
            data['from'] = 'en'
            data['to'] = 'zh'
            data['signType'] = 'v3'
            curtime = str(int(time.time()))
            data['curtime'] = curtime
            salt = str(uuid.uuid1())
            signStr = self.Youdao_API_Key + truncate(q) + salt + curtime + self.Youdao_API_secret
            sign = encrypt(signStr)
            data['appKey'] = self.Youdao_API_Key
            data['q'] = q
            data['salt'] = salt
            data['sign'] = sign

            response = do_request(data)
            response_dict = json.loads(response.text)
            translated_text = response_dict['translation'][0]

        return translated_text
    

    def translateText(self,selected_text):
        self.text_box.delete("1.0", ttk.END)
        transform_text = self.transformSelectPdf(selected_text)
        self.translated_text = self.requestsUrl(transform_text, self.translate_tools[self.current_option - 1])
        self.text_box.insert("1.0", self.translated_text)


    def updateClipboard(self):
        selected_text = pyperclip.paste()
        if self.v.get() == "translate":
            if selected_text != self.last_selected_text and isinstance(selected_text, str) and selected_text != "":
                self.translateText(selected_text)
                self.last_selected_text = selected_text
                self.last_option = self.current_option
                self.is_copy = False
                self.temp_text = ""
            elif self.current_option != self.last_option:
                if self.is_copy == False and isinstance(selected_text, str) and selected_text != "":
                    self.translateText(selected_text)
                    self.last_selected_text = selected_text
                    self.last_option = self.current_option
                elif self.is_copy == True and isinstance(self.temp_text, str) and self.temp_text != "":
                    self.translateText(self.temp_text)
                    self.last_option = self.current_option

        elif self.v.get() == "copy":
            if  isinstance(selected_text, str) and selected_text != "":
                self.text_box.delete("1.0", ttk.END)
                transform_text = self.transformSelectPdf(selected_text)
                pyperclip.copy(transform_text)
                self.last_selected_text = selected_text
        self.master.after(200, self.updateClipboard)

    def optionChanged(self, *args):
        self.current_option = self.options[self.selected_option.get()]

    def quit(self):
        self.master.quit()


if __name__ == "__main__":
    APIKey_dict = getAPIKey()
    if not APIKey_dict:
        tkinter.messagebox.askokcancel('提示', '未设置API')
    else:
        available_translate_tools = getAvailableTranslateTools(APIKey_dict)
        pyperclip.copy("")
        root = ttk.Window()
        root.resizable(False, False)
        translate_window = TranslateWindow(root,available_translate_tools,APIKey_dict)
        root.wm_attributes("-topmost", 1)
        root.protocol("WM_DELETE_WINDOW", translate_window.quit)
        root.mainloop()
