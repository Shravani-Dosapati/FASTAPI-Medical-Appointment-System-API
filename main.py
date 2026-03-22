# FASTAPI Application on Medicine Appoitment System

import fastapi
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date
import math


app = fastapi.FastAPI()     # app is a variable or object of fastapi class

doctors = [
    {
        "id": 1,
        "name": "Dr. Anjali Mehta",
        "specialization": "Cardiologist",
        "fee": 800,
        "experience_years": 12,
        "is_available": True
    },
    {
        "id": 2,
        "name": "Dr. Rahul Verma",
        "specialization": "Dermatologist",
        "fee": 500,
        "experience_years": 8,
        "is_available": True
    },
    {
        "id": 3,
        "name": "Dr. Sneha Reddy",
        "specialization": "Pediatrician",
        "fee": 600,
        "experience_years": 10,
        "is_available": False
    },
    {
        "id": 4,
        "name": "Dr. Arjun Kapoor",
        "specialization": "General",
        "fee": 300,
        "experience_years": 5,
        "is_available": True
    },
    {
        "id": 5,
        "name": "Dr. Priya Sharma",
        "specialization": "Cardiologist",
        "fee": 900,
        "experience_years": 15,
        "is_available": True
    },
    {
        "id": 6,
        "name": "Dr. Vikram Singh",
        "specialization": "Dermatologist",
        "fee": 450,
        "experience_years": 7,
        "is_available": False
    }
]

appointments = []     # Empty list to store appointments
appt_counter = 1      # Counter to assign unique IDs to appointments

class AppointmentRequest(BaseModel):
    patient_name: str = Field(..., min_length=2)
    doctor_id: int = Field(..., gt=0)
    date: date
    reason: str = Field(..., min_length=5)
    appointment_type: str = "in-person"
    senior_citizen: bool = False

class NewDoctor(BaseModel):
    name: str = Field(..., min_length=2)
    specialization: str = Field(..., min_length=2)
    fee: int = Field(..., gt=0)
    experience_years: int = Field(..., gt=0)
    is_available: bool = True

@app.get("/")       #Home / route url
def home():
    return {"message": "Welcome to Medicine Appointment System"}

@app.get("/doctors")     # doctors / route url
def get_doctors():
    total = len(doctors)
    available_doctors = [doctor for doctor in doctors if doctor["is_available"]]

    return {
        "total": total,
        "available_count": len(available_doctors),
        "doctors": doctors}

@app.post("/test-appointment")
def test_appointment(data: AppointmentRequest):
    return data

def find_doctor(doctor_id: int):
    return next((d for d in doctors if d["id"] == doctor_id), None)

def calculate_fee(
        base_fee: int, 
        appointment_type: str, 
        senior_citizen: bool = False):
    
    if appointment_type == "video":
        fee = base_fee * 0.8
    elif appointment_type == "emergency":
        fee = base_fee * 1.5
    else:
        fee = base_fee

    if senior_citizen:
        fee = fee * 0.85

    return fee


@app.post("/appointments")     # appointments / route url
def create_appointment(appointment: AppointmentRequest):
    global appt_counter
    doctor = find_doctor(appointment.doctor_id)

    if not doctor:
        raise HTTPException(status_code=404, detail={"message": "Doctor not found"})
    
    if not doctor["is_available"]:
        raise HTTPException(status_code=400, detail={"message": "Doctor is not available"})
    
    fee = calculate_fee(doctor["fee"], appointment.appointment_type, appointment.senior_citizen)

    new_appointment = {
        "appointment_id": appt_counter,
        "patient_name": appointment.patient_name,
        "doctor_id": doctor["id"],
        "doctor_name": doctor["name"],
        "date": appointment.date,
        "reason": appointment.reason,
        "appointment_type": appointment.appointment_type,
        "fee": fee,
        "senior_citizen": appointment.senior_citizen,
        "status": "scheduled"
    }
    appointments.append(new_appointment)
    appt_counter += 1

    doctor["is_available"] = False

    return {"message": "Appointment created successfully", "appointment": new_appointment}

@app.get("/appointments")     # appointments / route url
def get_appointments():

    return {
        "total_appointments": len(appointments),
        "appointments": appointments
    }


