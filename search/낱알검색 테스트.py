import cv2
import numpy as np
import statistics
import matplotlib.pyplot as plt
import colorsys
import webcolors

# Set color bounds
# orange_upper = np.array([10, 100, 20])
# orange_lower = np.array([25, 255, 255])
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

# Load the image and convert it to grayscale
img = cv2.imread('books.jpg')
rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
img2 = img.copy()

# Load image and convert to HSV color space
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply Gaussian blur to reduce noise and make edges smoother
gray_blur = cv2.GaussianBlur(gray, (5, 5), 0)

# perform edge detection
edges = cv2.Canny(gray_blur, 30, 100)

# Convert image to binary using Otsu's thresholding
_, thresh = cv2.threshold(gray_blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# Find contours in the binary image
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

avgArray = []
pillNum = 0
n_colors = 5

def show_color(roi):
    average = pill_roi.mean(axis=0).mean(axis=0)
    pixels = np.float32(pill_roi.reshape(-1, 3))

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
    flags = cv2.KMEANS_RANDOM_CENTERS

    _, labels, palette = cv2.kmeans(pixels, 5, None, criteria, 10, flags)
    _, counts = np.unique(labels, return_counts=True)

    print(palette)
    dominant = palette[np.argmax(counts)]
    # dominant2 = palette[counts.argsort()[-2]]
    hsv = colorsys.rgb_to_hsv(dominant[0]/255, dominant[1]/255, dominant[2]/255)
    hsv = [hsv[0] * 360, hsv[1] * 100, hsv[2] * 100]

    print(f"Average color: {average}")

    print(f"Dominant color: {dominant}")
    # print(f"Dominant color2: {dominant2}")
    print(f"Dominant color in hsv: {hsv}")

    print("show_color")

    for color, bounds in colors.items():
        if np.all(hsv >= bounds['lower_bound']) and np.all(hsv <= bounds['upper_bound']):
            return color
            break

    avg_patch = np.ones(shape=pill_roi.shape, dtype=np.uint8) * np.uint8(average)

    indices = np.argsort(counts)[::-1]
    freqs = np.cumsum(np.hstack([[0], counts[indices] / float(counts.sum())]))
    rows = np.int_(pill_roi.shape[0] * freqs)

    dom_patch = np.zeros(shape=pill_roi.shape, dtype=np.uint8)

    for i in range(len(rows) - 1):
        dom_patch[rows[i]:rows[i + 1], :, :] += np.uint8(palette[indices[i]])

    fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(12, 6))
    ax0.imshow(avg_patch)
    ax0.set_title('Average color')
    ax0.axis('off')
    ax1.imshow(dom_patch)
    ax1.set_title('Dominant colors')
    ax1.axis('off')
    fig.show()

pillList = []

# Loop over all contours and check if they are pill-shaped
for cnt in contours:

    # Approximate the contour as a polygon
    epsilon = 0.001
    approx = cv2.approxPolyDP(cnt, epsilon * cv2.arcLength(cnt, True), True)
    # approx = cv2.approxPolyDP(cnt, epsilon, True)

    # Calculate the positions and area of the polygon
    x, y, w, h = cv2.boundingRect(cnt)
    area = cv2.contourArea(cnt)
    ratio = abs(w - h) / w

    # Determine if the polygon is pill-shaped
    if len(approx) >= 5 and len(approx) <= 1000 and cv2.arcLength(cnt, True) < 5000 and area >= 10000:

        print(f"approx: {len(approx)}")
        pillNum += 1

        # Get pill region and find the average and dominant colors
        pill_roi = rgb_img[y:y + h, x:x + w]
        cv2.imshow(str(pillNum), img[y:y + h, x:x + w])
        pill_color = show_color(pill_roi)

        avgArray.append(len(approx))
        edges = statistics.median(avgArray)
        cv2.drawContours(img, [cnt], 0, (0, 255, 0), 2)
        print(f"ratio: {ratio}")
        # finding center point of shape
        # M = cv2.moments(cnt)
        # if M['m00'] != 0.0:
        #     center = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))

        pill_shape = ''
        if ratio > 0.1:
            pill_shape = '타원'
            # cv2.putText(img, 'ellipse', center,
            #             cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

        else:
            pill_shape = '원형'
            # cv2.putText(img, 'circle', center,
            #             cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        pillList.append({'color': pill_color, 'shape': pill_shape})

# print(f"Number of pills: {pillNum}")
# print(pillList)
result = {'number': pillNum, 'contents': pillList}
print(result)
# Display the output image
# img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)
cv2.imshow('output', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
