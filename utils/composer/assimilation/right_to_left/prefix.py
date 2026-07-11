from schemas.latin.preposition import Preposition
from schemas.latin.verb import (
    VerbIrregularPerfectParticipleStem, 
    VerbIrregularPresentInfinitiveStem
)
from utils.composer.rule import Rule
from utils.misc import autoclone


def assimilate_ab(prefix, stem):
    rules = [
        (("a", "e", "i", "o", "u", "h"), lambda p: p[:-1]),
        (("c", "d", "f", "g", "n", "q", "s", "t", "v"), lambda p: p[:-1] + "n"),
        (("l"), lambda p: p[:-1] + "l"),
        (("r"), lambda p: p[:-1] + "r")
    ]

    for condition, transform in rules:
        if stem.orth.startswith(condition):
            prefix.orth = transform(prefix.orth)
            return [prefix]

    return []


def assimilate_ad(prefix, stem):
    rules = [
        (("c", "f", "g", "l", "n", "p", "r", "s", "t"), lambda p, s: p[:-1] + s[0]),
        (("q"), lambda p, s: p[:-1] + "c"),
        (("t"), lambda p, s: p[:-1] + "s"),
        (("m"), lambda p, s: p[:-1]),
    ]

    for condition, transform in rules:
        if stem.orth.startswith(condition):
            prefix.orth = transform(prefix.orth, stem.orth)
            return [prefix]
        
    if isinstance(stem, VerbIrregularPresentInfinitiveStem) or isinstance(stem, VerbIrregularPerfectParticipleStem):
        prefix.orth = prefix.orth[:-1] + "u"
        return [prefix]
    
    return []


def assimilate_com(prefix, stem):
    rules = [
        (("a", "e", "i", "o", "u", "h"), lambda p: p[:-1]),
        (("c", "d", "f", "g", "n", "q", "s", "t", "v"), lambda p: p[:-1] + "n"),
        (("l"), lambda p: p[:-1] + "l"),
        (("r"), lambda p: p[:-1] + "r")
    ]

    for condition, transform in rules:
        if stem.orth.startswith(condition):
            prefix.orth = transform(prefix.orth)
            return [prefix]
        
    return []


def assimilate_dis(prefix, stem):
    rules = [
        (("r", "g", "l", "v", "m", "n"), lambda p, s: p[:-1]),
        (("f"), lambda p, s: p[:-1] + s[0])
    ]

    for condition, transform in rules:
        if stem.orth.startswith(condition):
            prefix.orth = transform(prefix.orth, stem.orth)
            return [prefix]
        
    return []


def assimilate_ex(prefix, stem):
    rules = [
        (("c", "f"), lambda p, s: p[:-1] + s[0])
    ]

    # TODO: find out more
    for condition, transform in rules:
        if stem.orth.startswith(condition):
            prefix.orth = transform(prefix.orth, stem.orth)
            return [prefix]
        
    return []


def assimilate_in(prefix, stem):
    rules = [
        (("b", "m", "p"), lambda p, s: p[:-1] + "m"),
        (("l", "r"), lambda p, s: p[:-1] + s[0])
    ]
    
    for condition, transform in rules:
        if stem.orth.startswith(condition):
            prefix.orth = transform(prefix.orth, stem.orth)
            return [prefix]
        
    return []


def assimilate_sub(prefix, stem):
    #TODO: find out more (i.e. sus)

    rules = [
        (("c", "f", "g", "l", "r"), lambda p, s: p[:-1] + s[0]),
        (("t"), lambda p, s: p[:-1] + "s")
    ]

    for condition, transform in rules:
        if stem.orth.startswith(condition):
            prefix.orth = transform(prefix.orth, stem.orth)
            return [prefix]

    other_prefixes = []
    if stem.orth.startswith(("p")):
        for connecting_letter in ["p", "s"]:
            other_prefix = autoclone(prefix)
            other_prefix.radical = autoclone(prefix.radical)
            other_prefix.orth = prefix.orth[:len(prefix.orth) - 1] + connecting_letter
            other_prefixes.append(other_prefix)
        return [prefix] + other_prefixes
    
    return []


def assimilate_re(prefix, stem):
    rules = [
        (("a", "e", "i", "o", "u"), lambda p: p + "d")
    ]

    for condition, transform in rules:
        if stem.orth.startswith(condition):
            prefix.orth = transform(prefix.orth)
            return [prefix]
        
    return []


def assimilate_ob(prefix, stem):
    rules = [
        (("c", "f", "p"), lambda p, s: p[:-1] + s[0])
    ]

    for condition, transform in rules:
        if stem.orth.startswith(condition):
            prefix.orth = transform(prefix.orth, stem.orth)
            return [prefix]
        
    return []


def assimilate_trans(prefix, stem):
    rules = [
        (("s", "c", "d", "v"), lambda p: p[:-2])
    ]
    
    for condition, transform in rules:
        if stem.orth.startswith(condition):
            prefix.orth = transform(prefix.orth)
            return [prefix]
        
    return []


class PrefixAssimilationRule(Rule):
    _RULES = {
        "ab": assimilate_ab,
        "ad": assimilate_ad,
        "com": assimilate_com,
        "dis": assimilate_dis,
        "ex": assimilate_ex,
        "in": assimilate_in,
        "sub": assimilate_sub,
        "re": assimilate_re,
        "ob": assimilate_ob,
        "trans": assimilate_trans
    }

    def matches(self, left, right):
        return isinstance(left, Preposition) and left.orth in self._RULES

    def apply(self, left, right):
        cloned_left = autoclone(left)
        cloned_left.radical = autoclone(left.radical)
        cloned_right = autoclone(right)
        cloned_right.radical = autoclone(right.radical)

        transform = self._RULES.get(cloned_left.orth)
        if transform:
            return [
                (assimilated_prefix, cloned_right)
                for assimilated_prefix in transform(cloned_left, cloned_right)
            ]
