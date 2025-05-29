import os
from PIL import Image

def optimize_and_convert():
    current_dir = os.getcwd()
    
    # 配置参数
    MAX_WIDTH = 1920      # 最大宽度（按需调整）
    MAX_HEIGHT = 1080     # 最大高度（按需调整）
    QUALITY = 80          # 质量百分比（0-100）
    RESAMPLE = Image.LANCZOS  # 高质量缩放算法
    
    # 创建输出文件夹（如果不存在）
    output_folder = os.path.join(current_dir, "webp_output")
    os.makedirs(output_folder, exist_ok=True)
    
    # 获取图片文件
    image_files = [f for f in os.listdir(current_dir) 
                  if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    image_files.sort()
    
    counter = 1
    for img_file in image_files:
        try:
            with Image.open(os.path.join(current_dir, img_file)) as img:
                # 计算新尺寸（保持宽高比）
                width, height = img.size
                if width > MAX_WIDTH or height > MAX_HEIGHT:
                    ratio = min(MAX_WIDTH/width, MAX_HEIGHT/height)
                    new_size = (int(width*ratio), int(height*ratio))
                    img = img.resize(new_size, RESAMPLE)
                
                # 转换为RGB模式（避免Alpha通道影响）
                if img.mode in ('RGBA', 'P'):
                    img = img.convert('RGB')
                
                # 保存为WebP（带优化参数）
                output_path = os.path.join(output_folder, f"{counter}.webp")
                img.save(output_path, 'webp', 
                        quality=QUALITY,
                        method=6,  # 压缩方法（0-6，越大压缩越强）
                        optimize=True)
                
                # 显示压缩效果
                orig_size = os.path.getsize(os.path.join(current_dir, img_file)) / 1024
                new_size = os.path.getsize(output_path) / 1024
                print(f"{img_file} ({orig_size:.1f}KB) -> webp_output/{counter}.webp ({new_size:.1f}KB)")
                counter += 1
                
        except Exception as e:
            print(f"处理 {img_file} 失败: {str(e)}")

if __name__ == "__main__":
    optimize_and_convert()