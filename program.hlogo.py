import turtle
t = turtle.Turtle()
for i in range(10):
   t.forward(40)
   t.right(100)
   t.penup()
   t.forward(10)
   t.pendown()
   for i in range(10):
       t.forward(40)
       t.right(100)
       t.penup()
       t.forward(10)
       t.pendown()
if ((1>0)and(0<1)):
   t.forward(40)
turtle.mainloop() 
