import datetime as dt

import pytest

import reminder


def test_seconds_until_later_today():
    now = dt.datetime(2024, 1, 1, 10, 0, 0)
    assert reminder.seconds_until("10:30", now) == 30 * 60


def test_seconds_until_rolls_over_to_tomorrow():
    now = dt.datetime(2024, 1, 1, 23, 0, 0)
    assert reminder.seconds_until("01:00", now) == 2 * 3600


def test_seconds_until_accepts_seconds():
    now = dt.datetime(2024, 1, 1, 12, 0, 0)
    assert reminder.seconds_until("12:00:15", now) == 15


def test_invalid_time_raises():
    with pytest.raises(ValueError):
        reminder.seconds_until("25:99")


def test_main_with_delay_calls_notify(monkeypatch):
    calls = []
    monkeypatch.setattr(reminder.time, "sleep", lambda s: None)
    monkeypatch.setattr(reminder, "notify", lambda t, m: calls.append((t, m)))
    assert reminder.main(["--in", "0.01", "-m", "hi", "--repeat", "3"]) == 0
    assert calls == [("Reminder", "hi")] * 3
