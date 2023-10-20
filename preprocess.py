import cv2
import numpy as np

image_path = "preprocess_image.png"


def preprocess(image_path):
    img = cv2.imread(image_path)
    img = cv2.resize(img, (1280,720)) # kullandığım örnek resim çok büyük olduğu için kullandım. gerçek görüntüye göre değiştirin
    
    img = line_manual(img)  # çizgiler için line fonkisyonunu çağır
    img = draw_black(img)   # siyaha boyamak için draw fonksiyonunu çağır

    top, bottom = split_image(img)  # resmi bölmek için split fonksiyonunu çağır
    
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # RGB formata dönüştürür
    top= cv2.resize(top, (224, 224))  # yeniden boyutlandır 224,224
    
    bottom = cv2.resize(bottom, (224, 224))  # yeniden boyutlandır 224,224
    img = img / 255.0  
    #cv2.imshow(winname="Top Half", mat=top)
    #cv2.imshow(winname="Bottom Half", mat=bottom)
    return top, bottom
    
def line_manual(img):
    pts_red = np.array([[600,0], [727,0], [45,720], [1190,720]], np.int32) #sol üst, sağ üst, sol alt, sağ alt

    #red 
    cv2.line(img=img, pt1=pts_red[0], pt2=pts_red[2], color=(255, 0, 0), thickness=2)
    cv2.line(img=img, pt1=pts_red[1], pt2=pts_red[3], color=(255, 0, 0), thickness=2)

    return img

def draw_black(img):
    draw_black = np.array([[727,0], [600,0], [45,720], [1190,720]], np.int32)

    # Çokgeni siyahla doldurmak için bir maske oluşturun
    mask = np.zeros_like(img)
    result = cv2.fillPoly(mask, [draw_black], (255, 255, 255))

    # Maskenin tersini alarak çokgen dışındaki bölgeyi siyahla boyayın
    result = cv2.bitwise_and(img, mask)

    return result


def split_image(img):
    # resmi ortadan böl yatay olarak
    height, width, _ = img.shape
    middle_y = height // 2

    # Resmi dikey olarak ikiye bölmek için iki bölgeyi tanımlayın
    top_half = img[:middle_y, :, :]
    bottom_half = img[middle_y:, :, :]

    top_half_cropped = top_half[:, 340:width - 340, :]  # üstteki resmin sağından ve solundan (340px) kırp

    return top_half_cropped, bottom_half


top,bottom = preprocess(image_path)

img = cv2.imread(filename=image_path)       # resmin orijinal halini göstermek için
cv2.imshow(winname="orijinal_resim",mat=img)

cv2.imshow(winname="Top", mat=top)
cv2.imshow(winname="Bottom", mat=bottom)
cv2.waitKey(0)
cv2.destroyAllWindows()
