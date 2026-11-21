
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os


# 6.1 Module: Image Node Creation
class Node:
    def __init__(self, image_path):
        self.image_path = image_path
        self.prev = None
        self.next = None


# 6.2 Module: Doubly Linked List Initialization
class DoublyLinkedListGallery:
    def __init__(self):
        self.head = None
        self.tail = None
        self.current = None
        self.size = 0

    # 6.3 Module: Image Insertion
    def add_image(self, image_path):
        new_node = Node(image_path)

        if self.head is None:
            self.head = self.tail = self.current = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node

        self.size += 1

    # 6.4 Module: Next Image Navigation
    def next_image(self):
        if self.current and self.current.next:
            self.current = self.current.next
            return self.current.image_path
        return None

    # Previous Image Navigation
    def previous_image(self):
        if self.current and self.current.prev:
            self.current = self.current.prev
            return self.current.image_path
        return None

    # 6.5 Module: Image Deletion
    def delete_current(self):
        if self.current is None:
            return False

        node = self.current

        if node.prev:
            node.prev.next = node.next
        else:
            self.head = node.next

        if node.next:
            node.next.prev = node.prev
        else:
            self.tail = node.prev

        self.current = node.next if node.next else node.prev

        self.size -= 1
        return True

    # 6.8 Module: Gallery Information
    def get_gallery_info(self):
        if self.current is None:
            return "No images available"

        count = 1
        temp = self.head

        while temp != self.current:
            count += 1
            temp = temp.next

        return f"Image {count} of {self.size}"


# 6.6 Module: Image Display
def display_image(image_path):
    image = Image.open(image_path)
    image.thumbnail((650, 420))
    photo = ImageTk.PhotoImage(image)
    return photo


# Main Application
class ImageGalleryApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Image Gallery Management System")
        self.root.geometry("900x650")
        self.root.configure(bg="#20232a")

        self.gallery = DoublyLinkedListGallery()
        self.photo = None

        self.create_ui()

    # GUI Design
    def create_ui(self):

        title = tk.Label(
            self.root,
            text="IMAGE GALLERY",
            font=("Arial", 24, "bold"),
            bg="#20232a",
            fg="white"
        )
        title.pack(pady=20)

        self.image_frame = tk.Frame(
            self.root,
            bg="#30343b",
            width=700,
            height=440
        )
        self.image_frame.pack(pady=10)
        self.image_frame.pack_propagate(False)

        self.image_label = tk.Label(
            self.image_frame,
            text="No Image Selected",
            bg="#30343b",
            fg="white",
            font=("Arial", 16)
        )
        self.image_label.pack(expand=True)

        self.info_label = tk.Label(
            self.root,
            text="No images available",
            font=("Arial", 13),
            bg="#20232a",
            fg="white"
        )
        self.info_label.pack(pady=10)

        button_frame = tk.Frame(
            self.root,
            bg="#20232a"
        )
        button_frame.pack(pady=15)

        tk.Button(
            button_frame,
            text="Add Images",
            command=self.select_images,
            width=14,
            bg="#28a745",
            fg="white",
            font=("Arial", 11, "bold")
        ).grid(row=0, column=0, padx=8)

        tk.Button(
            button_frame,
            text="Previous",
            command=self.previous_image,
            width=14,
            bg="#007bff",
            fg="white",
            font=("Arial", 11, "bold")
        ).grid(row=0, column=1, padx=8)

        tk.Button(
            button_frame,
            text="Next",
            command=self.next_image,
            width=14,
            bg="#007bff",
            fg="white",
            font=("Arial", 11, "bold")
        ).grid(row=0, column=2, padx=8)

        tk.Button(
            button_frame,
            text="Delete",
            command=self.delete_image,
            width=14,
            bg="#dc3545",
            fg="white",
            font=("Arial", 11, "bold")
        ).grid(row=0, column=3, padx=8)

        tk.Button(
            button_frame,
            text="Exit",
            command=self.root.destroy,
            width=14,
            bg="#555555",
            fg="white",
            font=("Arial", 11, "bold")
        ).grid(row=0, column=4, padx=8)

    # 6.7 Module: Image Selection
    def select_images(self):
        file_paths = filedialog.askopenfilenames(
            title="Select Images",
            filetypes=[
                ("Image Files", "*.png *.jpg *.jpeg *.gif *.bmp")
            ]
        )

        for path in file_paths:
            self.gallery.add_image(path)

        self.show_current_image()

    # Display Current Image
    def show_current_image(self):
        if self.gallery.current is None:
            self.image_label.config(
                image="",
                text="No Image Selected"
            )
            self.photo = None
        else:
            try:
                path = self.gallery.current.image_path
                self.photo = display_image(path)

                self.image_label.config(
                    image=self.photo,
                    text=""
                )

            except Exception as e:
                messagebox.showerror(
                    "Image Error",
                    str(e)
                )

        self.info_label.config(
            text=self.gallery.get_gallery_info()
        )

    # Next Button
    def next_image(self):
        if self.gallery.next_image():
            self.show_current_image()
        else:
            messagebox.showinfo(
                "Navigation",
                "This is the last image."
            )

    # Previous Button
    def previous_image(self):
        if self.gallery.previous_image():
            self.show_current_image()
        else:
            messagebox.showinfo(
                "Navigation",
                "This is the first image."
            )

    # Delete Button
    def delete_image(self):
        if self.gallery.current is None:
            messagebox.showwarning(
                "Warning",
                "No image available to delete."
            )
            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Remove this image from the gallery?"
        )

        if confirm:
            self.gallery.delete_current()
            self.show_current_image()


# Main Program Execution
if __name__ == "__main__":
    root = tk.Tk()
    app = ImageGalleryApp(root)
    root.mainloop()
      