def filter_doctors_logic(
    specialization: str = None,
    max_fee: int = None,
    min_experience: int = None,
    is_available: bool = True):

    result = doctors

    if specialization is not None:
        result = [d for d in result if d["specialization"].lower() == specialization.lower()]
    
    if max_fee is not None:
        result = [d for d in result if d["fee"] <= max_fee]
    
    if min_experience is not None:
        result = [d for d in result if d["experience_years"] >= min_experience]

    if is_available is not None:
        result = [d for d in result if d["is_available"] == is_available]

    return result

@app.get("/doctors/filter") 
def filter_doctors(
    specialization: str = None,
    max_fee: int = None,
    min_experience: int = None,
    is_available: bool = True):

    filtered = filter_doctors_logic(
            specialization, 
            max_fee, 
            min_experience,
            is_available)

    return {
        "total": len(filtered),
        "doctors": filtered}

@app.post("/doctors", status_code=201)     # doctors / route url
def add_doctor(new_doc: NewDoctor):

    existing = next(
        (d for d in doctors if d["name"].lower() == new_doc.name.lower()), 
        None)

    if existing:
        raise HTTPException(status_code=400, detail="Doctor with this name already exists")

    new_doctor = {
        "id": len(doctors) + 1,
        "name": new_doc.name,
        "specialization": new_doc.specialization,
        "fee": new_doc.fee,
        "experience_years": new_doc.experience_years,
        "is_available": new_doc.is_available
    }
    doctors.append(new_doctor)

    return {"message": "Doctor added successfully", "doctor": new_doctor}

@app.put("/doctors/{doctor_id}")     # doctors/{doctor_id} / route url
def update_doctor(doctor_id: int,
                  fee: Optional[int] = None,
                  is_available: Optional[bool] = None):
    
    doctor = find_doctor(doctor_id)

    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    if fee is not None:
        if fee <= 0:
            raise HTTPException(status_code=400, detail="Fee must be greater than 0")
        doctor["fee"] = fee 

    if is_available is not None:
        doctor["is_available"] = is_available

    return {"message": "Doctor details updated successfully", "doctor": doctor}

@app.delete("/doctors/{doctor_id}")     # doctors/{doctor_id} / route url
def delete_doctor(doctor_id: int):

    doctor = find_doctor(doctor_id)

    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    # Check for active (scheduled) appointments
    has_active_appointments = any(
        appt for appt in appointments
        if appt["doctor_id"] == doctor_id and appt["status"] == "scheduled")

    if has_active_appointments:
        raise HTTPException(status_code=400,detail="Cannot delete doctor with active appointments")

    # Remove doctor
    doctors.remove(doctor)

    return {"message": "Doctor deleted successfully"}

def find_appointment(appt_id: int):
    return next((a for a in appointments if a["appointment_id"] == appt_id), None)

@app.post("/appointments/{appointment_id}/confirm")     # appointments/{appointment_id}/confirm/route url
def confirm_appointment(appointment_id: int):
    appointment = find_appointment(appointment_id)

    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    if appointment["status"] != "scheduled":
        raise HTTPException(status_code=400, detail="Only scheduled appointments can be confirmed")

    appointment["status"] = "confirmed"

    return {"message": "Appointment confirmed successfully", "appointment": appointment}

@app.post("/appointments/{appointment_id}/cancel")     # appointments/{appointment_id}/cancel/route url
def cancel_appointment(appointment_id: int):
    appointment = find_appointment(appointment_id)

    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    if appointment["status"] == "cancelled":
        raise HTTPException(status_code=400, detail="Appointment is already cancelled")

    # Making the doctor available again if appointment is cancelled
    appointment["status"] = "cancelled"
    doctor = find_doctor(appointment["doctor_id"])
    if doctor:
        doctor["is_available"] = True

    return {"message": "Appointment cancelled successfully", "appointment": appointment}

@app.post("/appointments/{appointment_id}/complete")     # appointments/{appointment_id}/completed/route url
def complete_appointment(appointment_id: int):
    appointment = find_appointment(appointment_id)

    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    if appointment["status"] != "confirmed":
        raise HTTPException(status_code=400, detail="Only confirmed appointments can be marked as completed")

    appointment["status"] = "completed"

    return {"message": "Appointment marked as completed successfully", "appointment": appointment}

