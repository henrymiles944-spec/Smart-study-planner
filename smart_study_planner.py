"""
Smart Study Planner
--------------------
A console-based Python programme that helps a student log, review and
analyse their study sessions across different subjects over a semester.

All session data is stored in memory (as a list of dictionaries) while the
programme is running, and is saved to / reloaded from a plain text file
(study_log.txt) so that the data survives across multiple runs.

Author: Kalunda
"""

import os

# Name of the file used to persist study session data between runs.
DATA_FILE = "study_log.txt"

# The list of sessions is kept as a module-level list of dictionaries.
# Each dictionary has the keys: subject, topic, date, duration (minutes).
sessions = []


# ---------------------------------------------------------------------------
# c) classify_session(duration)
# ---------------------------------------------------------------------------
def classify_session(duration):
    """
    Classify a study session based on its duration (in minutes).

    Short  -> under 30 minutes
    Medium -> 30 to 90 minutes (inclusive)
    Long   -> over 90 minutes
    """
    if duration < 30:
        return "Short"
    elif duration <= 90:
        return "Medium"
    else:
        return "Long"


# ---------------------------------------------------------------------------
# b) add_session()
# ---------------------------------------------------------------------------
def add_session():
    """
    Prompt the user for the details of a new study session and add it to
    the sessions list. The duration is validated so that only a positive
    number is accepted; the user is re-prompted until a valid value is
    entered.
    """
    print("\n--- Add a New Study Session ---")
    subject = input("Enter subject name: ").strip()
    topic = input("Enter topic covered: ").strip()
    date = input("Enter date or day label (e.g. 2026-09-10 or 'Monday'): ").strip()

    # Keep asking until the user supplies a valid positive number for duration.
    duration = None
    while duration is None:
        raw_duration = input("Enter duration of session in minutes: ").strip()
        try:
            value = float(raw_duration)
            if value <= 0:
                print("Duration must be a positive number. Please try again.")
                continue
            duration = value
        except ValueError:
            print("Invalid input. Please enter a numeric value for duration.")

    # Store each session as a dictionary and append it to the list of sessions.
    session = {
        "subject": subject,
        "topic": topic,
        "date": date,
        "duration": duration,
    }
    sessions.append(session)
    print(f"Session added: {subject} ({classify_session(duration)}, {duration:.0f} min)")


# ---------------------------------------------------------------------------
# d) view_sessions()
# ---------------------------------------------------------------------------
def view_sessions():
    """
    Display every logged session in a neatly formatted table, showing the
    subject, topic, duration and its Short/Medium/Long classification.
    """
    print("\n--- All Study Sessions ---")
    if not sessions:
        print("No study sessions have been logged yet.")
        return

    header = f"{'No.':<4}{'Subject':<15}{'Topic':<20}{'Date':<15}{'Duration (min)':<16}{'Class':<8}"
    print(header)
    print("-" * len(header))
    for index, s in enumerate(sessions, start=1):
        classification = classify_session(s["duration"])
        print(
            f"{index:<4}{s['subject']:<15}{s['topic']:<20}{s['date']:<15}"
            f"{s['duration']:<16.0f}{classification:<8}"
        )


# ---------------------------------------------------------------------------
# e) search_by_subject(subject)
# ---------------------------------------------------------------------------
def search_by_subject(subject):
    """
    Display only the sessions recorded for the given subject (case-insensitive
    match), along with the total time spent on it. If no sessions are found,
    a clear message is displayed instead of an empty table.
    """
    matches = [s for s in sessions if s["subject"].lower() == subject.lower()]

    print(f"\n--- Sessions for Subject: {subject} ---")
    if not matches:
        print(f"No sessions found for subject '{subject}'.")
        return

    header = f"{'No.':<4}{'Topic':<20}{'Date':<15}{'Duration (min)':<16}{'Class':<8}"
    print(header)
    print("-" * len(header))
    total_minutes = 0
    for index, s in enumerate(matches, start=1):
        classification = classify_session(s["duration"])
        print(f"{index:<4}{s['topic']:<20}{s['date']:<15}{s['duration']:<16.0f}{classification:<8}")
        total_minutes += s["duration"]

    print(f"\nTotal time spent on {subject}: {total_minutes:.0f} minutes "
          f"({total_minutes / 60:.2f} hours)")


