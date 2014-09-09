__author__ = 'rwill127'
from nose.tools import *
import sneak_attack as sa

class TestAttack(object):
    def setup(self):
        self.a = sa.Attack()

    def test_mh(self):
        self.a.mh_only()

    def test_both(self):
        self.a.always_both()

    def test_conditional(self):
        self.a.oh_on_mh_miss()