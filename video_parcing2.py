import cv2
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract.exe"
from moviepy.editor import VideoFileClip
import easyocr
from PIL import Image




#ввод
clip_name = "SDR_14.03.25_test"
date = clip_name.split('_')[1]
author = clip_name.split('_')[0]
stream_hour = clip_name.split('_')[2]

lang = "en"
reader = easyocr.Reader([lang])

timer_cords = (1500, 480, 1536, 511)
turn_cords = (1594, 14, 1670, 35)
#turn GDM (1602, 16, 1663, 38)
#turn SDR (1602, 16, 1663, 38)
uptable_cords = (830, 27, 1070, 55)

# # Подпись файла
# DataFile = open(f'ExtractedData\{clip_name}_DataOutput.txt','a')
# DataFile.write(clip_name+'\n')
# DataFile.close()

# Открытие видеофайла
video_clip = VideoFileClip(f"videos/{clip_name}.mp4")
video_length = int(round(video_clip.duration))

# Выбор кадров
default_step = 9
big_step = 40
step = default_step
current_frame = 0
DoGetRes = False

# Loop # 
###########################################################################################################

while current_frame + step < video_length:

    video_clip.save_frame(f'photos/{clip_name}_Frame_{current_frame}.jpg', t = current_frame)

    # Обрезка верхней таблицы
    im = Image.open(f'photos/{clip_name}_Frame_{current_frame}.jpg')
    im_crop = im.crop(uptable_cords)
    im_crop.save(f'photos/{clip_name}_UpTable_{current_frame}.jpg')


    # Чтение теста с фото
    result = reader.readtext(f'photos/{clip_name}_UpTable_{current_frame}.jpg')


    # Сохранение результатов в массивы
    if len(result)==3:

        # Обрезка хода
        im = Image.open(f'photos/{clip_name}_Frame_{current_frame}.jpg')
        im_crop = im.crop(turn_cords)
        im_crop.save(f'photos/{clip_name}_Turn_{current_frame}.jpg')

        img = cv2.imread(f'photos/{clip_name}_Turn_{current_frame}.jpg')
        img = cv2.resize(img, None, fx=9, fy=9)  # Увеличение изображения в 9 раз
        turn = str(pytesseract.image_to_string(img))
        
        DoTurnFound = False
        print(turn)
        if len(turn)==0:
            turn = -1
        else:
            lt = len(turn)
            turn = str(turn)
            turn += ' '
            for i in range(lt):
                if str(turn[i]).isdigit():
                    if str(turn[i+1]).isdigit():
                        turn=int(turn[i:i+2])
                        DoTurnFound = True
                        break
                    else:
                        turn=int(turn[i])
                        DoTurnFound = True
                        break
        if not DoTurnFound or turn > 19:
            turn = -1

        
        # Экспорт в файл
        DataFile = open(f'ExtractedData\{clip_name}_DataOutput.txt','a')
        DataFile.write(' '.join([str(turn), result[0][1].strip('%'), result[1][1].strip('%'), result[2][1].strip('%'), date, stream_hour, author])+'\n')
        DataFile.close()
        
        # turn win tie loose
        print("found results: ", ' '.join([str(turn), result[0][1].strip('%'), result[1][1].strip('%'), result[2][1].strip('%')]))
        DoGetRes = True
        step = big_step
        
    # Обрезка таймера
    im = Image.open(f'photos/{clip_name}_Frame_{current_frame}.jpg')
    im_crop = im.crop((1500, 480, 1540, 517))
    im_crop.save(f'photos/{clip_name}_Timer_{current_frame}.jpg')

    time_till_battle = reader.readtext(f'photos/{clip_name}_Timer_{current_frame}.jpg')
    if len(time_till_battle)==0:
        time_till_battle = [['','?']]

    print("progress: ",f"{current_frame}/{video_length}   {round(current_frame/video_length*100, 1)}%")



    # Смена кадра
    try:
        step = int(time_till_battle[0][1]) + 9
    except:
        step = default_step

    if DoGetRes:
        step = big_step
        DoGetRes = False
    current_frame += step

        
print('Done!')
        


