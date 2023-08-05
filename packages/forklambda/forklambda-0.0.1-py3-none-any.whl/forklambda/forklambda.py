
class forklambda(object):
    def __init__(self, variables, expr_s: str, env={}):
        if type(variables) == list:
            self.variables = variables
        else:
            # get rid of spaces
            variables = variables.replace(' ', '')
            if ',' in variables:
                self.variables = variables.split(',')
            else:
                self.variables = [variables]
        self.expr_s = expr_s
        self.env = env

    def __repr__(self):
        return  '{} {}: {} with {}'.format('λ', ','.join(self.variables), self.expr_s, self.env)

    def __call__(self, *args, **kwargs):
        env_ext = self.env.copy()
        if args:
            for k, v in zip(self.variables[:len(args)], args):
                env_ext[k] = v

        if kwargs:
            for k, v in kwargs.items():
                env_ext[k] = v

        variables = list(filter(lambda name: name not in env_ext.keys(), self.variables))

        if not variables:
            return eval(self.expr_s, globals(), env_ext)
        else:
            return forklambda(variables, self.expr_s, env_ext)


if __name__ == "__main__":
    # demo 1
    print('Demo 1')
    fl = forklambda(['a', 'b', 'c'], 'a + 2 * b + 3 * c')
    print(fl(1)(2)(3))
    print(fl(1, 2, 3))
    print(fl(1, c=3, b=2))
    print(fl(c=3)(1, 2))

    # demo 2
    print('Demo 2')
    fl = forklambda('x, y, f', 'f(x) * y')
    print(fl(f=forklambda('x', '3*x'))(2))


