import tkinter as tk

class curve:
    def __init__(self, root):
        self.root = root
        self.root.title("curve test thing")
        self.root.geometry("500x500")
        
        self.canvas = tk.Canvas(root, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.slider = tk.Scale(root, from_=-200, to=200, orient=tk.HORIZONTAL, command=self.update_curve)
        self.slider.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.curvature = 0
        self.draw_curve()
    
    def draw_curve(self):
        self.canvas.delete("all")
        
        start_x, start_y = 100, 250
        end_x, end_y = 400, 250
        
        control_x = (start_x + end_x) / 2
        control_y = 250 + self.curvature
        
        # bezier curve, maybe change to exponential
        steps = 100
        points = []
        for t in range(steps + 1):
            t /= steps
            x = (1 - t)**2 * start_x + 2 * (1 - t) * t * control_x + t**2 * end_x
            y = (1 - t)**2 * start_y + 2 * (1 - t) * t * control_y + t**2 * end_y
            points.append((x, y))
        
        for i in range(len(points) - 1):
            x1, y1 = points[i]
            x2, y2 = points[i + 1]
            self.canvas.create_line(x1, y1, x2, y2, fill="blue", width=2)
    
    def update_curve(self, value):
        self.curvature = int(value)
        self.draw_curve()

if __name__ == "__main__":
    root = tk.Tk()
    app = curve(root)
    root.mainloop()