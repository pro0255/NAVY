
import turtle


SIZE = 20


#? https://fedimser.github.io/l-systems.html

class LSystem():
    def __init__(self, axiom, rule, angle, num):
        self.angle = angle
        self.rule = rule
        self.axiom = axiom
        self.num = num
        self.resolved = None
        self.resolve_axiom_deps_rule()
        self.stack = []

    def resolve_axiom_deps_rule(self):
        c = 0
        res = self.axiom
        while(c < self.num):
            res = res.replace('F', self.rule)
            c += 1
        self.resolved = res


    def create_rule(self, rule):
        i = rule.index('>')
        i_start_rule = i + 2
        left_side = rule[0:i-2]
        right_side = rule[i_start_rule:len(rule)]
        return left_side, right_side


    def draw(self):
        t = turtle.Turtle()
        c = 0
        size = len(self.resolved)
        while(c < size):
            current = self.resolved[c]
            if current == 'F':
                t.forward(SIZE)
            if current == '+':
                t.left(self.angle)
            if current == '-':
                t.right(self.angle)
            if current == '[':
                self.stack.append((t.position(), t.heading()))
            if current == ']':
                state = self.stack.pop()
                pos, head = state
                t.setposition(pos)
                t.setheading(head)
            c+=1
        input('Exit..')

