# lineer - car hud steering guidance system
check out the demo [here](https://www.youtube.com/watch?v=UqEKbWCKcXU)!
lineer is a car hud (heads-up display) guidance system that helps drivers navigate with a dynamic  line on their vehicle's hud. <br>
it uses a combination of graphical elements and interactive sliders to adjust how the guidance lines appear based on the steering wheel’s input.<br> 
when the steering wheel turns, a scroll wheel on a mouse turns (which you have to mount), which bends the lines on the hud to provide real-time visual guidance.

## features:
- dynamic line bending: adjust the curvature of the guidance lines in real-time using your steering wheel 
- interactive sliders: fine-tune various parameters such as curve strength, distance between lines, tiling factor, and color thresholds to enhance visibility
- color preferences: customize the color of the guidance lines and the background to suit personal preferences

## installation:
1. clone thy repo.
2. no libraries are required! uses tkinter.  
3. run `lineer.py` 

## usage:
- adjusting guidance lines: use the sliders to control the curvature, strength, distance, and tiling of the guidance lines to calibrate it to your car
- color customization: open the color preferences window to select the desired colors for straight lines, slight curves, and full curves <br>
  (i recommend going for a stark black background for best hud visibility)
- mount a mouse, with the scroll wheel touching the steering wheel, somewhere in your car, like from the dash. 
- go in fullscreen, and put your display on the dash, where it can be reflected on your windshield.
- turn your wheel!

## customization:
- sliders:  
  - slider for bend: controls the curvature of the guidance line (when turning)
  - slider for curve strength: adjusts the strength of the bend  (make it more "bent" from the top/bottom)
  - slider for distance: sets the distance between the guidance lines  
  - slider for tiling factor: controls the effect of tiling on the guidance lines (yknow, road)
  - slider for yellow threshold: affects the mid-point color transition from green to yellow (or start color to mid color)
  - slider for scroll distance: determines how much the guidance bends with each scroll tick
- colors:  
  - straight color: the base color for the guidance line, completely straight  
  - slight curve color: the color that transitions from straight to slightly curved lines, slightly bent
  - curve color: the color representing strongly curved lines, fully bent
  - background color: customize the background to suit your preference

## a plead from the broke
if you have a more reliable way to make the rotary encoder part (such as using an Arduino rotary encoder), please (attempt to) make it. i don't have that kind of stuff on me right now, and i want to see this part of the project actually be reliable. thank you <3  
