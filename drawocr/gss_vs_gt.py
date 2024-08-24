from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import numpy as np
import cv2

dictionary = "aàáạảãâầấậẩẫăằắặẳẵAÀÁẠẢÃĂẰẮẶẲẴÂẦẤẬẨẪeèéẹẻẽêềếệểễEÈÉẸẺẼÊỀẾỆỂỄoòóọỏõôồốộổỗơờớợởỡOÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠiìíịỉĩIÌÍỊỈĨuùúụủũưừứựửữƯỪỨỰỬỮUÙÚỤỦŨyỳýỵỷỹYỲÝỴỶỸ"


def make_groups():
    groups = []
    i = 0
    while i < len(dictionary) - 5:
        group = [c for c in dictionary[i : i + 6]]
        i += 6
        groups.append(group)
    return groups


groups = make_groups()

TONES = ["", "ˋ", "ˊ", "⸱", "ˀ", "˜"]
SOURCES = ["ă", "â", "Ă", "Â", "ê", "Ê", "ô", "ơ", "Ô", "Ơ", "ư", "Ư", "Đ", "đ"]
TARGETS = ["aˇ", "aˆ", "Aˇ", "Aˆ", "eˆ", "Eˆ", "oˆ", "o˒", "Oˆ", "O˒", "u˒", "U˒", "D^", "d^"]


def parse_tone(word):
    res = ""
    tone = ""
    for char in word:
        if char in dictionary:
            for group in groups:
                if char in group:
                    if tone == "":
                        tone = TONES[group.index(char)]
                    res += group[0]
        else:
            res += char
    res += tone
    return res


def full_parse(word):
    word = parse_tone(word)
    res = ""
    for char in word:
        if char in SOURCES:
            res += TARGETS[SOURCES.index(char)]
        else:
            res += char
    return res


def correct_tone_position(word):
    word = word[:-1]
    first_ord_char = ""
    second_order_char = ""
    for char in word:
        for group in groups:
            if char in group:
                second_order_char = first_ord_char
                first_ord_char = group[0]
    if len(word) >= 1 and word[-1] == first_ord_char and second_order_char != "":
        pair_chars = ["qu", "Qu", "qU", "QU", "gi", "Gi", "gI", "GI"]
        for pair in pair_chars:
            if pair in word and second_order_char in ["u", "U", "i", "I"]:
                return first_ord_char
        return second_order_char
    return first_ord_char


def decoder(recognition):
    for char in TARGETS:
        recognition = recognition.replace(char, SOURCES[TARGETS.index(char)])
    replace_char = correct_tone_position(recognition)
    if recognition[-1] in TONES:
        tone = recognition[-1]
        recognition = recognition[:-1]
        for group in groups:
            if replace_char in group:
                recognition = recognition.replace(replace_char, group[TONES.index(tone)])
    return recognition

def enhance_image(img):
    enhancer = ImageEnhance.Sharpness(img)
    img = enhancer.enhance(2)  # Tăng cường độ nét
    return img

def resize_image(img, scale_factor):
    img_cv = np.array(img)
    img_resized = cv2.resize(img_cv, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_CUBIC)
    return Image.fromarray(img_resized)

