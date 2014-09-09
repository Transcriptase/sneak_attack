__author__ = 'rwill127'

import random as r
import matplotlib.pyplot as pp


class Attack(object):
    def __init__(self):
        self.mh_die = 6
        self.oh_die = 4
        self.sa_dice = 1
        self.abi = 3
        self.prof = 2
        self.target_ac = 14

        self.sa_used = False
        self.mh_hit = False
        self.oh_hit = False
        self.dmg = 0

        self.roll = 0

    def hit_roll(self):
        self.roll = r.randint(1, 20)

    def crit_check(self):
        return(self.roll == 20)

    def hit_check(self):
        return(self.roll + self.abi + self.prof >= self.target_ac)

    def wpn_dmg(self, wpn_die):
        dmg = r.randint(1, wpn_die)
        if self.crit_check():
            dmg += r.randint(1, wpn_die)
        return dmg

    def sa_dmg(self):
        dmg = 0
        dice = self.sa_dice
        if self.crit_check():
            dice  = 2 * self.sa_dice
        for i in xrange(dice):
            dmg += r.randint(1,6)
        return dmg

    def sa_check(self):
        if not self.sa_used:
            self.dmg += self.sa_dmg()
            self.sa_used = True

    def mh_atk(self):
        self.hit_roll()
        if self.crit_check() or self.hit_check():
            self.mh_hit = True
            self.dmg += self.wpn_dmg(self.mh_die) + self.abi
            self.sa_check()

    def oh_atk(self):
        self.hit_roll()
        if self.crit_check() or self.hit_check():
            self.oh_hit = True
            self.dmg += self.wpn_dmg(self.oh_die)
            self.sa_check()

    def reset(self):
        self.dmg = 0
        self.sa_used =False
        self.mh_hit = False
        self.oh_hit = False

    def mh_only(self):
        #Main hand attack only
        self.reset()
        self.mh_atk()

    def always_both(self):
        #Always MH and OH
        self.reset()
        self.mh_atk()
        self.oh_atk()

    def oh_on_mh_miss(self):
        #OH only when MH misses
        self.reset()
        self.mh_atk()
        if not self.mh_hit:
            self.oh_atk()

if __name__ == "__main__":
    n_trials = 10000

    a = Attack()

    def mean(nums):
        return(sum(nums)/float(len(nums)))

    def generate(attack, method):
        results = []
        for i in xrange(n_trials):
            method()
            results.append(attack.dmg)
        return results

    plan_names = ("Main Hand Only",
                  "Always Both",
                  "OH on Miss")

    plans = (a.mh_only,
             a.always_both,
             a.oh_on_mh_miss)

    def multitest(plan_dict):
        results = {}
        for name, plan in plan_dict:
            results[name] = generate(a, plan)
        return results

    def find_max(result_dict):
        max_dmg = 0
        for result in result_dict.values():
            if max(result) > max_dmg:
                max_dmg = max(result)
        return max_dmg


    def multiresult_plot(result_dict):
        n, bins, patches = pp.hist(result_dict.values(),
                                   bins=find_max(result_dict),
                                   histtype="step",
                                   label=result_dict.keys())
        pp.legend()
        pp.show()

    results = multitest(zip(plan_names, plans))
    multiresult_plot(results)

    all_results = {}
    acs = xrange(13, 21)
    for ac in acs:
        a.target_ac = ac
        all_results[ac] = multitest(zip(plan_names,plans))

    mh_only_summary = []
    both_always_summary = []
    oh_on_miss_summary = []
    for ac, results in all_results.iteritems():
        mh_only_summary.append(mean(results["Main Hand Only"]))
        both_always_summary.append(mean(results["Always Both"]))
        oh_on_miss_summary.append(mean(results["OH on Miss"]))

    pp.plot(acs, mh_only_summary, acs, oh_on_miss_summary, acs, both_always_summary)
    pp.show()
    
    both_ratio = []
    for i,j in zip(oh_on_miss_summary, both_always_summary):
        both_ratio.append(i/j)

    mh_ratio = []
    for i,j in zip(oh_on_miss_summary, mh_only_summary):
        mh_ratio.append(i/j)


