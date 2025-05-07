
# 🚨 TrafficGuardian - Motorbike Safety Violation Detection System

TrafficGuardian is a smart backend system built in Python to automate the detection and reporting of traffic safety violations related to motorbikes. This project is designed to assist law enforcement in identifying violators through camera feeds and alerting nearby traffic wardens in real-time.

## 📁 Project Structure

```
├── Controller/
│   ├── ChallanController.py
│   ├── YoloController.py
│   ├── OCR.py
│   └── ... 
├── Model/
│   ├── Violation.py
│   ├── WadenChowki.py
│   ├── Shift.py
│   └── ...
├── Router.py
├── app.py (or main.py)
├── requirements.txt
└── README.md
```

## 🚦 Features

- 🔍 Detects motorbike violations (no helmet, side mirrors, etc.)
- 🎯 Real-time YOLOv8 integration for object detection
- 📷 OCR for number plate recognition
- 🧠 Intelligent routing of alerts to nearest chowki
- 🧾 Auto-generation of challan (ticket) via controller logic
- 🗂️ SQLite/MySQL/PostgreSQL support for persistent data storage

## 🛠️ Technologies Used

- **Python 3.10+**
- **Flask / FastAPI**
- **YOLOv8 (Ultralytics)**
- **Tesseract OCR**
- **OpenCV**
- **SQLAlchemy**
- **PyCharm** as the main IDE

## 🔌 How to Run

1. **Clone the repository**:
   ```bash
   git clone https://github.com/MohsinALi1a1/TrafficGuardian.git
   cd TrafficGuardian
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the app**:
   ```bash
   python app.py
   ```

## 🔐 Authentication (Optional)
You can implement token-based authentication to secure the endpoints for admin, warden, and camera roles.

## 📸 Dataset & Training
- YOLOv8 trained on a custom dataset annotated using Roboflow.
- Dataset includes helmet detection, number plates, and side mirrors.

## 📂 Database Schema Highlights

- `TrafficWarden`: Stores warden info
- `Violation`: Stores violation types and timestamps
- `ChallanHistory`: Tracks issued challans and warden who issued them
- `Direction`, `Camera`, `Chowki`: Logical mapping of real-world monitoring points

## 👨‍💻 Contributors

- **Mohsin Ali** – Backend Developer & AI Integration
- **Team Members** – (add your teammates)

## 📄 License

This project is part of an academic final year project and is not licensed for commercial use. Contact the author for more information.

---

## 📬 Contact

Have questions or suggestions?

- Email: mohsinali@example.com
- GitHub: [MohsinALi1a1](https://github.com/MohsinALi1a1)
