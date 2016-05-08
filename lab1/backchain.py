from production import AND, OR, NOT, PASS, FAIL, IF, THEN, RuleExpression, \
     match, populate, simplify, variables
from zookeeper import ZOOKEEPER_RULES

# This function, which you need to write, takes in a hypothesis
# that can be determined using a set of rules, and outputs a goal
# tree of which statements it would need to test to prove that
# hypothesis. Refer to the problem set (section 2) for more
# detailed specifications and examples.

# Note that this function is supposed to be a general
# backchainer.  You should not hard-code anything that is
# specific to a particular rule set.  The backchainer will be
# tested on things other than ZOOKEEPER_RULES.

def expand_subtree(subtree, bindings, rules):
    # build an identical subtree by recursively
    # walking and replacing each leaf with a backchained
    # tree

    cloned_node = subtree.__class__()
    for expression in subtree:
        if isinstance(expression, RuleExpression):
            cloned_node.append( expand_subtree(expression, bindings) )
        else:
            # assume if it's not a RuleExpression, it's a leaf node
            hypothesis = populate(expression, bindings)
            cloned_node.append( backchain_to_goal_tree(rules, hypothesis) )

    return simplify( cloned_node )



def backchain_to_goal_tree(rules, hypothesis):
    # check rules for matching consequents
    #   i) no matches -> hypothesis is a leaf
    #   ii) matches -> OR(antecedent)

    or_cond = OR()

    # always append the hypothesis
    or_cond.append(hypothesis)

    for rule in rules:
        bindings = match(rule.consequent()[0], hypothesis)
        if bindings:
            # append the goal tree from the antecedent
            ante = rule.antecedent()
            if isinstance(ante, RuleExpression):
                or_cond.append( expand_subtree(ante, bindings, rules) )

    return simplify( or_cond )

# Here's an example of running the  backward chainer - uncomment
# it to see it work:
res = backchain_to_goal_tree(ZOOKEEPER_RULES, 'opus is a penguin')
print res