# ---------------------------------------------------------------------------
# f) study_statistics()
# ---------------------------------------------------------------------------
def study_statistics():
    """
    Compute and display:
      - total hours studied overall
      - total hours studied per subject
      - the subject with the least total study time (weakest area)
      - the single longest session recorded
    """
    print("\n--- Study Statistics ---")
    if not sessions:
        print("No study sessions have been logged yet.")
        return

    # Total hours studied overall.
    total_minutes = sum(s["duration"] for s in sessions)
    print(f"Total hours studied overall: {total_minutes / 60:.2f} hours")

    # Total hours studied per subject, using a dictionary to accumulate minutes.
    minutes_per_subject = {}
    for s in sessions:
        subject = s["subject"]
        minutes_per_subject[subject] = minutes_per_subject.get(subject, 0) + s["duration"]

    print("\nHours studied per subject:")
    for subject, minutes in minutes_per_subject.items():
        print(f"  {subject}: {minutes / 60:.2f} hours")

    # The subject with the least total study time (the student's weakest area).
    weakest_subject = min(minutes_per_subject, key=minutes_per_subject.get)
    print(f"\nWeakest area (least total study time): {weakest_subject} "
          f"({minutes_per_subject[weakest_subject] / 60:.2f} hours)")

    # The single longest session recorded.
    longest = max(sessions, key=lambda s: s["duration"])
    print(f"\nLongest session recorded: {longest['subject']} - {longest['topic']} "
          f"({longest['duration']:.0f} min, {classify_session(longest['duration'])})")


# ---------------------------------------------------------------------------
# g) save_sessions() and load_sessions()
# ---------------------------------------------------------------------------
def save_sessions():
    """
    Save every logged session to the data file (study_log.txt). Each session
    is written on its own line using '|' as a field separator, since subject/
    topic/date text is unlikely to contain that character.
    """
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        for s in sessions:
            line = f"{s['subject']}|{s['topic']}|{s['date']}|{s['duration']}\n"
            f.write(line)
    print(f"\nAll sessions have been saved to '{DATA_FILE}'.")


def load_sessions():
    """
    Automatically reload any existing sessions from the data file when the
    programme starts. If the file does not exist yet (e.g. on the very first
    run), the programme simply starts with an empty list instead of crashing.
    """
    if not os.path.exists(DATA_FILE):
        return  # No saved data yet - start with an empty sessions list.

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split("|")
            if len(parts) != 4:
                continue  # Skip malformed lines rather than crashing.
            subject, topic, date, duration_str = parts
            try:
                duration = float(duration_str)
            except ValueError:
                continue  # Skip lines with an unreadable duration.
            sessions.append({
                "subject": subject,
                "topic": topic,
                "date": date,
                "duration": duration,
            })


# ---------------------------------------------------------------------------
# a) Menu-driven interface
# ---------------------------------------------------------------------------
def display_menu():
    """Print the main menu options."""
    print("\n===== Smart Study Planner =====")
    print("1. Add a study session")
    print("2. View all sessions")
    print("3. Search sessions by subject")
    print("4. View statistics")
    print("5. Save and exit")


def main():
    """
    Main programme loop. Loads any previously saved sessions, then repeatedly
    displays the menu and dispatches to the relevant function based on the
    user's choice, rejecting invalid choices without crashing.
    """
    load_sessions()
    print("Welcome to the Smart Study Planner!")

    while True:
        display_menu()
        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            add_session()
        elif choice == "2":
            view_sessions()
        elif choice == "3":
            subject = input("Enter subject to search for: ").strip()
            search_by_subject(subject)
        elif choice == "4":
            study_statistics()
        elif choice == "5":
            save_sessions()
            print("Goodbye! Happy studying.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")


if __name__ == "__main__":
    main()
