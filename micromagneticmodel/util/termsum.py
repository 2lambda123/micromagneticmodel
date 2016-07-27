import six
import abc


@six.add_metaclass(abc.ABCMeta)
class TermSum(object):
    def __init__(self):
        self.terms = []

    @abc.abstractmethod
    def add(self, term): pass

    @abc.abstractmethod
    def _lefthandside(self): pass

    @property
    def latex_str(self):
        s = self._lefthandside

        for term in self.terms:
            if term._latex_str[1] != "-" and s[-1] != "=":
                s += "+"
            s += term._latex_str[1:-1]

        if self.terms == []:
            s += "0"
        s += "$"

        return s

    @property
    def _repr_str(self):
        terms_repr = [term._repr_str for term in self.terms]
        return " + ".join(terms_repr)

    def _repr_latex_(self):
        return self.latex_str
    
    def __iadd__(self, other):
        self.add(other)
        return self

    def calculator_script(self):
        script = ''
        for term in self.terms:
            script += term.calculator_script()

        return script

    def __repr__(self):
        return self._repr_str