@app.get("/appointments/active")     # appointments/active/route url
def get_active_appointments():
    active_appointments = [a for a in appointments if a["status"] in ["scheduled", "confirmed"]]

    return {
        "total": len(active_appointments),
        "active_appointments": active_appointments
    }

@app.get("/appointments/by-doctor/{doctor_id}")     # appointments/by-doctor/{doctor_id}/route url
def get_appointments_by_doctor(doctor_id: int):

    doctor = find_doctor(doctor_id)

    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    doctor_appointments = [a for a in appointments if a["doctor_id"] == doctor_id]

    return {
        "total": len(doctor_appointments),
        "appointments": doctor_appointments
    }

@app.get("/doctors/search")     # doctors/search/route url
def search_doctors(keyword: str):
    keyword = keyword.lower()

    results = [d for d in doctors if keyword in d["name"].lower() or keyword in d["specialization"].lower()]

    if not results:
        raise HTTPException(status_code=404, detail="No doctors found matching the keyword")
    
    return {
        "total": len(results),
        "doctors": results
    }  
@app.get("/doctors/sort")
def sort_doctors(sort_by: str = "fee", order: str = "asc"):

    valid_fields = ["fee", "name", "experience_years"]

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail="Invalid sort field")

    reverse = True if order == "desc" else False

    sorted_list = sorted(doctors, key=lambda d: d[sort_by], reverse=reverse)

    return {
        "sort_by": sort_by,
        "order": order,
        "doctors": sorted_list
    }

@app.get("/doctors/page")
def paginate_doctors(page: int = 1, limit: int = 3):
    
    total = len(doctors)
    
    total_pages = math.ceil(total / limit)
    
    start = (page - 1) * limit
    end = start + limit

    data = doctors[start:end]

    return {
        "page": page,
        "limit": limit,
        "total_pages": total_pages,
        "total_records": total,
        "doctors": data}


@app.get("/appointments/search")
def search_appointments(patient_name: str):

    results = [
        a for a in appointments
        if patient_name.lower() in a["patient_name"].lower()
    ]

    return {
        "total": len(results),
        "appointments": results}

@app.get("/appointments/sort")
def sort_appointments(sort_by: str = "fee"):

    if sort_by not in ["fee", "date"]:
        raise HTTPException(status_code=400, detail="Invalid sort field")

    sorted_list = sorted(appointments, key=lambda a: a[sort_by])

    return {"appointments": sorted_list}

@app.get("/appointments/page")
def paginate_appointments(page: int = 1, limit: int = 3):

    total = len(appointments)
    start = (page - 1) * limit
    end = start + limit

    return {
        "page": page,
        "total": total,
        "appointments": appointments[start:end]}


@app.get("/doctors/browse")
def browse_doctors(
    keyword: str = None,
    sort_by: str = "fee",
    order: str = "asc",
    page: int = 1,
    limit: int = 4
):
    result = doctors

    # FILTER
    if keyword:
        keyword = keyword.lower()
        result = [
            d for d in result
            if keyword in d["name"].lower() or keyword in d["specialization"].lower()
        ]

    # SORT
    reverse = True if order == "desc" else False
    result = sorted(result, key=lambda d: d[sort_by], reverse=reverse)

    # PAGINATION
    total = len(result)
    start = (page - 1) * limit
    end = start + limit

    paginated = result[start:end]

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "results": paginated
    }

@app.get("/doctors/summary")     # doctors/summary / route url
def get_doctors_summary():
    total = len(doctors)
    available = len([d for d in doctors if d["is_available"]])
    most_experienced = max(doctors, key=lambda d: d["experience_years"])
    cheap_consultation= min(doctors, key=lambda d: d["fee"])["fee"] # Find the doctor with the lowest fee
    specialization_count = {}
    for doctor in doctors:
        specialization = doctor["specialization"]
        specialization_count[specialization] = specialization_count.get(specialization, 0) + 1

    return {
        "total": total,
        "available_count": available,
        "most_experienced_doctor": most_experienced["name"],
        "cheapest_fee": cheap_consultation,
        "specialization_count": specialization_count
    }


@app.get("/doctors/{doctor_id}")
def get_doctor(doctor_id: int):
    doc = find_doctor(doctor_id)

    if not doc:
        raise HTTPException(status_code=404, detail="Doctor not found")

    return doc













