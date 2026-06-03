import os
import base64
import cv2
from PIL import Image

os.environ["ZHIPUAI_API_KEY"] = "f02ec7a8462b4c1880dd10ae6a59cb20.2XZWHPVxAeMQV10J"

from zhipuai import ZhipuAI

client = ZhipuAI(api_key=os.environ["ZHIPUAI_API_KEY"])

# ============================================================
# 从视频中提取关键帧（每隔 N 秒取一帧）
# ============================================================
def extract_frames(video_path, interval_seconds=5):
    """
    从视频中提取关键帧
    video_path: 视频文件路径
    interval_seconds: 每隔多少秒取一帧
    """
    frames = []
    cap = cv2.VideoCapture(video_path)
    
    fps = cap.get(cv2.CAP_PROP_FPS)  # 帧率
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / fps
    
    print(f"📹 视频信息：")
    print(f"   - 时长：{duration:.1f} 秒")
    print(f"   - 帧率：{fps:.1f} fps")
    print(f"   - 总帧数：{total_frames}")
    
    frame_interval = int(fps * interval_seconds)
    frame_count = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        if frame_count % frame_interval == 0:
            # 转换为 PIL Image
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(frame_rgb)
            frames.append(pil_image)
            print(f"   - 提取第 {len(frames)} 帧（时间：{frame_count/fps:.1f}秒）")
        
        frame_count += 1
    
    cap.release()
    print(f"\n✅ 共提取 {len(frames)} 个关键帧\n")
    return frames

# ============================================================
# 图片转 base64
# ============================================================
def encode_image(image):
    import io
    buffer = io.BytesIO()
    image.save(buffer, format='JPEG')
    return base64.b64encode(buffer.getvalue()).decode('utf-8')

# ============================================================
# 分析单个图片
# ============================================================
def analyze_single_image(image, question):
    img_base64 = encode_image(image)
    
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
# 分析视频（多帧聚合）
# ============================================================
def analyze_video(video_path, question):
    """分析视频内容"""
    
    # 1. 提取关键帧
    frames = extract_frames(video_path, interval_seconds=5)
    
    if not frames:
        return "无法提取视频帧"
    
    # 2. 选择代表性帧（前、中、后）
    selected_frames = []
    if len(frames) >= 3:
        selected_frames.append(frames[0])           # 开头
        selected_frames.append(frames[len(frames)//2])  # 中间
        selected_frames.append(frames[-1])          # 结尾
    else:
        selected_frames = frames
    
    print(f"🎬 分析 {len(selected_frames)} 个关键帧...")
    
    # 3. 分析每一帧
    frame_analyses = []
    for i, frame in enumerate(selected_frames):
        print(f"   分析第 {i+1}/{len(selected_frames)} 帧...")
        analysis = analyze_single_image(frame, "描述这张图片的内容")
        frame_analyses.append(analysis)
    
    # 4. 汇总分析结果
    summary_prompt = f"""
用户问题：{question}

以下是视频中几个关键帧的描述：
{chr(10).join([f"【帧{i+1}】{analysis}" for i, analysis in enumerate(frame_analyses)])}

请根据以上信息，回答用户关于视频的问题。
回答要简洁、准确，综合多帧信息。
"""
    
    response = client.chat.completions.create(
        model="glm-4-plus",  # 用文本模型做总结
        messages=[{"role": "user", "content": summary_prompt}],
        temperature=0.7,
    )
    
    return response.choices[0].message.content

# ============================================================
# 主程序
# ============================================================
if __name__ == "__main__":
    print("\n" + "="*50)
    print("🎬 视频理解 Agent 已启动")
    print("="*50)
    print("我能分析视频内容！")
    
    video_file = "test_video.mp4"
    
    if not os.path.exists(video_file):
        print(f"\n⚠️ 请先把视频文件放到 {video_file}")
        print("支持格式：mp4, mov, avi")
        exit(1)
    
    while True:
        q = input(f"\n视频文件：{video_file}\n你想问什么？（输入 quit 退出）\n你：")
        if q.lower() in ['quit', 'q']:
            print("再见！")
            break
        
        print("\n🤖 分析中（可能需要几秒）...\n")
        answer = analyze_video(video_file, q)
        print(f"助手：{answer}\n")