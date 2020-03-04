import re
import pytest
import numpy as np
import discretisedfield as df
import micromagneticmodel as mm
from .checks import check_term


class TestMagnetoElastic:
    def setup(self):
        mesh = df.Mesh(p1=(0, 0, 0), p2=(5, 5, 5), cell=(1, 1, 1))
        B1field = df.Field(mesh, dim=1, value=5e6)
        B2field = df.Field(mesh, dim=1, value=7e6)
        efield = df.Field(mesh, dim=6, value=(1, 0, 0, 1, 1, 1))

        self.valid_args = [(1, 1, (0, 1, 0, 2, 3, 7)),
                           (2e6, 3e6, (1e6, 1, 0.1, 2, 3, 7)),
                           (7e6, -2e-6, (0, 1e-8, 0, 2, 3.14, 7)),
                           (B1field, B2field, efield)]
        self.invalid_args = [((0, 1), 1, (0, 1, 0, 2, 3, 7)),
                             (2e6, '5', (1e6, 1, 0.1, 2, 3, 7)),
                             (7e6, -2e-6, (0, 1e-8, 3.14, 7)),
                             (7e6, -2e-6, 5)]

    def test_init_valid_args(self):
        for B1, B2, e in self.valid_args:
            term = mm.MagnetoElastic(B1=B1, B2=B2, e=e)
            check_term(term)
            assert hasattr(term, 'B1')
            assert hasattr(term, 'B2')
            assert hasattr(term, 'e')
            assert term.name == 'magnetoelastic'
            assert re.search(r'^MagnetoElastic\(B1=.+, B2=.+, e=.+\)$',
                             repr(term))

    def test_init_invalid_args(self):
        for B1, B2, e in self.invalid_args:
            with pytest.raises((TypeError, ValueError)):
                term = mm.MagnetoElastic(B1=B1, B2=B2, e=e)

        with pytest.raises(AttributeError):
            term = mm.MagnetoElastic(wrong=1)
