🏫 Smart Timetable Generator

An intelligent timetable generation system designed to simplify and optimize the creation of school timetables — starting with primary schools.

The system ensures:

* Balanced subject distribution
* Fair teacher workload allocation
* Conflict-free scheduling
* Flexible school structure support

---

🚀 Features

✅ Core Functionality

* Automatic timetable generation
* Support for single and double lessons
* Flexible school schedules (different days & periods)
* Breaks, lunch, assemblies, and custom slot types
* Capacity validation (Required vs Available slots)

🧠 Smart Constraints Handling

* No overlapping lessons per class
* Subject lesson requirements per week
* Double lesson handling
* Lab session flexibility
* Detection of under/over allocation

⚙️ System Design

* Modular architecture (data, core logic, execution)
* Extendable for AI-based optimization
* Built for scalability (multi-class, multi-teacher support)

---

🏗️ Project Structure

```
project-root/
│
├── core/                  # Scheduling logic
│   ├── scheduler.py
│   ├── timeslot_generator.py
│   └── lesson_block_generator.py
│
├── models/                # Data models
│   ├── subject.py
│   ├── class_model.py
│   └── timeslot.py
│
├── data/                  # Sample & initialization data
│   └── sample_data.py
│
├── main.py                # Entry point
└── README.md
```

---

## ▶️ How to Run

1. Clone the repository:

bash
git clone https://github.com/your-username/timetable-generator.git
cd timetable-generator


2. Run the system:

bash
python main.py


---

🧪 Current Capabilities

* Generates a working timetable
* Handles double lessons correctly
* Avoids slot conflicts
* Detects capacity issues
* Produces clean, readable output

---

🚧 Upcoming Features

* Teacher assignment and conflict handling
* Subject distribution optimization
* Difficulty-based scheduling (AI)
* UI for school administrators
* Database integration
* Multi-class scheduling

---

🧠 Vision

To build a **smart academic scheduling system** that:

* Reduces administrative workload
* Improves student learning experience
* Provides data-driven insights for schools

---

🤝 Contributing

Contributions are welcome. Feel free to fork the project and submit a pull request.

---

📄 License

This project is licensed under the MIT License.
