"""

AST elements of a DSL for describing cross-validation experiment protocols.

"""
import numpy as np

from .base import Task, Split

class Average(object):
    def __init__(self, values):
        self.values = values


class Score(object):
    def __init__(self, model, task):
        self.model = model
        self.task = task


class BestModel(object):
    def __init__(self, split):
        self.split = split


class MergeTasks(object):
    def __init__(self, *tasks):
        self.tasks = tasks


class RetrainClassifier(object):
    def __init__(self, model, task):
        self.model = model
        self.task = task


#
#
#

class Visitor(object):

    def evaluate(self, node, memo):
        if memo is None:
            memo = {}

        if id(node) not in memo:
            fname = 'on_' + node.__class__.__name__
            rval = getattr(self, fname)(node, memo)
            memo[node] = rval

        return memo[node]

    def on_Average(self, node, memo):
        return np.mean([self.evaluate(value, memo) for value in node.values])

    def on_Score(self, node, memo):
        model = self.evaluate(node.model, memo)
        task = self.evaluate(node.task, memo)
        raise NotImplementedError('implement me')

    def on_BestModel(self, node, memo):
        split = self.evaluate(node.split, memo)
        raise NotImplementedError('implement me')

    def on_Task(self, node, memo):
        return node

    def on_Split(self, node, memo):
        return node
