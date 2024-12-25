import tkinter as tk
from math import sin, cos, radians

class curve:
    def __init__(self, root):
        self.root = root
        self.root.title("curve test thing")
        self.root.geometry("500x500")
        
        self.canvas = tk.Canvas(root, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.curvature = 0 
        
        button_frame = tk.Frame(root)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        left_button = tk.Button(button_frame, text="up", command=self.curve_up)
        left_button.pack(side=tk.LEFT, expand=True, fill=tk.X)
        
        right_button = tk.Button(button_frame, text="down", command=self.curve_down)
        right_button.pack(side=tk.RIGHT, expand=True, fill=tk.X)
        
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
    
    def curve_up(self):
        self.curvature -= 20
        self.draw_curve()
    
    def curve_down(self):
        self.curvature += 20
        self.draw_curve()

if __name__ == "__main__":
    root = tk.Tk()
    app = curve(root)
    root.mainloop()


#so like will this comment show up if i push another time
#how about anotehr time