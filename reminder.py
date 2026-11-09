"""Desktop reminder: show a notification at a given time or after a delay.

Uses a native Windows toast (win10toast) when available, falls back to
plyer on macOS/Linux, and finally to a console message with a beep.

Examples:
    python reminder.py --at 21:30 --message "Stand up and stretch"
    python reminder.py --in 25 --message "Pomodoro done" --repeat 4
"""

from __future__ import annotations

import argparse
import datetime as dt
import sys
import time


def notify(title: str, message: str) -> None:
    """Show a desktop notification using the best backend available."""
    try:
        from win10toast import ToastNotifier  # Windows only

        ToastNotifier().show_toast(title, message, duration=10, threaded=False)
        return
    except Exception:  # noqa: BLE001 - backend missing or failed, try the next one
        pass
    try:
        from plyer import notification  # cross-platform

        notification.notify(title=title, message=message, timeout=10)
        return
    except Exception:  # noqa: BLE001
        pass
    print(f"\a[{dt.datetime.now():%H:%M:%S}] {title}: {message}", flush=True)


def seconds_until(clock_time: str, now: dt.datetime | None = None) -> float:
    """Seconds from ``now`` until the next occurrence of ``HH:MM`` (or ``HH:MM:SS``)."""
    now = now or dt.datetime.now()
    fmt = "%H:%M:%S" if clock_time.count(":") == 2 else "%H:%M"
    target_time = dt.datetime.strptime(clock_time, fmt).time()
    target = dt.datetime.combine(now.date(), target_time)
    if target <= now:
        target += dt.timedelta(days=1)
    return (target - now).total_seconds()


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Show a desktop reminder.")
    when = parser.add_mutually_exclusive_group(required=True)
    when.add_argument("--at", metavar="HH:MM", help="clock time for the reminder")
    when.add_argument("--in", dest="minutes", type=float, metavar="MIN", help="minutes from now")
    parser.add_argument("--message", "-m", default="Time's up!", help="reminder text")
    parser.add_argument("--title", default="Reminder", help="notification title")
    parser.add_argument(
        "--repeat", type=int, default=1, help="with --in: repeat N times (e.g. Pomodoro)"
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        for i in range(args.repeat if args.minutes is not None else 1):
            delay = args.minutes * 60 if args.minutes is not None else seconds_until(args.at)
            due = dt.datetime.now() + dt.timedelta(seconds=delay)
            print(f"Reminder {i + 1} set for {due:%Y-%m-%d %H:%M:%S}. Press Ctrl+C to cancel.")
            time.sleep(delay)
            notify(args.title, args.message)
    except KeyboardInterrupt:
        print("\nCancelled.")
        return 130
    except ValueError as exc:
        print(f"Invalid time: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
