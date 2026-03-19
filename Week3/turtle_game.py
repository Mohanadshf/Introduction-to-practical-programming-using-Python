import turtle
import random
import math

def run():
    print("\n--- Turtle drawing (chaos triangle) ---")
    print("Close the turtle window when finished to return to the menu.\n")

    size_text = input("Enter triangle side length in pixels (default 300): ").strip()
    if size_text == '':
        size = 300
    else:
        size= int(size_text)

    iter_text = input("Enter number of iterations (default 2000): ").strip()
    if iter_text == '':
        iterations=2000
    else:
        iterations= int(iter_text)

    #Formula for height = root of 3 /2 * side
    h = (math.sqrt(3) /2) * size
    v1 = (-size/2, -h/3)
    v2 = (size/2, -h/3)
    v3 = (0, 2*h/3)
    vertices = [v1, v2, v3]

    #turtle means the moving pen to draw
    print("Turtle window should appear now...")
    screen = turtle.Screen() # opens the screen
    screen.title("Chaos Game – Triangle")

    t = turtle.Turtle()
    t.hideturtle()
    t.penup() # so it only draws points and not lines
    t.speed(0) # highest speed
    turtle.tracer(0,0) #idk what it does but it fastens the process

    outline = turtle.Turtle()
    outline.hideturtle()
    outline.penup()
    outline.goto(v1)
    outline.pendown()
    outline.goto(v2)
    outline.goto(v3)
    outline.goto(v1)
    outline.penup()

    t.goto(0, 0)  # start point

    for i in range(iterations):
        vx, vy = random.choice(vertices)
        x, y = t.position()
        new_x = (x + vx) / 2
        new_y = (y + vy) / 2
        t.goto(new_x, new_y)
        t.dot(2)  # small point

        # update screen occasionally
        if i % 200 == 0:
            turtle.update()

    turtle.update()

    print("Drawing complete. Click the turtle window to exit...")
    screen.exitonclick()
    print("Returned to main menu.\n")

if __name__ == "__main__":
    run()