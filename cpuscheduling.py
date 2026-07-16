import os

# ─────────────────────────────────────────────
#  CPU Process Scheduling Simulator
#  Algorithms: FCFS, SJF, RR
# ─────────────────────────────────────────────

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    print("=" * 60)
    print("       CPU PROCESS SCHEDULING SIMULATOR")
    print("       OS Lab Project — Python")
    print("=" * 60)

def get_processes():
    processes = []
    n = int(input("\nEnter number of processes: "))
    print()
    for i in range(n):
        pid = f"P{i+1}"
        at  = int(input(f"  {pid} — Arrival Time : "))
        bt  = int(input(f"  {pid} — Burst Time   : "))
        processes.append({"pid": pid, "at": at, "bt": bt})
        print()
    return processes

def print_gantt(gantt):
    print("\n  Gantt Chart:")
    print("  ", end="")
    for seg in gantt:
        width = seg["end"] - seg["start"]
        print(f"| {seg['pid']:^{max(3, width*2-1)}} ", end="")
    print("|")

    print("  ", end="")
    for seg in gantt:
        width = seg["end"] - seg["start"]
        print(f"{seg['start']:<{max(3, width*2+1)}}", end="")
    print(gantt[-1]["end"])

def print_results(results, algo_name):
    print(f"\n  Results — {algo_name}")
    print("  " + "-" * 56)
    print(f"  {'PID':<6} {'AT':<6} {'BT':<6} {'CT':<6} {'TAT':<8} {'WT':<8}")
    print("  " + "-" * 56)
    total_tat = total_wt = 0
    for r in results:
        print(f"  {r['pid']:<6} {r['at']:<6} {r['bt']:<6} {r['ct']:<6} {r['tat']:<8} {r['wt']:<8}")
        total_tat += r["tat"]
        total_wt  += r["wt"]
    print("  " + "-" * 56)
    n = len(results)
    print(f"  Average Turnaround Time : {total_tat/n:.2f}")
    print(f"  Average Waiting Time    : {total_wt/n:.2f}")

def calc_stats(procs, gantt):
    results = []
    for p in procs:
        segs = [s for s in gantt if s["pid"] == p["pid"]]
        ct  = segs[-1]["end"] if segs else 0
        tat = ct - p["at"]
        wt  = tat - p["bt"]
        results.append({**p, "ct": ct, "tat": tat, "wt": wt})
    return results

# ── FCFS ──────────────────────────────────────
def fcfs(procs):
    procs = sorted(procs, key=lambda x: x["at"])
    t, gantt = 0, []
    for p in procs:
        t = max(t, p["at"])
        gantt.append({"pid": p["pid"], "start": t, "end": t + p["bt"]})
        t += p["bt"]
    return gantt

# ── SJF (Non-Preemptive) ──────────────────────
def sjf(procs):
    procs = [p.copy() for p in procs]
    t, gantt, done = 0, [], set()
    while len(done) < len(procs):
        avail = [p for p in procs if p["pid"] not in done and p["at"] <= t]
        if not avail:
            t = min(p["at"] for p in procs if p["pid"] not in done)
            continue
        p = min(avail, key=lambda x: x["bt"])
        gantt.append({"pid": p["pid"], "start": t, "end": t + p["bt"]})
        t += p["bt"]
        done.add(p["pid"])
    return gantt

# ── Round Robin ───────────────────────────────
def round_robin(procs, quantum):
    procs   = sorted(procs, key=lambda x: x["at"])
    rem     = {p["pid"]: p["bt"] for p in procs}
    t       = 0
    gantt   = []
    queue   = []
    arrived = set()
    idx     = 0
    n       = len(procs)
    done    = set()

    while len(done) < n:
        while idx < n and procs[idx]["at"] <= t:
            if procs[idx]["pid"] not in arrived:
                queue.append(procs[idx]["pid"])
                arrived.add(procs[idx]["pid"])
            idx += 1

        if not queue:
            if idx < n:
                t = procs[idx]["at"]
            continue

        pid = queue.pop(0)
        run = min(quantum, rem[pid])
        gantt.append({"pid": pid, "start": t, "end": t + run})
        t += run
        rem[pid] -= run

        while idx < n and procs[idx]["at"] <= t:
            if procs[idx]["pid"] not in arrived:
                queue.append(procs[idx]["pid"])
                arrived.add(procs[idx]["pid"])
            idx += 1

        if rem[pid] > 0:
            queue.append(pid)
        else:
            done.add(pid)

    return gantt

# ── CPU Utilization ───────────────────────────
def cpu_utilization(gantt):
    busy = sum(s["end"] - s["start"] for s in gantt)
    total = gantt[-1]["end"]
    return (busy / total) * 100

# ── Main Menu ─────────────────────────────────
def main():
    while True:
        clear()
        print_header()
        print("""
  Select Algorithm:

    1. FCFS — First Come First Serve
    2. SJF  — Shortest Job First (Non-Preemptive)
    3. RR   — Round Robin
    4. Compare — Run ALL 3 algorithms on same input
    0. Exit
""")
        choice = input("  Enter choice: ").strip()

        if choice == "0":
            print("\n  Goodbye!\n")
            break

        if choice not in ("1","2","3","4"):
            input("\n  Invalid choice. Press Enter...")
            continue

        clear()
        print_header()
        procs = get_processes()

        quantum = 2
        if choice in ("3", "4"):
            quantum = int(input("  Time Quantum (for Round Robin): "))

        clear()
        print_header()

        def run_and_show(gantt, procs, name):
            results = calc_stats(procs, gantt)
            print(f"\n{'─'*60}")
            print(f"  Algorithm : {name}")
            print(f"{'─'*60}")
            print_gantt(gantt)
            print_results(results, name)
            util = cpu_utilization(gantt)
            print(f"\n  CPU Utilization : {util:.1f}%")

        if choice == "1":
            run_and_show(fcfs(procs), procs, "FCFS — First Come First Serve")
        elif choice == "2":
            run_and_show(sjf(procs), procs, "SJF — Shortest Job First")
        elif choice == "3":
            run_and_show(round_robin(procs, quantum), procs, f"Round Robin (Quantum={quantum})")
        elif choice == "4":
            algos = [
                (fcfs(procs),                "FCFS"),
                (sjf(procs),                 "SJF"),
                (round_robin(procs, quantum), f"Round Robin (Q={quantum})"),
            ]
            for gantt, name in algos:
                run_and_show(gantt, procs, name)

        input("\n\n  Press Enter to go back to menu...")

if __name__ == "__main__":
    main()