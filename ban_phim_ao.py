import cv2
import time
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(1)
cap.set(3, 1200)
cap.set(4, 720)
detector = HandDetector(detectionCon=0.8)
# Danh sách các phím
keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"]]
# Lớp Button để tạo nút
class Button():
    def __init__(self, pos, text, size=(85, 85)):
        self.pos = pos
        self.size = size
        self.text = text
    def draw(self, img):
        x, y = self.pos
        w, h = self.size
        cv2.rectangle(img, self.pos, (x + w, y + h), (255, 0, 0), cv2.FILLED)
        cv2.putText(img, self.text, (x + 25, y + 60),
                    cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 4)
        return img
def drawALL(img, buttonList):
    for button in buttonList:
        img = button.draw(img)
    return img
buttonList = []
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttonList.append(Button([100 * j + 50, 100 * i + 50], key))
while True:
    success, img = cap.read()
    if not success:
        print("Không thể đọc từ camera.")
        break
    # Phát hiện tay và lấy các thông tin bàn tay
    hands, img = detector.findHands(img)
    # Vẽ toàn bộ các nút
    img = drawALL(img, buttonList)
    if hands:
        hand = hands[0]
        lmList = hand['lmList']
        for button in buttonList:
            x, y = button.pos
            w, h = button.size
            if x < lmList[8][0] < x + w and y < lmList[8][1] < y + h:
                # Đổi màu nút khi chạm vào
                cv2.rectangle(img, button.pos, (x + w, y + h), (255, 0, 255), cv2.FILLED)
                cv2.putText(img, button.text, (x + 25, y + 60),
                            cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 4)

                try:
                    length, _, _ = detector.findDistance(lmList[8], lmList[12], img)
                    if length < 30:
                        print(f"Đã nhấn: {button.text}")
                        cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                        cv2.putText(img, button.text, (x + 25, y + 60),
                                    cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 4)
                        time.sleep(0.3)

                except Exception as e:
                    print(f"Lỗi khi tính khoảng cách hoặc xử lý nút: {e}")
    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()

