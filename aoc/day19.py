import operator
import re


class UnconditionalRule:
    def __call__(self, value):
        return True


class ConditionalRule:
    def __init__(self, field, comparison, against):
        self.field = field
        self.threshold = int(against)
        match comparison:
            case "<":
                self.op = operator.lt
            case ">":
                self.op = operator.gt
            case _:
                raise ValueError

    def __repr__(self):
        return f"{self.field}{self.op}{self.threshold}"

    def __call__(self, part):
        return self.op(part[self.field], self.threshold)


def parse_workflows(data):
    for line in data.splitlines():
        name, rule_strings = line[:-1].split("{")
        rules = []
        for rule_string in rule_strings.split(","):
            match = re.fullmatch(r"(x|m|a|s)(\<|\>)(\d+)\:(\w+)", rule_string)
            if not match:
                rules.append((UnconditionalRule(), rule_string))
            else:
                rules.append((ConditionalRule(match[1], match[2], match[3]), match[4]))
        yield name, rules


def parse_parts(data):
    for line in data.splitlines():
        part = {}
        for match in re.finditer(r"(x|m|a|s)=(\d+)", line):
            part[match[1]] = int(match[2])
        yield part


def run(data):
    #data = DATA
    workflow_data, part_data = data.split("\n\n")

    workflows = {name: rules for name, rules in parse_workflows(workflow_data)}
    parts = list(parse_parts(part_data))

    total = 0
    for part in parts:
        target = "in"
        while target != "A" and target != "R":
            for rule, target in workflows[target]:
                if rule(part):
                    break
        if target == "A":
            total += sum(part.values())

    return total, 0

DATA = """\
px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}"""
