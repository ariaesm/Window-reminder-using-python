# Desktop Reminder (Python)

A tiny command-line tool that pops up a desktop notification at a set time or after a delay — handy for breaks, meetings or Pomodoro sessions.

## Features

- Remind at a clock time (`--at 21:30`) or after a delay (`--in 25`)
- Repeat mode for Pomodoro-style cycles (`--repeat 4`)
- Native toast on Windows, `plyer` notifications on macOS/Linux, and a console + beep fallback when neither is installed
- No required dependencies; unit-tested

## Usage

```bash
# at a specific time (rolls over to tomorrow if the time has passed)
python reminder.py --at 21:30 --message "Stand up and stretch"

# four 25-minute Pomodoros
python reminder.py --in 25 --repeat 4 --title "Pomodoro" -m "Take a 5 minute break"
```

Optional, for native pop-ups:

```bash
pip install win10toast   # Windows
pip install plyer        # macOS / Linux
```

## Tests

```bash
pip install pytest
pytest
```

## License

[MIT](LICENSE)
