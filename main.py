import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw, ImageFont

class WatermarkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Watermarking Application")
        self.root.geometry("600x750")  # Slightly adjusted height for the compact layout

        # Set custom icon
        self.root.iconphoto(False, tk.PhotoImage(file="images/icon.png"))

        # Variables to store image and watermark
        self.image = None
        self.watermark_text = tk.StringVar()
        self.watermark_image = None

        # Title label with custom font and color
        title_label = tk.Label(root, text="Watermarking Tool", font=("Arial", 20, "bold"), bg="#282C34", fg="white")
        title_label.pack(pady=10)

        # Upload Image Button
        self.upload_button = ttk.Button(root, text="Upload Image", command=self.upload_image, width=20)
        self.upload_button.pack(pady=10)

        # Watermark Text Entry with label
        entry_frame = tk.Frame(root, bg="#282C34")
        entry_frame.pack(pady=5)

        self.text_entry_label = tk.Label(entry_frame, text="Enter Watermark Text:", font=("Arial", 12), bg="#282C34", fg="white")
        self.text_entry_label.pack(side=tk.LEFT, padx=5)
        self.text_entry = tk.Entry(entry_frame, textvariable=self.watermark_text, font=("Arial", 12), width=20)
        self.text_entry.pack(side=tk.LEFT, padx=5)

        # Frame for Apply and Save buttons
        button_frame = tk.Frame(root, bg="#282C34")
        button_frame.pack(pady=10)

        # Apply Watermark Button
        self.apply_button = ttk.Button(button_frame, text="Apply Watermark", command=self.apply_watermark, width=20)
        self.apply_button.pack(side=tk.LEFT, padx=10)

        # Save Image Button (initially disabled)
        self.save_button = ttk.Button(button_frame, text="Save Image", command=self.save_image, width=20)
        self.save_button.pack(side=tk.LEFT, padx=10)
        self.save_button.config(state=tk.DISABLED)

        # Canvas to display the image
        self.canvas = tk.Canvas(root, width=500, height=500, bg="#ABB2BF")
        self.canvas.pack(pady=10)

        # Set window background color
        self.root.configure(bg="#282C34")

    def upload_image(self):
        """Upload an image file."""
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
        if file_path:
            self.image = Image.open(file_path)
            self.display_image(self.image)

    def display_image(self, image):
        """Display the image on the canvas."""
        image.thumbnail((500, 500))  # Thumbnail size to fit the canvas
        self.img_tk = ImageTk.PhotoImage(image)
        self.canvas.create_image(250, 250, image=self.img_tk)

    def apply_watermark(self):
        """Apply a diagonal watermark that fully covers the entire image, including all corners."""
        if self.image:
            watermark_text = self.watermark_text.get()
            if watermark_text:
                # Convert the original image to RGBA (with alpha channel)
                watermarked_image = self.image.convert("RGBA")

                # Create a new image for the watermark with an alpha channel (RGBA)
                txt_layer = Image.new("RGBA", (watermarked_image.size[0] * 2, watermarked_image.size[1] * 2), (255, 255, 255, 0))

                draw = ImageDraw.Draw(txt_layer)

                # Set the font size based on the image size
                font_size = int(watermarked_image.size[0] / len(watermark_text) * 0.3)
                font = ImageFont.truetype("arial.ttf", font_size)

                # Calculate the size of the text box using textbbox
                bbox = draw.textbbox((0, 0), watermark_text, font=font)
                text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]

                # Determine the start position with more margin to cover all corners
                margin_x = int(watermarked_image.size[0] * 0.25)
                margin_y = int(watermarked_image.size[1] * 0.25)

                # Place watermark text with increased overlap
                for y in range(-margin_y, txt_layer.size[1], text_height * 2):
                    for x in range(-margin_x, txt_layer.size[0], text_width * 2):
                        draw.text((x, y), watermark_text, fill=(255, 255, 255, 150), font=font)

                # Rotate the text layer to cover the entire image
                txt_layer = txt_layer.rotate(45, expand=True)

                # Crop the txt_layer back to the original image size
                txt_layer = txt_layer.crop((txt_layer.size[0] // 4, txt_layer.size[1] // 4,
                                            txt_layer.size[0] * 3 // 4, txt_layer.size[1] * 3 // 4))

                # Create a new image with the same size as the original to composite the rotated text layer
                rotated_layer = Image.new("RGBA", watermarked_image.size, (255, 255, 255, 0))
                rotated_layer.paste(txt_layer, (0, 0), txt_layer)

                # Combine the watermark with the original image
                watermarked_image = Image.alpha_composite(watermarked_image, rotated_layer)

                # Display the final image
                self.display_image(watermarked_image.convert("RGB"))
                self.watermark_image = watermarked_image

                # Enable the save button and ensure it is visible
                self.save_button.config(state=tk.NORMAL)
            else:
                messagebox.showwarning("Input Error", "Please enter watermark text.")
        else:
            messagebox.showwarning("Input Error", "Please upload an image first.")

    def save_image(self):
        """Save the watermarked image."""
        if self.watermark_image:
            save_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                     filetypes=[("PNG Files", "*.png"),
                                                                ("JPEG Files", "*.jpg"),
                                                                ("All Files", "*.*")])
            if save_path:
                self.watermark_image.save(save_path)
                messagebox.showinfo("Image Saved", f"Image saved to {save_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = WatermarkApp(root)
    root.mainloop()
