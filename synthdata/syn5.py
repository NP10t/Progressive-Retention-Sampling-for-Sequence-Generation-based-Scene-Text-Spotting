import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont
import random
import os

def create_curved_text(text, width, height, curve_amount=0.01):
    img = Image.new('RGBA', (width, height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(random.choice(["arial.ttf", "times.ttf"]), random.randint(60, 100))
    
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (width - text_width) / 2
    y = (height - text_height) / 2
    
    char_bboxes = []
    
    for i, char in enumerate(text):
        char_bbox = draw.textbbox((0, 0), char, font=font)
        char_width = char_bbox[2] - char_bbox[0]
        char_height = char_bbox[3] - char_bbox[1]
        
        y_offset = int(curve_amount * height * np.sin(2 * np.pi * i / len(text)))
        draw.text((x, y + y_offset), char, fill=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 255), font=font)
        
        char_bboxes.append((x, y + y_offset, x + char_width, y + y_offset + char_height))
        
        x += char_width
    
    # Tính toán bounding box bao quanh toàn bộ văn bản
    min_x = min(b[0] for b in char_bboxes)
    min_y = min(b[1] for b in char_bboxes)
    max_x = max(b[2] for b in char_bboxes)
    max_y = max(b[3] for b in char_bboxes)
    
    bounding_box = [(min_x, min_y), (max_x, min_y), (max_x, max_y), (min_x, max_y)]
    
    return img, bounding_box

def rotate_plane(img, angle_x, angle_y, angle_z):
    width, height = img.size
    scale_factor = 2
    img = img.resize((width * scale_factor, height * scale_factor), Image.LANCZOS)
    width, height = img.size
    
    Rx = np.array([[1, 0, 0],
               [0, np.cos(angle_x), -np.sin(angle_x)],
               [0, np.sin(angle_x), np.cos(angle_x)]])

    Ry = np.array([[np.cos(angle_y), 0, np.sin(angle_y)],
                [0, 1, 0],
                [-np.sin(angle_y), 0, np.cos(angle_y)]])

    Rz = np.array([[np.cos(angle_z), -np.sin(angle_z), 0],
                [np.sin(angle_z), np.cos(angle_z), 0],
                [0, 0, 1]])

    R = np.dot(Rz, np.dot(Ry, Rx))

    # Tạo lưới điểm 3D
    x, y = np.meshgrid(np.arange(width), np.arange(height))
    z = np.zeros_like(x)

    # Dịch chuyển tâm về gốc tọa độ
    x = x - width / 2
    y = y - height / 2

    # Áp dụng phép xoay
    xyz = np.dot(np.dstack([x, y, z]), R.T)

    # Chiếu về mặt phẳng 2D với khoảng cách từ camera
    d = width * random.uniform(0.5, 1.5) # Điều chỉnh khoảng cách này tùy theo yêu cầu
    x_proj = xyz[:, :, 0] / (xyz[:, :, 2] + d)
    y_proj = xyz[:, :, 1] / (xyz[:, :, 2] + d)

    # Dịch chuyển về vị trí ban đầu
    x_proj = x_proj * width / 2 + width / 2
    y_proj = y_proj * height / 2 + height / 2


    src = np.array([[0, 0], [width - 1, 0], [width - 1, height - 1], [0, height - 1]], dtype=np.float32)
    dst = np.array([
        [x_proj[0, 0], y_proj[0, 0]],
        [x_proj[0, -1], y_proj[0, -1]],
        [x_proj[-1, -1], y_proj[-1, -1]],
        [x_proj[-1, 0], y_proj[-1, 0]]
    ], dtype=np.float32)
    
    print(src, dst)
            
    M = cv2.getPerspectiveTransform(src, dst)
    result_img = cv2.warpPerspective(np.array(img), M, (width, height), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_TRANSPARENT)
    
    result_img = Image.fromarray(result_img)
    result_img = result_img.resize((width // scale_factor, height // scale_factor), Image.LANCZOS)
    
    return result_img

def create_synthetic_image(text, background_path, output_path):
    background = Image.open(background_path).convert("RGBA")
    width, height = background.size
    
    img = create_curved_text(text, width, height, curve_amount=0.01)

    d_x = np.pi / 3
    d_y = np.pi / 3
    d_z = np.pi / 12
    
    angle_x = random.uniform(-d_x, d_x)
    angle_y = random.uniform(-d_y, d_y)
    angle_z = random.uniform(-d_z, d_z)
    
    rotated_pil = rotate_plane(img, angle_x, angle_y, angle_z)
    
    out = Image.alpha_composite(background, rotated_pil)
    out.save(output_path)
    
    return output_path, text, polygon

def generate_dataset(num_images, background_folder, output_folder, words_file):
    with open(words_file, 'r', encoding='utf-8') as f:
        words = f.read().splitlines()
    
    backgrounds = [os.path.join(background_folder, f) for f in os.listdir(background_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    annotations = []
    
    for i in range(num_images):
        text = random.choice(words)
        background = random.choice(backgrounds)
        output_path = os.path.join(output_folder, f"image_{i}.png")
        
        output_path, text, polygon = create_synthetic_image(text, background, output_path)
        
        annotations.append(f"{','.join(map(str, poly.flatten()))}, {text}")
    
    with open(os.path.join(output_folder, "annotations.txt"), "w", encoding='utf-8') as f:
        f.write("\n".join(annotations))

# Sử dụng hàm
generate_dataset(1,
                "E:/ppnckh/background",
                "E:/ppnckh/output",
                "E:/ppnckh/words/text.txt"
                )