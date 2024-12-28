import tkinter as tk
from tkinter.colorchooser import askcolor
import math
#fix ui
#cascade color inputs

class CurveApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Car Guide")
        self.root.geometry("1400x500")
        self.canvas = tk.Canvas(root, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.straight_color = "#00ff00"  # green
        self.slight_curve_color = "#ffff00"  # yellow
        self.curve_color = "#ff0000"  # red
        self.bg_color = "#ffffff"  # white

        self.color_frame = tk.Frame(root)
        self.color_frame.pack(side=tk.TOP, fill=tk.X)

        self.straight_color_entry = self.add_color_input(
            "Straight Color", self.straight_color, lambda color: self.set_color("straight_color", color)
        )
        self.slight_curve_color_entry = self.add_color_input(
            "Slight Curve Color", self.slight_curve_color, lambda color: self.set_color("slight_curve_color", color)
        )
        self.curve_color_entry = self.add_color_input(
            "Curve Color", self.curve_color, lambda color: self.set_color("curve_color", color)
        )
        self.bg_color_entry = self.add_color_input(
            "Background Color", self.bg_color, self.set_bg_color
        )

        self.slider_bend = tk.Scale(root, from_=-2, to=2, resolution=0.01, orient=tk.HORIZONTAL, command=self.update_curve)
        self.slider_bend.pack(side=tk.BOTTOM, fill=tk.X)

        self.slider_strength = tk.Scale(root, from_=1, to=4, resolution=0.01, orient=tk.HORIZONTAL, label="Curve Strength", command=self.update_curve)
        self.slider_strength.pack(side=tk.RIGHT, fill=tk.Y)

        self.slider_distance = tk.Scale(root, from_=50, to=800, resolution=1, orient=tk.HORIZONTAL, label="Distance Between Lines", command=self.update_curve)
        self.slider_distance.pack(side=tk.RIGHT, fill=tk.Y)

        self.slider_tiling = tk.Scale(root, from_=0, to=-400, resolution=1, orient=tk.HORIZONTAL, label="Tiling Factor", command=self.update_curve)
        self.slider_tiling.pack(side=tk.RIGHT, fill=tk.Y)

        self.slider_yellow_threshold = tk.Scale(root, from_=0.7, to=1.5, resolution=0.01, orient=tk.HORIZONTAL, label="Middle Color Threshold", command=self.update_curve)
        self.slider_yellow_threshold.pack(side=tk.RIGHT, fill=tk.Y)

        self.slider_scroll_distance = tk.Scale(root, from_=0.01, to=0.2, resolution=0.01, orient=tk.HORIZONTAL, label="Dis. per Scroll", command=self.update_scroll_distance)
        self.slider_scroll_distance.set(0.1)
        self.slider_scroll_distance.pack(side=tk.RIGHT, fill=tk.Y)

        self.bend_factor = 0
        self.curve_strength = 1
        self.distance_between_lines = 50 
        self.tiling_factor = 0  
        self.yellow_threshold = 1.3
        self.scroll_step_size = 0.1  
        self.canvas.bind("<Configure>", lambda event: self.draw_curve())

        self.fullscreen_button = tk.Button(root, text="Fullscreen", command=self.toggle_fullscreen)
        self.fullscreen_button.pack(side=tk.TOP, padx=10, pady=5)

        self.canvas.bind("<MouseWheel>", self.on_scroll)

        self.root.bind("<Escape>", self.toggle_fullscreen_on_escape)

    def add_color_input(self, label, default_color, command):
        frame = tk.Frame(self.color_frame)
        frame.pack(side=tk.LEFT, padx=10)

        tk.Label(frame, text=label).pack()
        entry = tk.Entry(frame, width=10)
        entry.insert(0, default_color)
        entry.pack()

        def on_update_color():
            hex_color = entry.get()
            if len(hex_color) == 7 and hex_color[0] == "#":
                command(hex_color)
            else:
                tk.messagebox.showerror("Invalid Color", "Enter a valid hex color (e.g., #00ff00).")

        entry.bind("<Return>", lambda e: on_update_color())
        tk.Button(frame, text="Select", command=lambda: self.pick_color(command, entry)).pack()

        return entry

    def set_color(self, color_attr, color=None):
        if color:
            setattr(self, color_attr, color)
            self.update_curve()

    def set_bg_color(self, color):
        if color:
            self.canvas.config(bg=color)

    def pick_color(self, command, entry):
        color = askcolor()[1]
        if color:
            command(color)
            entry.delete(0, tk.END)
            entry.insert(0, color)

    def draw_curve(self):
        self.canvas.delete("all")

        canvas_width = self.canvas.winfo_width()
        start_x = (canvas_width - self.distance_between_lines) / 2  
        spacing = self.distance_between_lines
        tilt_factor = self.tiling_factor

        start_y, end_y = 100, 400

        points1 = []
        points2 = []
        steps = 100

        for t in range(steps + 1):
            y = start_y + t * (end_y - start_y) / steps

            offset = (math.exp(abs(self.bend_factor) * (1 - (y - start_y) / (end_y - start_y))) - 1) ** self.curve_strength
            offset *= 1 if self.bend_factor >= 0 else -1

            x1 = start_x + offset * spacing - tilt_factor * (1 - t / steps)
            x2 = start_x + spacing + offset * spacing + tilt_factor * (1 - t / steps)
            points1.append((x1, y))
            points2.append((x2, y))

        color = self.get_color(abs(self.bend_factor))

        for i in range(len(points1) - 1):
            x1, y1 = points1[i]
            x2, y2 = points1[i + 1]
            self.canvas.create_line(x1, y1, x2, y2, fill=color, width=6)

        for i in range(len(points2) - 1):
            x1, y1 = points2[i]
            x2, y2 = points2[i + 1]
            self.canvas.create_line(x1, y1, x2, y2, fill=color, width=6)

    def get_color(self, bend_factor):
        max_bend = 2
        yellow_threshold = self.yellow_threshold

        ratio = bend_factor / max_bend

        if ratio < (yellow_threshold / max_bend): 
            ratio_scaled = ratio * max_bend / yellow_threshold
            return self.blend_colors(self.straight_color, self.slight_curve_color, ratio_scaled)
        else:
            ratio_scaled = (ratio - yellow_threshold / max_bend) / (1 - yellow_threshold / max_bend)
            return self.blend_colors(self.slight_curve_color, self.curve_color, ratio_scaled)

    def blend_colors(self, color1, color2, ratio):
        r1, g1, b1 = self.hex_to_rgb(color1)
        r2, g2, b2 = self.hex_to_rgb(color2)

        r = int(r1 + (r2 - r1) * ratio)
        g = int(g1 + (g2 - g1) * ratio)
        b = int(b1 + (b2 - b1) * ratio)

        return f"#{r:02x}{g:02x}{b:02x}"

    def hex_to_rgb(self, hex_color):
        hex_color = hex_color.lstrip("#")
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def update_curve(self, value=None):
        self.bend_factor = max(-2, min(2, float(self.slider_bend.get())))
        self.curve_strength = float(self.slider_strength.get())
        self.distance_between_lines = float(self.slider_distance.get())
        self.tiling_factor = float(self.slider_tiling.get())
        self.yellow_threshold = float(self.slider_yellow_threshold.get())
        self.draw_curve()

    def update_scroll_distance(self, value=None):
        self.scroll_step_size = float(self.slider_scroll_distance.get())

    def on_scroll(self, event):
        """Adjust bend factor with the scroll wheel."""
        delta = event.delta
        current_value = float(self.slider_bend.get())
        if delta > 0:
            new_value = min(2, current_value + self.scroll_step_size)  #scroll up
        else:
            new_value = max(-2, current_value - self.scroll_step_size)  #scroll down
        self.slider_bend.set(new_value)
        self.update_curve()

    def toggle_fullscreen(self, event=None):
        """Toggle fullscreen mode by hiding UI elements and expanding canvas"""
        if self.color_frame.winfo_ismapped():
            #death to the ui elements!
            self.color_frame.pack_forget()
            self.slider_bend.pack_forget()
            self.slider_strength.pack_forget()
            self.slider_distance.pack_forget()
            self.slider_tiling.pack_forget()
            self.slider_yellow_threshold.pack_forget()
            self.fullscreen_button.pack_forget()
            self.slider_scroll_distance.pack_forget()

            self.root.attributes("-fullscreen", True)
            self.canvas.pack(fill=tk.BOTH, expand=True)
        else:
            #reappear
            self.color_frame.pack(side=tk.TOP, fill=tk.X)
            self.slider_bend.pack(side=tk.BOTTOM, fill=tk.X)
            self.slider_strength.pack(side=tk.RIGHT, fill=tk.Y)
            self.slider_distance.pack(side=tk.RIGHT, fill=tk.Y)
            self.slider_tiling.pack(side=tk.RIGHT, fill=tk.Y)
            self.slider_yellow_threshold.pack(side=tk.RIGHT, fill=tk.Y)
            self.slider_scroll_distance.pack(side=tk.RIGHT, fill=tk.Y)
            self.fullscreen_button.pack(side=tk.TOP, padx=10, pady=5)

            self.root.attributes("-fullscreen", False)
            self.canvas.pack(fill=tk.BOTH, expand=True)

    def toggle_fullscreen_on_escape(self, event=None):
        if self.root.attributes("-fullscreen"):
            self.toggle_fullscreen()


if __name__ == "__main__":
    root = tk.Tk()
    app = CurveApp(root)
    root.mainloop()
