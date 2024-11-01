import cv2
import numpy as np

# Load cascade phân loại khuôn mặt
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Mở camera (sử dụng camera mặc định)
cap = cv2.VideoCapture(1)

while True:
    # Đọc hình ảnh từ camera
    ret, frame = cap.read()

    # Chuyển ảnh sang thang màu xám
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Phát hiện khuôn mặt
    faces = face_cascade.detectMultiScale(gray)

    # Vẽ hình chữ nhật quanh các khuôn mặt phát hiện được
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Hiển thị hình ảnh
    cv2.imshow('Detecting face', frame)

    # Nhấn phím 'q' để thoát
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Giải phóng camera và đóng các cửa sổ
cap.release()
cv2.destroyAllWindows()
