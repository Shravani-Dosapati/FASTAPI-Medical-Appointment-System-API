# 💊 Medical Appointment System API (FastAPI)

A backend system built using **FastAPI** to manage doctors, appointments, and consultation workflows.
This project demonstrates real-world backend concepts like validation, filtering, sorting, pagination, and workflow handling.

---

## 🚀 Features

### 👨‍⚕️ Doctor Management

* Add new doctors
* Update doctor details (fee, availability)
* Delete doctors with dependency checks
* Filter doctors by specialization, fee, experience, and availability
* Search doctors by name or specialization
* Sort and paginate doctor data
* Combined browse (filter + sort + pagination)

---

### 📅 Appointment Management

* Create appointments with validation
* Fee calculation based on:

  * Appointment type (video, in-person, emergency)
  * Senior citizen discount
* Confirm, cancel, and complete appointments
* Track appointment status:

  * scheduled → confirmed → completed
  * scheduled/confirmed → cancelled
* View active appointments
* Search, sort, and paginate appointments
* Get appointments by doctor

---

## 🧠 Concepts Covered

* FastAPI routing and path operations
* Pydantic validation
* Query parameters handling
* Helper functions (clean architecture)
* Business logic layering
* State management (appointment lifecycle)
* Error handling with HTTPException
* Filtering, sorting, and pagination
* REST API best practices

---

## 🛠️ Tech Stack

* Python
* FastAPI
* Uvicorn
* Pydantic

---

## ⚙️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/your-username/medical-appointment-api.git
cd medical-appointment-api
```

### 2. Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

### 3. Install dependencies

```bash
pip install fastapi uvicorn
```

### 4. Run the server

```bash
uvicorn main:app --reload
```

---

## 📌 API Documentation

Once the server is running, open:

👉 Swagger UI

```
http://127.0.0.1:8000/docs
```

👉 ReDoc

```
http://127.0.0.1:8000/redoc
```

---

## 📊 Sample Endpoints

### Doctors

* `GET /doctors`
* `POST /doctors`
* `PUT /doctors/{doctor_id}`
* `DELETE /doctors/{doctor_id}`
* `GET /doctors/filter`
* `GET /doctors/search`
* `GET /doctors/sort`
* `GET /doctors/page`
* `GET /doctors/browse`

---

### Appointments

* `POST /appointments`
* `GET /appointments`
* `POST /appointments/{id}/confirm`
* `POST /appointments/{id}/cancel`
* `POST /appointments/{id}/complete`
* `GET /appointments/active`
* `GET /appointments/by-doctor/{doctor_id}`
* `GET /appointments/search`
* `GET /appointments/sort`
* `GET /appointments/page`

---

## 🔄 Appointment Workflow

```
scheduled → confirmed → completed
scheduled → cancelled
confirmed → cancelled
```

---

## ⚠️ Important Notes

* Doctors cannot be deleted if they have active (scheduled) appointments
* Appointment fees are dynamically calculated
* Validation is handled using Pydantic models
* All filters use safe checks (`is not None`)

---

## 🎯 Future Improvements

* Database integration (PostgreSQL / MongoDB)
* Authentication & Authorization (JWT)
* Role-based access (Admin / Patient / Doctor)
* Logging & monitoring
* Deployment (Docker + Cloud)

---

## 👩‍💻 Author

Shravani Dosapati

---

## 📄 License

This project is for learning and demonstration purposes.
