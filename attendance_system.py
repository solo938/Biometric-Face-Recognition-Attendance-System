import cv2
from core.recognition import recognize_faces, mark_attendance, face_app

cap = cv2.VideoCapture(0)
cv2.namedWindow("Biometric Attendance — Press Q to quit", cv2.WINDOW_NORMAL)
print("Attendance system running. Press Q to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Camera read failed."); break

    frame   = cv2.flip(frame, 1)
    results = recognize_faces(frame)

    for emp_id, name, similarity, box in results:
        msg, color = mark_attendance(emp_id)
        label = f"{name}  |  {msg}"

        
        cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), color, 2)
        
        cv2.rectangle(frame, (box[0], box[1] - 28), (box[2], box[1]), color, cv2.FILLED)
        cv2.putText(
            frame, label, (box[0] + 4, box[1] - 7),
            cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 1,
        )

    cv2.imshow("Biometric Attendance — Press Q to quit", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
print("Session ended.")
