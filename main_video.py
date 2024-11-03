import cv2
import os
from simple_facerec import SimpleFacerec
from tkinter import Tk, Button, Label, Entry, filedialog, messagebox, Toplevel, Canvas
from PIL import Image, ImageTk

# Encode faces from a folder
sfr = SimpleFacerec()
sfr.load_encoding_images("images/")

cap = None

def start_recognition():
    global cap
    cap = cv2.VideoCapture(0)
    recognizing()

def add_image():
    global cap
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    if ret:
        # Show popup form for entered name
        popup = Toplevel(root)
        popup.title("Enter Name")
        
        Label(popup, text="Name:").grid(row=0, column=0, padx=10, pady=10)
        name_entry = Entry(popup)
        name_entry.grid(row=0, column=1, padx=10, pady=10)
        
        def save_image():
            name = name_entry.get().strip()
            if name:
                # Save image to local folder (images)
                image_name = f"{name}.jpg"
                save_path = os.path.join("images", image_name)
                cv2.imwrite(save_path, frame)
                sfr.load_encoding_images("images/")
                messagebox.showinfo("Success", f"Image '{image_name}' added and model updated.")
                popup.destroy()
            else:
                messagebox.showerror("Error", "Please enter a name.")

        Button(popup, text="Save", command=save_image).grid(row=1, column=0, columnspan=2, pady=10)

def recognizing():
    global cap
    if cap is not None and cap.isOpened():
        ret, frame = cap.read()
        if ret:
            # Detect faces
            face_locations, face_names = sfr.detect_known_faces(frame)
            for face_loc, name in zip(face_locations, face_names):
                y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]
                cv2.putText(frame, name, (x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 200), 4)
            
            # Convert the frame to an ImageTk format for tkinter
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(rgb_frame)
            imgtk = ImageTk.PhotoImage(image=img)
            display_canvas.create_image(0, 0, anchor="nw", image=imgtk)
            display_canvas.image = imgtk

        # Repeat this function every 10 ms
        root.after(10, recognizing)

# GUI setup
root = Tk()
root.title("Kehadiran Mahasiswa")
root.geometry("800x600")
root.configure(bg="white")

# Label for title
Label(root, text="Kehadiran Mahasiswa", font=("Arial", 16), bg="white").pack(pady=10)

# Display canvas for camera feed
display_canvas = Canvas(root, width=640, height=480, bg="black")
display_canvas.pack(pady=10)

# Frame for buttons to organize them horizontally
button_frame = Canvas(root, bg="white")
button_frame.pack()

# Buttons for start and add image functions
start_button = Button(button_frame, text="START", command=start_recognition, font=("Arial", 12), bg="black", fg="white")
start_button.grid(row=0, column=0, padx=10, pady=10)

add_button = Button(button_frame, text="TAMBAHKAN DATA", command=add_image, font=("Arial", 12), bg="black", fg="white")
add_button.grid(row=0, column=1, padx=10, pady=10)

root.mainloop()