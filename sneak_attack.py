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


class Tester(object):
    def __init__(self, attack):
        self.n_trials = 10000
        self.a = attack
        self.plan_names = ("Main Hand Only",
                           "Always Both",
                           "OH on Miss")
        self.plans = (self.a.mh_only, self.a.always_both, self.a.oh_on_mh_miss)
        self.acs = xrange(13, 21)

    def mean(self, nums):
        return(sum(nums)/float(len(nums)))

    def generate(self, method):
        damages = []
        for i in xrange(self.n_trials):
            method()
            damages.append(self.a.dmg)
        return damages

    def multitest(self):
        results = {}
        for name, plan in zip(self.plan_names, self.plans):
            results[name] = self.generate(plan)
        return results

    def find_max(self, result_dict):
        max_dmg = 0
        for result in result_dict.values():
            if max(result) > max_dmg:
                max_dmg = max(result)
        return max_dmg

    def multiresult_plot(self, result_dict):
        n, bins, patches = pp.hist(result_dict.values(),
                                   bins=self.find_max(result_dict),
                                   histtype="step",
                                   label=result_dict.keys())
        pp.legend()
        pp.show()

    def ac_comparison(self):
        all_results = {}
        for ac in self.acs:
            self.a.target_ac = ac
            all_results[ac] = self.multitest()
        return all_results

    def summarize(self, results_dict):
        mh_only_summary = []
        both_always_summary = []
        oh_on_miss_summary = []
        for ac, results in results_dict.iteritems():
            mh_only_summary.append(self.mean(results["Main Hand Only"]))
            both_always_summary.append(self.mean(results["Always Both"]))
            oh_on_miss_summary.append(self.mean(results["OH on Miss"]))
        summary_pack = {}
        for name, summary in zip(self.plan_names, (mh_only_summary, both_always_summary, oh_on_miss_summary)):
            summary_pack[name] = summary
        return summary_pack

    def summary_plot(self, summary_pack):
        pp.plot(self.acs, summary_pack["Main Hand Only"],
                self.acs, summary_pack["OH on Miss"],
                self.acs, summary_pack["Always Both"])
        pp.show()

    def vector_ratio(self, num_vec, denom_vec):
        ratio_vec = []
        for i, j in zip(num_vec, denom_vec):
            ratio_vec.append(i/j)
        return ratio_vec

if __name__ == "__main__":
    a = Attack()
    t = Tester(a)
    results = t.multitest()
    t.multiresult_plot(results)
    all_results = t.ac_comparison()
    summary = t.summarize(all_results)
    t.summary_plot(summary)

    b = Attack()
    b.prof = 3
    b.sa_dice = 2
    t2 = Tester(b)
    t2.multiresult_plot(t2.multitest())
    all_results = t2.ac_comparison()
    summary = t2.summarize(all_results)
    t.summary_plot(summary)

    c = Attack()
    c.prof = 3
    c.abi = 4
    c.sa_dice = 4
    c.oh_die = 6
    t3 = Tester(c)
    t3.multiresult_plot(t3.multitest())
    all_results = t3.ac_comparison()
    t3.summary_plot(t3.summarize(all_results))