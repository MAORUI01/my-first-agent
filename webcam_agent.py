import os
import base64
import cv2
import time
from PIL import Image
import threading
from collections import deque

os.environ["ZHIPUAI_API_KEY"] = os.getenv("ZHIPUAI_API_KEY", "your-zhipu-api-key")

from zhipuai import ZhipuAI

client = ZhipuAI(api_key=os.environ["ZHIPUAI_API_KEY"])

# ============================================================
# 图片转 base64
# ============================================================
def encode_image(image):
    _, buffer = cv2.imencode('.jpg', image)
    return base64.b64encode(buffer).decode('utf-8')

# ============================================================
# 分析单帧画面
# ============================================================
def analyze_frame(frame, question):
    """分析当前摄像头画面"""
    img_base64 = encode_image(frame)
    
    response = client.chat.completions.create(
        model="glm-4v-plus",
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
# 实时摄像头分析
# ============================================================
class WebcamAgent:
    def __init__(self):
        self.cap = None
        self.is_running = False
        self.fps = 1  # 每秒分析1帧（避免API调用太频繁）
        self.last_analysis = ""
        
    def start(self):
        """启动摄像头"""
        self.cap = cv2.VideoCapture(0)  # 0 表示默认摄像头
        
        if not self.cap.isOpened():
            print("❌ 无法打开摄像头")
            return False
        
        print("✅ 摄像头已启动")
        print(f"📹 分辨率：{int(self.cap.get(3))} x {int(self.cap.get(4))}")
        return True
    
    def run(self):
        """运行实时分析"""
        if not self.start():
            return
        
        self.is_running = True
        frame_count = 0
        last_analysis_time = 0
        analysis_interval = 3  # 每3秒分析一次（可调整）
        
        print("\n" + "="*50)
        print("🎬 实时视频流 Agent 已启动")
        print("="*50)
        print("按 'q' 退出")
        print("按 'a' 分析当前画面")
        print("按 'c' 连续分析模式（每3秒）")
        print("="*50 + "\n")
        
        # 用于异步分析的线程
        analysis_requested = False
        current_question = ""
        analysis_result = ""
        
        while self.is_running:
            ret, frame = self.cap.read()
            if not ret:
                print("❌ 无法获取画面")
                break
            
            # 显示画面
            display_frame = frame.copy()
            current_time = time.time()
            
            # 检查按键
            key = cv2.waitKey(1) & 0xFF
            
            # 退出
            if key == ord('q'):
                break
            
            # 单次分析
            elif key == ord('a'):
                analysis_requested = True
                current_question = "描述这张图片的内容"
                display_frame = cv2.putText(display_frame, "Analyzing...", (10, 30), 
                                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            # 开启/关闭连续分析
            elif key == ord('c'):
                analysis_interval = 3 if analysis_interval == 0 else 0
                status = "ON" if analysis_interval > 0 else "OFF"
                print(f"📊 连续分析模式：{status}")
            
            # 处理异步分析
            if analysis_requested:
                analysis_requested = False
                print("🤖 分析中...")
                try:
                    result = analyze_frame(frame, current_question)
                    analysis_result = result
                    print(f"📝 分析结果：{result}\n")
                except Exception as e:
                    print(f"❌ 分析失败：{e}")
            
            # 连续分析模式
            if analysis_interval > 0 and current_time - last_analysis_time > analysis_interval:
                last_analysis_time = current_time
                print("🤖 连续分析中...")
                try:
                    result = analyze_frame(frame, "简要描述当前画面")
                    if result != self.last_analysis:
                        self.last_analysis = result
                        print(f"📝 {result}\n")
                except Exception as e:
                    print(f"❌ 分析失败：{e}")
            
            # 显示分析结果
            if analysis_result:
                # 在画面上显示结果（截取前50字符）
                short_result = analysis_result[:50] + "..." if len(analysis_result) > 50 else analysis_result
                for i, line in enumerate(short_result.split('\n')[:3]):
                    cv2.putText(display_frame, line, (10, 60 + i*30), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            
            # 显示模式提示
            mode_text = "Continuous Mode: ON" if analysis_interval > 0 else "Continuous Mode: OFF"
            cv2.putText(display_frame, mode_text, (10, display_frame.shape[0] - 10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            cv2.putText(display_frame, "Press 'a' to analyze, 'c' for continuous, 'q' to quit", 
                       (10, display_frame.shape[0] - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
            # 显示画面
            cv2.imshow('Webcam Agent', display_frame)
        
        # 清理
        self.cap.release()
        cv2.destroyAllWindows()
        print("👋 程序已退出")

# ============================================================
# 主程序
# ============================================================
if __name__ == "__main__":
    agent = WebcamAgent()
    
    print("\n⚠️ 请确保摄像头已连接并授权")
    input("按 Enter 键开始...")
    
    agent.run()