
import turtle

class LSystem():
    def __init__(self, axiom, rule, angle, num):
        self.angle = angle
        self.rule = rule
        self.axiom = axiom
        self.num = num
        self.resolve_axiom_deps_rule()

    def resolve_axiom_deps_rule(self):
        c = 0
        res = self.axiom
        while(c < self.num):
            res = res.replace('F', self.rule)
            c += 1
        print(res)



    def draw(self):
        t = turtle.Turtle()
        c = 0
        while(c < 3):
            t.forward(50)
            c+=1
        


        input('Exit..')

