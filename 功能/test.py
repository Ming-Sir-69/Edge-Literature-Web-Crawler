import openai

# 设置你的OpenAI API Key
api_key = 'your openai API KEY'
openai.api_key = api_key

def translate_text(input_text, source_language="zh", target_language="en"):
    # 翻译成目标语言
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Translate this text from {source_language} to {target_language}: {input_text}",
        max_tokens=100
    )
    translated_text = response.choices[0].text.strip()
    
    return translated_text

def main():
    print("欢迎使用OpenAI翻译程序！输入文本进行翻译，输入'退出'以结束程序。")
    
    while True:
        input_text = input("\n请输入要翻译的文本：")
        if input_text.lower() == "退出":
            print("程序已退出。")
            break
        
        translated_text = translate_text(input_text, source_language="zh", target_language="en")
        print(f"翻译结果（中文 -> 英文）：{translated_text}")
        
        # 反向翻译（英文 -> 中文）
        translated_text_reverse = translate_text(translated_text, source_language="en", target_language="zh")
        print(f"反向翻译结果（英文 -> 中文）：{translated_text_reverse}")

if __name__ == "__main__":
    main()
