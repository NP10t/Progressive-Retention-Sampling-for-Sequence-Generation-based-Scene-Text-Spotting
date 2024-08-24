from PIL import Image, ImageDraw

def crop_by_coords(img, coords):
    """
    Cắt phần hình chữ nhật từ ảnh dựa trên tọa độ của 4 điểm.
    
    Args:
    - img: Ảnh đầu vào (PIL.Image)
    - coords: Tọa độ của 4 điểm [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]

    Returns:
    - Ảnh đã được cắt (PIL.Image)
    """
    # Tính toán bounding box từ tọa độ của 4 điểm
    x_coords = [coord[0] for coord in coords]
    y_coords = [coord[1] for coord in coords]

    left = min(x_coords)
    top = min(y_coords)
    right = max(x_coords)
    bottom = max(y_coords)

    return img.crop((left, top, right, bottom))

# Đường dẫn tới tấm ảnh
id = 1

img_path = "E:/ppnckh/annotated_image1713_" + str(id) + ".jpg"

# Mở ảnh
img = Image.open(img_path)

# Tọa độ của 4 điểm
x = 100

a = 2000
b = 1910 + 50
c = 4900
d = 4000 + x
coords = [(a, b), (c, b), (c, d), (a, d)]  # Thay đổi tọa độ tùy ý

# Cắt phần hình chữ nhật dựa trên tọa độ của 4 điểm
cropped_img = crop_by_coords(img, coords)

# Vẽ các hình chữ nhật lên ảnh đã cắt
draw = ImageDraw.Draw(cropped_img)

green_rect_coords = [(100, 900), (2200, 1500)]
orange_rect_coords = [(500, 350), (1150, 660)]
gray_rect_coords = [(100, 1520), (2200, 2100)]

draw.rectangle(green_rect_coords, outline="lime", width=5)
draw.rectangle(orange_rect_coords, outline="orange", width=5)
draw.rectangle(gray_rect_coords, outline="lightblue", width=5)

# Hiển thị ảnh đã cắt
cropped_img.show()

# Lưu ảnh đã cắt và vẽ
cropped_img.save("E:/ppnckh/zcropped_image_2nd_" + str(id) + ".jpg")
