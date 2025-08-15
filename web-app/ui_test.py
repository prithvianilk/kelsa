from time_util import SECONDS_IN_A_DAY, SECONDS_IN_AN_HOUR, SECONDS_IN_A_MINUTE
from ui import pretty_print_work_done

def test_pretty_print_work_done():
    assert pretty_print_work_done(0) == "0m"
    assert pretty_print_work_done(SECONDS_IN_A_MINUTE) == "1m"
    assert pretty_print_work_done(5 * SECONDS_IN_A_MINUTE) == "5m"
    assert pretty_print_work_done(59 * SECONDS_IN_A_MINUTE) == "59m"
    assert pretty_print_work_done(SECONDS_IN_AN_HOUR) == "1h 0m"
    assert pretty_print_work_done(SECONDS_IN_AN_HOUR + SECONDS_IN_A_MINUTE) == "1h 1m"
    assert pretty_print_work_done(SECONDS_IN_AN_HOUR + (59 * SECONDS_IN_A_MINUTE)) == "1h 59m"
    assert pretty_print_work_done(SECONDS_IN_A_DAY) == "1d 0h"
    assert pretty_print_work_done(SECONDS_IN_A_DAY + SECONDS_IN_AN_HOUR) == "1d 1h"
    assert pretty_print_work_done(SECONDS_IN_A_DAY + SECONDS_IN_AN_HOUR + SECONDS_IN_A_MINUTE) == "1d 1h"
    assert pretty_print_work_done(SECONDS_IN_A_DAY + (23 * SECONDS_IN_AN_HOUR)) == "1d 23h"
    assert pretty_print_work_done(2 * SECONDS_IN_A_DAY) == "2d 0h"