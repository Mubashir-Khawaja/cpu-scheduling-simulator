# CPU Process Scheduling Simulator

A menu-driven Python console application that simulates and compares three
fundamental CPU scheduling algorithms used in Operating Systems. Built as an
OS Lab project to demonstrate process scheduling behavior through Gantt charts
and performance metrics.

## Algorithms Implemented

| Algorithm | Type |
|---|---|
| FCFS (First Come First Serve) | Non-Preemptive |
| SJF (Shortest Job First) | Non-Preemptive |
| Round Robin | Preemptive (time-quantum based) |

## Features

- 📊 **Gantt Chart Visualization** — visual timeline of process execution
- 📈 **Performance Metrics** — Completion Time (CT), Turnaround Time (TAT), Waiting Time (WT) per process
- 📉 **Average TAT & WT** calculation across all processes
- ⚙️ **CPU Utilization %** calculation
- 🔄 **Compare Mode** — run all three algorithms on the same input for side-by-side comparison
- 🖥️ Clean, interactive menu-driven CLI (cross-platform screen clearing for Windows/Linux/Mac)

## Tech Stack

- **Language:** Python 3
- **Libraries:** `os` (standard library only — no external dependencies)

## How to Run

```bash
python scheduler.py
```

Then follow the on-screen menu:
1. Enter number of processes
2. Enter Arrival Time (AT) and Burst Time (BT) for each process
3. Select an algorithm (or "Compare" to run all three)
4. View the Gantt chart and performance table

## Sample Menu

```
1. FCFS — First Come First Serve
2. SJF  — Shortest Job First (Non-Preemptive)
3. RR   — Round Robin
4. Compare — Run ALL 3 algorithms on same input
0. Exit
```

## Project Structure

```
cpu-scheduling-simulator/
│
├── scheduler.py       # Main program
└── README.md          # Documentation
```

## Concepts Demonstrated

- Process scheduling fundamentals
- Gantt chart construction from execution segments
- Waiting Time & Turnaround Time calculation
- Queue-based scheduling logic (Round Robin)
- CPU utilization analysis

## Author

**Mubashir**
Computer Science Student

## License

This project is open source and available for educational use.
