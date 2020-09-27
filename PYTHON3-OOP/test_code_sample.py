from code_sample import m_sort, results_, sum_, factorial, FlightStatusTracker
import datetime
from unittest.mock import Mock 
import pytest 
from unittest.mock import patch

def test_results_9():
    assert(results_(4,5) == 9)

def test_results_20():
    assert(results_(10,10) == 20)

def test_results_6():
    assert(results_(1,2,3) == 6)

def test_results_12():
    assert(results_(1,8,3) == 12)

def test_results_8():
    assert(results_(1,2,3,2) == 8)

def test_results_opps():
    assert(results_(1,2,3,4,6) == "oops")

def test_results_opps_2():
    assert(results_(1) == "oops")

#test for sums 
def test_sum_6():
    assert(sum_([1,2,3]) == 6)

def test_sum_0():
    assert(sum_([]) == 0)

def test_sum_10():
    assert(sum_([1,2,3,2,1,1]) == 10)

def test_sum_10():
    assert(sum_([10,918,128,35,52,41,81]) == 1265)


# test for factorical 
def test_factorial_10():
    assert(factorial(10) == 3628800)

def test_factorial_0():
    assert(factorial(0) == 1)

def test_factorial_5():
    assert(factorial(5) == 120)

# test for m_sort 
def test_m_sort_l1():
    assert(m_sort([1]) == [1])

def test_m_sort_l2():
    assert(m_sort([2,1]) == [1,2])

def test_m_sort_l3():
    assert(m_sort([5,4,8,50,0,9,11]) == [0,4,5,8,9,11,50])

def test_m_sort_l4():
    assert(m_sort([3,5,2,1,2]) == [1, 2, 2, 3, 5])



@pytest.fixture
def tracker():
    return FlightStatusTracker()


def test_mock_method(tracker):
    """
    Written using pytest syntax, asserts that the correct exception is raised when an inappropriate arg is passed in. 
    Additionally it creates a Mock object for the set method and makes sure that its never called. It i was, it means 
    there is a bug in our exception handling code. 
    """
    tracker.redis.set = Mock()
    fake_now = datetime.datetime(2015, 4 , 1) 
    with pytest.raises(ValueError) as ex:
        tracker.change_status("AC101", "lost")
    assert ex.value.args[0] == "LOST is not a valid status"
    assert tracker.redis.set.call_count == 0


def test_patch_1(tracker):
    tracker.redis.set = Mock() 
    fake_now = datetime.datetime(2015, 4, 1) 
    with patch("datetime.datetime") as dt:
        dt.now.return_value = fake_now
        tracker.change_status("AC102", "on time") 
    dt.now.assert_called_once_with()
    tracker.redis.set.assert_called_once_with("flightno:AC102", "2015-04-01T00:00:00|ON TIME")
    
