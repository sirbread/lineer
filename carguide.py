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
        self.spacing = 50
        self.draw_curve()
    
    def draw_curve(self):
        self.canvas.delete("all")
        
        start_x1, start_y = 200, 100
        start_x2 = start_x1 + self.spacing
        end_x1, end_y = 200, 400
        end_x2 = end_x1 + self.spacing
        
        control_x1 = start_x1 + self.curvature
        control_x2 = start_x2 + self.curvature
        control_y = (start_y + end_y) / 2

        steps = 100
        points1 = []
        points2 = []
        
        for t in range(steps + 1):
            t /= steps
            x1 = (1 - t)**2 * start_x1 + 2 * (1 - t) * t * control_x1 + t**2 * end_x1
            y1 = (1 - t)**2 * start_y + 2 * (1 - t) * t * control_y + t**2 * end_y
            x2 = (1 - t)**2 * start_x2 + 2 * (1 - t) * t * control_x2 + t**2 * end_x2
            y2 = (1 - t)**2 * start_y + 2 * (1 - t) * t * control_y + t**2 * end_y
            points1.append((x1, y1))
            points2.append((x2, y2))
        
        for i in range(len(points1) - 1):
            x1, y1 = points1[i]
            x2, y2 = points1[i + 1]
            self.canvas.create_line(x1, y1, x2, y2, fill="blue", width=2)
        
        for i in range(len(points2) - 1):
            x1, y1 = points2[i]
            x2, y2 = points2[i + 1]
            self.canvas.create_line(x1, y1, x2, y2, fill="blue", width=2)
    
    def update_curve(self, value):
        self.curvature = int(value)
        self.draw_curve()

if __name__ == "__main__":
    root = tk.Tk()
    app = curve(root)
    root.mainloop()
