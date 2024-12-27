import tkinter as tk
import math

class CurveApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Exponential Curves")
        self.root.geometry("1400x500")
        
        self.canvas = tk.Canvas(root, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.slider_bend = tk.Scale(root, from_=-2, to=2, resolution=0.01, orient=tk.HORIZONTAL, command=self.update_curve)
        self.slider_bend.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.slider_strength = tk.Scale(root, from_=1, to=4, resolution=0.01, orient=tk.HORIZONTAL, label="Curve Strength", command=self.update_curve)
        self.slider_strength.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.slider_distance = tk.Scale(root, from_=50, to=800, resolution=1, orient=tk.HORIZONTAL, label="Distance Between Lines", command=self.update_curve)
        self.slider_distance.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.slider_tiling = tk.Scale(root, from_=0, to=-400, resolution=1, orient=tk.HORIZONTAL, label="Tiling Factor", command=self.update_curve)
        self.slider_tiling.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.bend_factor = 0
        self.curve_strength = 1
        self.distance_between_lines = 300 
        self.tiling_factor = -100  
        self.canvas.bind("<Configure>", lambda event: self.draw_curve())
        
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
        ratio = bend_factor / max_bend
        red = int(255 * ratio)
        green = int(255 * (1 - ratio))
        return f"#{red:02x}{green:02x}00"
    
    def update_curve(self, value=None):
        self.bend_factor = max(-2, min(2, float(self.slider_bend.get())))
        self.curve_strength = float(self.slider_strength.get())
        self.distance_between_lines = float(self.slider_distance.get())
        self.tiling_factor = float(self.slider_tiling.get())
        self.draw_curve()

if __name__ == "__main__":
    root = tk.Tk()
    app = CurveApp(root)
    root.mainloop()
