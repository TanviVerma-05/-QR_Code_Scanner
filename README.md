📸 QR Code Scanner (Image + Webcam) — Python GUI App
A simple yet powerful desktop QR Code Scanner built using Python, Tkinter, and OpenCV. This app allows users to scan QR codes from both image files and webcam, supports dark/light themes, and provides a friendly clipboard + URL prompt feature.

🚀 **Features**
🔍 Scan from Image Files (.jpg, .png, .bmp, etc.)

📷 Real-Time QR Detection via Webcam

🌗 Toggle Light / Dark Mode for better visibility

📋 Automatically Copies Scanned Data to Clipboard

🌐 Asks Before Opening URLs in your browser

🖥️ Resizable Output Dialog with scrollable result box

🧠 Built with OpenCV, PIL, and Tkinter

🖼️ **Screenshots**
![Screenshot 2025-06-04 200229](https://github.com/user-attachments/assets/cd8e95b8-96c2-44f9-984b-75a38f21dd7a)

![Screenshot 2025-06-04 200257](https://github.com/user-attachments/assets/fb123e74-7fcc-4bb7-a06d-9a5773c7103e)




🛠️ **Requirements**
1. Python 3.7+
2. OpenCV (opencv-python)
3. Pillow (PIL)
4. Tkinter (usually comes with Python)

**Install dependencies:**

bash
Copy code
```pip install opencv-python pillow```


If a URL is found, shows a Yes/No confirmation dialog before opening it.

Automatically displays and stores scanned content in a scrollable popup and copies it to clipboard.

Supports real-time webcam frame detection or file-based image analysis.
