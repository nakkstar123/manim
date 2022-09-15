from manim import *
class Optimization(Scene):

    def construct(self):
        axes = Axes(x_range = [0, 10], y_range = [0, 10], x_length = 5, y_length = 5, tips = False, axis_config = {"include_ticks": False}, y_axis_config = {"stroke_width": 0})
        axes.move_to([-1.5, 1, 0])
        self.add(axes)

        DOT_X = 5
        DOT_Y = 3

        pt = Dot(axes.c2p(DOT_X, DOT_Y), color = BLUE)

        origin = Dot(axes.c2p(0, 0))

        self.add(origin)

        x = ValueTracker(3)
        y = ValueTracker(2)

        ANGLE = 60*DEGREES

        angle_side = Line(start = axes.c2p(-0.1,-0.1), stroke_width = 2.0).set_angle(ANGLE).set_length(5)

        self.add(angle_side)

        x_int = always_redraw(lambda: Dot(axes.c2p(x.get_value(), 0)))
        y_int = always_redraw(lambda: Dot(axes.c2p(y.get_value()*np.cos(ANGLE), y.get_value()*np.sin(ANGLE))))



        triangle = always_redraw(lambda: Polygram([axes.c2p(x.get_value(), 0), axes.c2p(DOT_X,DOT_Y), axes.c2p(y.get_value()*np.cos(ANGLE), y.get_value()*np.sin(ANGLE))]))

        self.play(Write(pt))
        self.play(Create(triangle))
        self.play(Write(x_int), Write(y_int))



        line_group = VGroup()        
        for i, j in zip([1, 5, 3], [1.5, 5, 2]):


          x.set_value(i)
          y.set_value(j)

          # this part seems too redundant but for some reason doesn't work without it

          x1 = x.get_value()
          y1 = 0
          x2 = y.get_value()*np.cos(ANGLE)
          y2 = y.get_value()*np.sin(ANGLE)
          
          perimeter = np.linalg.norm(axes.c2p(DOT_X, DOT_Y) - axes.c2p(x1, y1)) + np.linalg.norm(axes.c2p(DOT_X, DOT_Y) - axes.c2p(x2, y2)) + np.linalg.norm(axes.c2p(x1, y1) - axes.c2p(x2, y2))

          perimeter_line = Line(start = [0, 0, 0], end = [0, perimeter, 0]).set_color(BLUE)

          line_group.add(perimeter_line)

        line_group.arrange(direction = RIGHT, buff = 0.5)
        line_group.move_to(axes.c2p(15, 3.5))



        # resetting tracker values

        x.set_value(3)
        y.set_value(2)        


        count = 0
        for i, j in zip([1, 5, 3], [1.5, 5, 2]):
          self.play(
              x.animate.set_value(i),  y.animate.set_value(j), run_time = 2, rate_func = smooth
          )
          self.play(TransformFromCopy(triangle, line_group[count]), run_time = 3)
          self.wait()
          count = count + 1


        self.wait()


        self.play(FadeOut(VGroup(triangle, x_int, y_int)))
  

        x_bis = Line(start = pt, end = axes.c2p(DOT_X, 0), color = RED)

        y_bis_x = np.cos(ANGLE)*(DOT_X*np.cos(ANGLE) + DOT_Y*np.sin(ANGLE))
        y_bis_y = np.sin(ANGLE)*(DOT_X*np.cos(ANGLE) + DOT_Y*np.sin(ANGLE))

        y_bis = Line(start = pt, end = axes.c2p(y_bis_x, y_bis_y), color = GREEN)

        self.play(Write(x_bis), Write(y_bis), run_time = 2)

        x_bis_mirr = DashedLine(start = axes.c2p(DOT_X, 0), end = axes.c2p(DOT_X, -1 * DOT_Y)).set_color(RED)


# # improve nomenclature

        a = DOT_X
        b = DOT_Y
        c = y_bis_x
        d = y_bis_y

        y_bis_mirr_x = 2*c - a
        y_bis_mirr_y = 2*d - b
        y_bis_mirr = DashedLine(start = axes.c2p(y_bis_x, y_bis_y), end = axes.c2p(y_bis_mirr_x, y_bis_mirr_y)).set_color(GREEN)

        self.wait()

        self.play(Write(x_bis_mirr), Write(y_bis_mirr), run_time = 2)

        self.wait()


        pt1 = Dot(axes.c2p(DOT_X, -1 * DOT_Y)).set_color(YELLOW)
        pt2 = Dot(axes.c2p(y_bis_mirr_x, y_bis_mirr_y)).set_color(YELLOW)

        pt3 = Dot(axes.c2p((c-a)*b/d + a, 0)).set_color(PURPLE)




        x = np.array([[d/(a-c),1] , [np.tan(ANGLE), -1]])
        y = np.array([a*d/(a-c)-b,0]).transpose()
        pt4_coords = np.dot(np.linalg.inv(x), y)

        pt4 = Dot(axes.c2p(pt4_coords[0], pt4_coords[1])).set_color(PURPLE)

        

        self.play(Write(pt1), Write(pt2))

        l1 = Line(start = pt1.get_arc_center(), end = pt2.get_arc_center()).set_color(YELLOW)
        self.play(Write(l1))

        self.play(Write(pt3), Write(pt4))


        optimal_triangle = Polygram([pt3.get_arc_center(), pt.get_arc_center(), pt4.get_arc_center()]).set_color(PURPLE)
        self.play(Create(optimal_triangle))

        optimal_perimeter = np.linalg.norm(pt3.get_arc_center() - pt.get_arc_center()) + np.linalg.norm(pt4.get_arc_center() - pt.get_arc_center()) + np.linalg.norm(pt3.get_arc_center() - pt4.get_arc_center())
        optimal_line = Line(start = [0, 0, 0], end = [0, optimal_perimeter, 0]).set_color(PURPLE)


        optimal_line.move_to(line_group).shift(LEFT)

        self.play(TransformFromCopy(optimal_triangle, optimal_line, run_time = 3))

        line_top = DashedLine(start = optimal_line.get_start(), end = optimal_line.get_start() + 1.5*RIGHT) #need to change this number if more added to line_group
        line_bottom = DashedLine(start = optimal_line.get_end(), end = optimal_line.get_end() + 1.5*RIGHT)

        self.play(
            Write(line_top),
            Write(line_bottom)
        )

        self.play(FadeOut(line_group), FadeOut(line_top), FadeOut(line_bottom))
        self.wait()

        self.play(FadeOut(optimal_line))

        tick_marks = VGroup() # make a group of tick marks here indicating equality of sides

        reflecting_triangle = Polygram([pt4.get_center(), pt.get_center(), axes.c2p(c,d)], color = BLUE, fill_opacity = 0.5)
        self.play(Write(reflecting_triangle))
        

        reflected_triangle = Polygram([pt4.get_center(), axes.c2p(y_bis_mirr_x, y_bis_mirr_y), axes.c2p(c,d)], color = BLUE, fill_opacity = 0.5)
        self.play(Transform(reflecting_triangle, reflected_triangle))
        self.wait()
        self.play(FadeOut(reflecting_triangle))
        self.remove(reflected_triangle)

        # show thereby implied coungruencies



# some way to move the entire picture and center it (add background rectangle, move as a VGroup?)

        self.wait()