def draw_ocr(img, coords, texts, detect_type="quad", draw_width=6, scale_factor=1):
    if img.mode != 'RGB':
        img = img.convert('RGB')

    img = enhance_image(img)
    img = resize_image(img, scale_factor)
    ocr_img = img.copy()
    draw = ImageDraw.Draw(ocr_img)
    
    img_width, img_height = img.size

    font_size = max(30, min(img_height, img_width) // 20000)  # Đảm bảo kích thước font tối thiểu là 10
    font = ImageFont.truetype("C:/Users/ASUS/Downloads/outputs/Arial.ttf", size=font_size)

    # Scale the coordinates
    coords = [[(int(x * scale_factor), int(y * scale_factor)) for x, y in coord] for coord in coords]

    for coord in coords:
        if detect_type in ["quad", "polygon"]:
            coord = np.array(coord)
            draw.polygon(
                coord.reshape(-1).astype(np.int64).tolist(),
                outline="red",
                width=draw_width,
            )
        elif detect_type in ["single"]:
            x, y = coord[0]
            draw.ellipse([x - 4, y - 4, x + 4, y + 4], fill="red", width=draw_width)
        else:  # ['box']
            c1, c2 = coord
            x1, y1 = c1
            x2, y2 = c2
            draw.rectangle([x1, y1, x2, y2], outline="red", width=draw_width)

    for coord, text in zip(coords, texts):
        bbox = font.getbbox(text)
        size = (bbox[2] - bbox[0], bbox[3] - bbox[1])

        pos = list(coord[0])
        pos[1] -= size[1]
        # Vẽ viền cho văn bản
        u = 1
        draw.text((pos[0] - u, pos[1] - u), text, font=font, fill="black")
        draw.text((pos[0] + u, pos[1] - u), text, font=font, fill="black")
        draw.text((pos[0] - u, pos[1] + u), text, font=font, fill="black")
        draw.text((pos[0] + u, pos[1] + u), text, font=font, fill="black")
        # Vẽ văn bản
        draw.text(pos, text, font=font, fill="white")
    
    # for coord, text in zip(coords, texts):
    #     bbox = font.getbbox(text)
    #     size = (bbox[2] - bbox[0], bbox[3] - bbox[1])

    #     pos = list(coord[0])
    #     pos[1] -= size[1]

    #     # Vẽ nền đen cho văn bản
    #     background = [(pos[0] - 2, pos[1] - 2), (pos[0] + size[0] + 2, pos[1] + size[1] + 2)]
    #     draw.rectangle(background, fill="black")

    #     # Vẽ viền cho văn bản
    #     draw.text((pos[0] - 1, pos[1] - 1), text, font=font, fill="black")
    #     draw.text((pos[0] + 1, pos[1] - 1), text, font=font, fill="black")
    #     draw.text((pos[0] - 1, pos[1] + 1), text, font=font, fill="black")
    #     draw.text((pos[0] + 1, pos[1] + 1), text, font=font, fill="black")

    #     draw.text(pos, text, font=font, fill="white")

    return ocr_img

# img = Image.open("E:/vietnamese/unseen_test_images/im1526.jpg")
# coords = [[(507,226), (542,226), (547,249), (513,248)]]
# texts = ['Tungf']
# scale_factor = 7 # Phóng to ảnh lên 2 lần
# ocr_img = draw_ocr(img, coords, texts, scale_factor=scale_factor)
# ocr_img.show()

def read_txt_file(file_path):
    coords = []
    texts = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split(',', 8+1)
            if len(parts) >= 10:
                x1, y1, x2, y2, x3, y3, x4, y4, confidence, text = parts
                # confidence = float(confidence[4:])
                confidence = float(confidence)
                text = decoder(text)
                # if(text[0:2] == 'Ha'):
                #     text = 'Hà,'
                if confidence > 0.65:
                    coords.append([(float(x1), float(y1)), (float(x2), float(y2)), (float(x3), float(y3)), (float(x4), float(y4))])
                    texts.append(text+" conf:"+str(round(confidence, 2)))
                    # texts.append(text)
    return coords, texts

id = '1713'

type = 6
folder = ''
if type == 1:
    folder = "res_output_final6000"
elif type == 2:
    folder = "res_output_VT15k"
elif type == 3:
    folder = "res_output_ke5ne4"
elif type == 4:
    file_path = "C:/Users/ASUS/Downloads/Hmean_UNITS/splv2/res_output/000"+id+".txt"
elif type == 5:
    folder = "res_output_EV5000"
elif type == 6:
    folder = "res_output_EV10kver2"

    
file_path = "C:/Users/ASUS/Downloads/outputs/"+folder+"/res_output/000"+id+".txt"

# Đọc thông tin từ file
coords, texts = read_txt_file(file_path)

# Mở ảnh gốc
img = Image.open("E:/vietnamese/unseen_test_images/im"+id+".jpg")

# Vẽ các text instances lên ảnh
scale_factor = 2  # Phóng to ảnh lên 7 lần
ocr_img = draw_ocr(img, coords, texts, scale_factor=scale_factor)
ocr_img.show()
ocr_img.save("annotated_image" + id + "_" + str(type) + ".jpg")
print("DONE")