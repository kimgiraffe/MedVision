import cv2
import numpy as np
import colorsys

from users.models import User, Prescription, PrescDetail, DrugInfo, PillData

# Set color bounds
colors = {
    '빨강': {
        'lower_bound': np.array([0, 50, 50]),
        'upper_bound': np.array([30, 100, 100])
    },
    '노랑': {
        'lower_bound': np.array([45, 50, 50]),
        'upper_bound': np.array([75, 100, 100])
    },
    '주황': {
        'lower_bound': np.array([30, 50, 50]),
        'upper_bound': np.array([45, 100, 100])
    },
    '파랑': {
        'lower_bound': np.array([210, 50, 50]),
        'upper_bound': np.array([270, 100, 100])
    },
    '초록': {
        'lower_bound': np.array([70, 30, 50]),
        'upper_bound': np.array([150, 100, 100])
    },
    '보라': {
        'lower_bound': np.array([270, 50, 50]),
        'upper_bound': np.array([330, 100, 100])
    },
    '하양': {
        'lower_bound': np.array([0, 0, 80]),
        'upper_bound': np.array([360, 20, 100])
    },
    '갈색': {
        'lower_bound': np.array([0, 20, 20]),
        'upper_bound': np.array([30, 60, 40])
    }
}

def show_color(pill_roi):
    average = pill_roi.mean(axis=0).mean(axis=0)
    pixels = np.float32(pill_roi.reshape(-1, 3))

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
    flags = cv2.KMEANS_RANDOM_CENTERS

    _, labels, palette = cv2.kmeans(pixels, 5, None, criteria, 10, flags)
    _, counts = np.unique(labels, return_counts=True)

    print(palette)
    dominant = palette[np.argmax(counts)]
    hsv = colorsys.rgb_to_hsv(dominant[0]/255, dominant[1]/255, dominant[2]/255)
    hsv = [hsv[0] * 360, hsv[1] * 100, hsv[2] * 100]

    print(f"Average color: {average}")
    print(f"Dominant color: {dominant}")
    print(f"Dominant color in hsv: {hsv}")

    for color, bounds in colors.items():
        if np.all(hsv >= bounds['lower_bound']) and np.all(hsv <= bounds['upper_bound']):
            return color
            break

def process_image(img_name):
    img_gray = cv2.cvtColor(img_name, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(img_gray, 190, 255, cv2.THRESH_BINARY_INV)
    img_blur = cv2.GaussianBlur(thresh, (3, 3), 1)
    img_canny = cv2.Canny(img_blur, 0, 0)
    kernel = np.ones((5, 5))
    img_dilate = cv2.dilate(img_canny, kernel, iterations=1)
    return cv2.erode(img_dilate, kernel, iterations=1)

def pill_scan(img_name):
    # Load the image and convert it to grayscale
    img = cv2.imread(img_name)
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # img2 = img.copy()
    #
    # # Load image and convert to HSV color space
    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #
    # # Apply Gaussian blur to reduce noise and make edges smoother
    # gray_blur = cv2.GaussianBlur(gray, (5, 5), 0)
    #
    # # perform edge detection
    # edges = cv2.Canny(gray_blur, 30, 100)
    #
    # # Convert image to binary using Otsu's thresholding
    # _, thresh = cv2.threshold(gray_blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    #
    # # Find contours in the binary image
    # contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    contours, hierarchies = cv2.findContours(process_image(img), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cnt = max(contours, key=cv2.contourArea)

    avgArray = []
    pillNum = 0

    pillList = []
    # Loop over all contours and check if they are pill-shaped
    for cnt in contours:

        # Approximate the contour as a polygon
        epsilon = 0.01
        # approx = cv2.approxPolyDP(cnt, epsilon * cv2.arcLength(cnt, True), True)
        approx = cv2.approxPolyDP(cnt, epsilon * cv2.arcLength(cnt, True), True)

        # Calculate the positions and area of the polygon
        x, y, w, h = cv2.boundingRect(cnt)
        area = cv2.contourArea(cnt)
        ratio = abs(w - h) / w

        # Determine if the polygon is pill-shaped
        if len(approx) >= 5 and len(approx) <= 1000 and cv2.arcLength(cnt, True) < 5000 and area >= 10000:
            pillNum += 1

            # Get pill region and find the average and dominant colors
            pill_roi = rgb_img[y:y + h, x:x + w]
            pill_color = show_color(pill_roi)

            avgArray.append(len(approx))

            pill_shape = ''
            if ratio > 0.1:
                pill_shape = '타원형'

            else:
                pill_shape = '원형'
            pillList.append({'color': pill_color, 'shape': pill_shape})

    result = {'number': pillNum, 'contents': pillList}
    print(result)
    return result

def get_data(itemList):
    dataList = []
    for i in itemList:
        drug = i.drugInfo
        dosage = i.dosagePerOnce
        drugNo = drug.drugNo
        # try:
        #     PillData.objects.get(drugNo=drugNo)
        # except PillData.DoesNotExist:
        #     continue

        data = PillData.objects.filter(drugNo=drugNo).first()
        if data is not None:
            for i in range(dosage):
                dataList.append({'color': data.pillColor, 'shape': data.pillShape})
        else: continue

    return dataList

def check_pill(result, dataList):
    if(result['pillNum'] == len(dataList)):
        return dataList.containsAll(result['contents'])
    else:
        return False

def find_prescription(result, user):
    pillNum = result['number']
    user = User.objects.get(userId=user)
    for p in Prescription.objects.get(user=user):
        itemList = PrescDetail.objects.filter(prescription=p)
        if len(itemList) >= pillNum:
            dataList = get_data(itemList)
            if check_pill(result, dataList) == True:
                print(itemList)

# pill_scan('books.jpg')