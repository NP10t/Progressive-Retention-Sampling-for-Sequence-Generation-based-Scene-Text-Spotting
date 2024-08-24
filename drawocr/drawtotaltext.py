import cv2
import matplotlib.pyplot as plt

def visualize_and_save_scene_text(image_path, coordinates, transcripts, output_path):
    # Đọc ảnh
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Chuyển sang RGB để hiển thị đúng màu sắc

    # Vẽ từng tứ giác và transcript
    for quad, transcript in zip(coordinates, transcripts):
        # Chuyển đổi tọa độ thành định dạng integer
        quad = [(int(x), int(y)) for x, y in quad]

        # Vẽ tứ giác
        for i in range(4):
            start_point = quad[i]
            end_point = quad[(i + 1) % 4]
            cv2.line(image, start_point, end_point, color=(0, 255, 0), thickness=2)

        # Tính vị trí đặt text (trung điểm của cạnh đầu tiên)
        text_position = ((quad[0][0] + quad[1][0]) // 2, (quad[0][1] + quad[1][1]) // 2)
        
        # Vẽ transcript
        cv2.putText(image, transcript, text_position, cv2.FONT_HERSHEY_SIMPLEX, 
                    fontScale=0.5, color=(255, 0, 0), thickness=2, lineType=cv2.LINE_AA)

    # Lưu ảnh đã vẽ vào file
    cv2.imwrite(output_path, cv2.cvtColor(image, cv2.COLOR_RGB2BGR))  # Chuyển về BGR để lưu đúng màu sắc

    # Hiển thị ảnh
    plt.figure(figsize=(10, 10))
    plt.imshow(image)
    plt.axis('off')
    plt.show()

# Ví dụ sử dụng
output_path = 'a.jpg'
image_path = r"C:\Users\ASUS\Downloads\totaltext\Total-Text\Test\img98.jpg"
coordinates = [
    [(221, 98), (313, 89), (310, 108), (236, 113)],
    [(250, 165), (304, 179), (307, 188), (245, 180)],
    [(310, 177), (323, 164), (335, 170), (317, 191)]
]
transcripts = ['Text 1', 'Text 2', 'Text 3']

visualize_and_save_scene_text(image_path, coordinates, transcripts, output_path)
