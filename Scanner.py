import cv2
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import webbrowser

root = tk.Tk()
root.title("QR Code Scanner (Image + Webcam)")
root.geometry("700x600")

is_dark_theme = False

def toggle_theme():
    global is_dark_theme, bg_color, fg_color
    is_dark_theme = not is_dark_theme
    bg_color = "#2e2e2e" if is_dark_theme else "white"
    fg_color = "white" if is_dark_theme else "black" 
    root.config(bg=bg_color)
    btn_image.config(bg=bg_color, fg=fg_color)
    btn_webcam.config(bg=bg_color, fg=fg_color)
    toggle_btn.config(bg=bg_color, fg=fg_color)
    image_label.config(bg=bg_color)
    status_label.config(bg=bg_color, fg=fg_color)

def show_qr_result(data):
    copy_to_clipboard(data)

    # Check if it's a URL and ask user immediately
    if data.startswith("http://") or data.startswith("https://"):
        response = messagebox.askyesno("Open URL", f"The QR code contains a link:\n\n{data}\n\nDo you want to open it?")
        if response:
            webbrowser.open(data)

    # Create a custom window regardless of data type
    dialog = tk.Toplevel(root)
    dialog.title("QR Code Detected - Copied to Clipboard")
    dialog.geometry("500x300")
    dialog.resizable(True, True)

    # Info label
    tk.Label(dialog, text="Scanned QR Data:", font=("Arial", 12, "bold")).pack(pady=5)

    # Text area with scroll
    frame = tk.Frame(dialog)
    frame.pack(fill="both", expand=True, padx=10, pady=5)

    scrollbar = tk.Scrollbar(frame)
    scrollbar.pack(side="right", fill="y")

    text_area = tk.Text(frame, wrap="word", yscrollcommand=scrollbar.set)
    text_area.insert("1.0", data)
    text_area.config(state="disabled")
    text_area.pack(side="left", fill="both", expand=True)

    scrollbar.config(command=text_area.yview)

    # Close button
    tk.Button(dialog, text="OK", command=dialog.destroy).pack(pady=5)





def copy_to_clipboard(data):
    root.clipboard_clear()
    root.clipboard_append(data)

def handle_qr_data(data):
    show_qr_result(data)
    

def scan_qr_from_image():
    file_path = filedialog.askopenfilename(
        title="Select an Image",
        filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif")]
    )
    if not file_path:
        return

    image = cv2.imread(file_path)
    if image is None:
        messagebox.showerror("Error", "Failed to load image.")
        return

    detector = cv2.QRCodeDetector()
    data, bbox, _ = detector.detectAndDecode(image)

    if bbox is not None and data:
        for i in range(len(bbox[0])):
            pt1 = tuple(map(int, bbox[0][i]))
            pt2 = tuple(map(int, bbox[0][(i + 1) % len(bbox[0])]))
            cv2.line(image, pt1, pt2, (0, 255, 0), 2)

        handle_qr_data(data)

        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(image_rgb)
        img_tk = ImageTk.PhotoImage(img_pil)

        image_label.config(image=img_tk)
        image_label.image = img_tk
        status_label.config(text="Scanned from Image")

    else:
        messagebox.showwarning("No QR Code", "No QR code found in the image.")
        status_label.config(text="No QR found")

# Webcam scanning variables
cap = None
detector = cv2.QRCodeDetector()
webcam_running = False

def start_webcam():
    global cap, webcam_running
    if webcam_running:
        stop_webcam()
        return

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        messagebox.showerror("Error", "Cannot open webcam")
        return

    webcam_running = True
    btn_webcam.config(text="Stop Webcam")
    status_label.config(text="Scanning from Webcam...")
    scan_webcam_frame()

def stop_webcam():
    global cap, webcam_running
    webcam_running = False
    btn_webcam.config(text="Start Webcam")
    status_label.config(text="Webcam stopped")
    if cap:
        cap.release()
    image_label.config(image='')

def scan_webcam_frame():
    global cap, webcam_running
    if not webcam_running:
        return

    ret, frame = cap.read()
    if not ret:
        messagebox.showerror("Error", "Failed to grab frame")
        stop_webcam()
        return

    data, bbox, _ = detector.detectAndDecode(frame)
    if bbox is not None and data:
        for i in range(len(bbox[0])):
            pt1 = tuple(map(int, bbox[0][i]))
            pt2 = tuple(map(int, bbox[0][(i + 1) % len(bbox[0])]))
            cv2.line(frame, pt1, pt2, (0, 255, 0), 2)

        handle_qr_data(data)
        stop_webcam()
        return

    # Show frame in tkinter
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(frame_rgb)
    img_tk = ImageTk.PhotoImage(img_pil)

    image_label.config(image=img_tk)
    image_label.image = img_tk

    # Repeat after 30 ms
    root.after(30, scan_webcam_frame)


def on_scan_image_click():
    # Change button color to indicate it's active
    btn_image.config(bg="#4CAF50", fg="white")  # Green background
    root.after(150, lambda: btn_image.config(bg=bg_color, fg=fg_color))  # Revert after 150 ms
    scan_qr_from_image()


def on_webcam_click():
    btn_webcam.config(bg="#2196F3", fg="white")  # Blue background
    root.after(100, lambda: btn_webcam.config(bg=bg_color, fg=fg_color))  # Reset after 100ms
    root.after(120, start_webcam)




# Widgets
btn_image = tk.Button(root, text="Scan QR from Image", command=on_scan_image_click, font=("Arial", 25))
btn_image.pack(pady=10)

btn_webcam = tk.Button(root, text="Start Webcam", command=on_webcam_click, font=("Arial", 25))
btn_webcam.pack(pady=10)

toggle_btn = tk.Button(root, text="Toggle Theme", command=toggle_theme, font=("Arial", 25))
toggle_btn.pack(pady=10)

image_label = tk.Label(root)
image_label.pack(pady=10)

status_label = tk.Label(root, text="", font=("Arial", 12))
status_label.pack()

toggle_theme()  # Start with dark theme

root.mainloop()


















