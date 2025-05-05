import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np
import threading
import time

class SharpenParallelApp:
    def __init__(self, master):
        self.master = master
        master.title("Parallel Sharpen Filter")
        master.geometry("1024x768")
        self.original_image = None
        self.processed_image = None
        self.photo_image = None     
        self.num_threads = 4  # Número padrão de threads

        menu_bar = tk.Menu(master)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Abrir", command=self.open_image)
        file_menu.add_command(label="Salvar", command=self.save_image, state="disabled")
        file_menu.add_separator()
        file_menu.add_command(label="Sair", command=master.quit)
        self.file_menu = file_menu
        menu_bar.add_cascade(label="Arquivo", menu=self.file_menu)

        filter_menu = tk.Menu(menu_bar, tearoff=0)
        filter_menu.add_command(label="Reverter Filtros", command=self.revert_filters, state="disabled")
        filter_menu.add_separator()
        filter_menu.add_command(label="Sharpen", command=self.apply_sharpen, state="disabled")
        self.filter_menu = filter_menu
        menu_bar.add_cascade(label="Filtros", menu=self.filter_menu)

        master.config(menu=menu_bar)
        self.image_label = tk.Label(master, text="Nenhuma imagem carregada", bg="gray", fg="white")
        self.image_label.pack(expand=True, fill="both")
        self.status_var = tk.StringVar()
        self.status_var.set("Nenhuma imagem carregada.")
        status_label = tk.Label(master, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        status_label.pack(fill=tk.X, side=tk.BOTTOM)
        self.processing = False

    def open_image(self):
        if self.processing:
            return
        file_path = filedialog.askopenfilename(filetypes=[("Imagens", "*.png;*.jpg;*.jpeg")])
        if file_path:
            try:
                img = Image.open(file_path)
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível abrir a imagem:\n{e}")
                return
            if img.mode not in ("RGB", "RGBA"):
                img = img.convert("RGB")
            self.original_image = img
            self.processed_image = img
            self._display_image(img)
            self.file_menu.entryconfig("Salvar", state="normal")
        self.filter_menu.entryconfig("Reverter Filtros", state="normal")
        self.filter_menu.entryconfig("Sharpen", state="normal")
        self.status_var.set(f"Imagem carregada: {file_path}")

    def save_image(self):
        if self.processing or self.processed_image is None:
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG Image", "*.png"), ("JPEG Image", "*.jpg"), ("JPEG Image", "*.jpeg")])
        if file_path:
            try:
                self.processed_image.save(file_path)
                self.status_var.set(f"Imagem salva em: {file_path}")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar imagem:\n{e}")

    def revert_filters(self):
        if self.processing or self.original_image is None:
            return
        self.processed_image = self.original_image.copy()
        self._display_image(self.processed_image)
        self.status_var.set("Filtros revertidos para original.")

    def _display_image(self, img):
        self.photo_image = ImageTk.PhotoImage(img)
        self.image_label.config(image=self.photo_image)
        self.image_label.image = self.photo_image
        self.image_label.config(bg="black")

    def _start_processing(self, name):
        self.processing = True
        self.status_var.set(f"Aplicando filtro: {name} ...")
        self.filter_menu.entryconfig("Sharpen", state="disabled")
        self.filter_menu.entryconfig("Reverter Filtros", state="disabled")
        self.master.config(cursor="wait")
        self.master.update()

    def _end_processing(self):
        self.processing = False
        self.filter_menu.entryconfig("Sharpen", state="normal")
        self.filter_menu.entryconfig("Reverter Filtros", state="normal")
        self.master.config(cursor="")
        self.master.update()

    def apply_sharpen(self):
        if self.processed_image is None or self.processing:
            return
        thread = threading.Thread(target=self._sharpen_thread)
        thread.daemon = True
        thread.start()

    def _sharpen_thread(self):
        self.master.after(0, lambda: self._start_processing("Sharpen"))
        start_time = time.time()
        img = self.processed_image
        kernel = np.array([[0, -1, 0],
                           [-1, 5, -1],
                           [0, -1, 0]])
        result_img = self._apply_convolution(img, kernel)
        elapsed = time.time() - start_time
        print(f"Tempo de processamento Sharpen: {elapsed:.2f} segundos")
        self.master.after(0, lambda: self._update_image_result(result_img, "Filtro Sharpen aplicado."))

    def _update_image_result(self, img, status_text):
        self.processed_image = img
        self._display_image(img)
        self.status_var.set(status_text)
        self._end_processing()

    def _apply_convolution(self, img, kernel, offset=0):
        arr = np.array(img)
        alpha = None
        if arr.ndim == 3 and arr.shape[2] == 4:
            alpha = arr[..., 3]
            arr = arr[..., :3]
        h, w = arr.shape[0], arr.shape[1]
        channels = 1 if arr.ndim == 2 else arr.shape[2]
        kH, kW = kernel.shape
        pad_h = kH // 2
        pad_w = kW // 2
        if arr.ndim == 2:
            arr_padded = np.pad(arr, ((pad_h, pad_h), (pad_w, pad_w)), mode='edge')
        else:
            arr_padded = np.pad(arr, ((pad_h, pad_h), (pad_w, pad_w), (0, 0)), mode='edge')
        result = np.zeros((h, w, channels), dtype=np.int16) if channels > 1 else np.zeros((h, w), dtype=np.int16)
        num_threads = min(self.num_threads, h)
        lines_per_thread = h // num_threads
        threads = []
        def process_rows(row_start, row_end):
            for i in range(row_start, row_end):
                for j in range(w):
                    if channels == 1:
                        total = 0
                        for ki in range(kH):
                            for kj in range(kW):
                                total += kernel[ki, kj] * int(arr_padded[i + ki, j + kj])
                        total += offset
                        result[i, j] = np.clip(total, 0, 255)
                    else:
                        for c in range(channels):
                            total = 0
                            for ki in range(kH):
                                for kj in range(kW):
                                    total += kernel[ki, kj] * int(arr_padded[i + ki, j + kj, c])
                            total += offset
                            result[i, j, c] = np.clip(total, 0, 255)
        start = 0
        for t in range(num_threads):
            end = h if t == num_threads - 1 else start + lines_per_thread
            th = threading.Thread(target=process_rows, args=(start, end))
            th.start()
            threads.append(th)
            start = end
        for th in threads:
            th.join()
        if alpha is not None:
            if result.ndim == 2:
                result = np.expand_dims(result, axis=2)
            result = np.dstack([result.astype(np.uint8), alpha])
            mode = "RGBA"
        else:
            result = result.astype(np.uint8)
            mode = "RGB" if channels == 3 else "L"
        return Image.fromarray(result, mode=mode)

def main():
    root = tk.Tk()
    app = SharpenParallelApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
