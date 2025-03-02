import easyocr
from PIL import Image
 
 
im = Image.open('photos\Screenshot_1.png')
im_crop = im.crop((830, 27, 1070, 55))
im_crop.save('photos\Cropped_1.png', quality=95)

# Create an OCR reader object
reader = easyocr.Reader(['en'])

# Read text from an image
result = reader.readtext('photos\Cropped_1.png')

# Print the extracted text
Win = []
Tie = []
Loose = []

if len(result)==3:
    Win.append(result[0][1])
    Tie.append(result[1][1])
    Loose.append(result[2][1])

print(Win)
print(Tie)
print(Loose)
