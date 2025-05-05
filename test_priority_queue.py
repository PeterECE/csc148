"""Assignment 1 - Tests for class PriorityQueue  (Task 3a)

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

All of the files in this directory are
Copyright (c) Jonathan Calver, Diane Horton, Sophia Huynh, Joonho Kim and
Jacqueline Smith.

Module Description:
This module will contain tests for class PriorityQueue.
"""
from container import PriorityQueue

# TODO: Put your pytest test functions for class PriorityQueue here

class TestPriorityQueue:
    def test_remove(self):
        pq = PriorityQueue()
        pq.add('fred')
        assert pq.remove() == 'fred'
        assert pq.is_empty() == True

    def test_is_empty(self):
        pq = PriorityQueue()
        assert pq.is_empty() == True
        pq.add('fred')
        assert pq.is_empty() == False
        assert pq.remove()
        assert pq.is_empty() == True

    def test_add(self):
        pq = PriorityQueue()
        pq.add('sophia')
        pq.add('fred')
        pq.add('anna')
        pq.add('anna')
        pq.add('fred')
        pq.add('mona')
        assert pq.remove() == 'anna'
        assert pq.remove() == 'anna'
        assert pq.remove() == 'fred'
        assert pq.remove() == 'fred'
        assert pq.remove() == 'mona'
        assert pq.remove() == 'sophia'
        assert pq.is_empty() == True

if __name__ == '__main__':
    import pytest

    pytest.main(['test_priority_queue.py'])
