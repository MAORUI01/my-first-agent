import os
import base64

# 智谱 AI 配置
os.environ["ZHIPUAI_API_KEY"] = os.getenv("ZHIPUAI_API_KEY", "your-zhipu-api-key")

from crewai import Agent, Task, Crew
from PIL import Image

# ============================================================
# 图片转 base64
# ============================================================
def encode_image(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode('utf-8')

# ============================================================
# 直接调用智谱 API（因为 CrewAI 默认不支持多模态）
# ============================================================
from zhipuai import ZhipuAI

client = ZhipuAI(api_key=os.environ["ZHIPUAI_API_KEY"])

def analyze_image(image_path, question):
    """分析图片并回答问题"""
    
    # 读取图片
    img_base64 = encode_image(image_path)
    
    # 调用智谱多模态 API
    response = client.chat.completions.create(
        model="glm-4v-plus",  # 多模态模型
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": question},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_base64}"}}
                ]
            }
        ],
        temperature=0.7,
    )
    
    return response.choices[0].message.content

# ============================================================
# 交互式测试
# ============================================================
if __name__ == "__main__":
    print("\n" + "="*50)
    print("🖼️ 多模态 Agent 已启动")
    print("="*50)
    print("我能看懂图片！")
    
    # 请把一张图片放到项目文件夹，命名为 test.jpg
    image_file = "test.jpg"
    
    # 检查图片是否存在
    if not os.path.exists(image_file):
        print(f"\n⚠️ 请先把图片放到 {image_file}")
        print("可以拖一张图片到项目文件夹，重命名为 test.jpg")
        exit(1)
    
    print(f"\n✅ 已加载图片：{image_file}")
    print(f"图片大小：{Image.open(image_file).size}\n")
    
    while True:
        q = input("你想问什么？（输入 quit 退出）\n你：")
        if q.lower() in ['quit', 'q']:
            print("再见！")
            break
        
        print("🤖 分析中...")
        answer = analyze_image(image_file, q)
        print(f"助手：{answer}\n")