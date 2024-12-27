import tkinter as tk
import math

class CurveApp:
    def __init__(self, root):
        self.root = root
        self.root.title("exponential")
        self.root.geometry("1400x500")
        
        self.canvas = tk.Canvas(root, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.slider = tk.Scale(root, from_=-2, to=2, resolution=0.01, orient=tk.HORIZONTAL, command=self.update_curve)
        self.slider.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.bend_factor = 0
        self.canvas.bind("<Configure>", lambda event: self.draw_curve())
        
    def draw_curve(self):
        self.canvas.delete("all")
        
        canvas_width = self.canvas.winfo_width()
        start_x = canvas_width / 2 - 150
        spacing = 300
        tilt_factor = -100
        
        start_y, end_y = 100, 400
        
        points1 = []
        points2 = []
        steps = 100
        
        for t in range(steps + 1):
            y = start_y + t * (end_y - start_y) / steps
            # Apply a stronger curve with higher power of bend_factor
            offset = (math.exp(abs(self.bend_factor) * (1 - (y - start_y) / (end_y - start_y))) - 1) ** 2
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
        ratio = bend_factor / max_bend
        red = int(255 * ratio)
        green = int(255 * (1 - ratio))
        return f"#{red:02x}{green:02x}00"
    
    def update_curve(self, value):
        self.bend_factor = max(-2, min(2, float(value)))
        self.draw_curve()

if __name__ == "__main__":
    root = tk.Tk()
    app = CurveApp(root)
    root.mainloop()
