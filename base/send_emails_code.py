import pandas as pd
import requests
import json
from datetime import datetime as dt
import smtplib
import os

def populate_dummy_data():
    session = requests.Session()
    headers = {"content-type": "application/json"}

    patient_json = """{
        "resourceType": "Patient",
        "id": "2",
        "active": true,
        "name": [
            {6
                "use": "official",
                "family": "Bo",
                "given": [
                    "Mary"
                ]
            }
        ],
        "gender": "female",
        "birthDate": "1998-12-22",
        "deceasedBoolean": false
        }
    """
    url = "http://localhost:8080/fhir/Patient"
    response = session.post(url, headers=headers, data=patient_json)

    condition_json = """{
        "resourceType" : "Condition",
        "id" : "1",
        "clinicalStatus" : {
            "coding" : [{
            "system" : "http://terminology.hl7.org/CodeSystem/condition-clinical",
            "code" : "active"
            }]
        },
        "verificationStatus" : {
            "coding" : [{
            "system" : "http://terminology.hl7.org/CodeSystem/condition-ver-status",
            "code" : "confirmed"
            }]
        },
        "category" : [{
            "coding" : [{
            "system" : "http://terminology.hl7.org/CodeSystem/condition-category",
            "code" : "encounter-diagnosis",
            "display" : "Encounter Diagnosis"
            },
            {
            "system" : "http://snomed.info/sct",
            "code" : "439401001",
            "display" : "Diagnosis"
            }]
        }],
        "severity" : {
            "coding" : [{
            "system" : "http://snomed.info/sct",
            "code" : "24484000",
            "display" : "Severe"
            }]
        },
        "code" : {
            "coding" : [{
            "system" : "http://snomed.info/sct",
            "code" : "243796009",
            "display" : "Anxiety"
            }],
            "text" : "Anxiety"
        },
        "subject" : {
            "reference" : "Patient/2"
        },
        "onsetDateTime" : "2022-05-24"
        }"""
    url = "http://localhost:8080/fhir/Condition"
    response = session.post(url, headers=headers, data=condition_json)

    meds_json = """{
        "resourceType": "MedicationRequest",
        "id": "example",
        "meta": {
            "extension": [
                {
                    "url": "http://hl7.org/fhir/StructureDefinition/instance-name",
                    "valueString": "CDMH Medication Request Example"
                },
                {
                    "url": "http://hl7.org/fhir/StructureDefinition/instance-description",
                    "valueMarkdown": "This is a CDMH Medication Request example for the *CDMH  MedicationRequest Profile*."
                }
            ],
            "profile": [
                "http://hl7.org/fhir/us/cdmh/StructureDefinition/cdmh-medicationrequest"
            ]
        },
        "status": "active",
        "intent": "order",
        "medicationCodeableConcept": {
            "coding": [
                {
                    "system": "http://www.nlm.nih.gov/research/umls/rxnorm",
                    "code": "312938",
                    "display": "Zoloft 75mg"
                }
            ],
            "text": "Zoloft 75mg"
        },
        "subject": {
            "reference": "Patient/2"
        },
        "authoredOn": "2022-04-05",
        "dosageInstruction": [
            {
                "text": "75 mg",
                "timing": {
                    "repeat": {
                        "boundsPeriod": {
                            "start": "2022-04-05"
                        }
                    }
                }
            }
        ],
        "dispenseRequest": {
            "numberOfRepeatsAllowed": 100,
            "quantity": {
                "value": 75,
                "unit": "mg",
                "system": "http://unitsofmeasure.org",
                "code": "mg"
            },
            "expectedSupplyDuration": {
                "value": 300,
                "unit": "days",
                "system": "http://unitsofmeasure.org",
                "code": "d"
            }
        }
    }"""
    url = "http://localhost:8080/fhir/MedicationRequest"
    response = session.post(url, headers=headers, data=meds_json)

    return

def pull_patient():
    # pull patient
    url = 'http://localhost:8080/fhir/Patient/2'
    session = requests.Session()
    headers = {"content-type": "application/json"}
    response = session.get(url, headers=headers, verify=False)
    pjson = json.loads(response.text)
    return pjson

def pull_diagnosis():
    # pull diagnosis
    url = 'http://localhost:8080/fhir/Condition?subject=2'
    session = requests.Session()
    headers = {"content-type": "application/json"}
    response = session.get(url, headers=headers, verify=False)
    cjson = json.loads(response.text)
    diagnosis = cjson.get('entry', {})[0].get('resource', {}).get('code', {}).get('text')
    return diagnosis

def pull_medication():
    # pull medication
    url = 'http://localhost:8080/fhir/MedicationRequest?subject=2'
    session = requests.Session()
    headers = {"content-type": "application/json"}
    response = session.get(url, headers=headers, verify=False)
    mjson = json.loads(response.text)
    medication = mjson.get('entry', {})[0].get('resource', {}).get('medicationCodeableConcept', {}).get('text')
    return medication

def format_clusters(clusters):
    # fix list formatting
    for col in ['means', 'stds', 'mins', 'maxes']:
        clusters[col] = clusters[col].apply(lambda x:json.loads(x))

    # because I don't actually have access to location data, I'll be leaving that out of the algorithm for now
    # limit all lists to non-location only for now
    for col in ['means', 'stds', 'mins', 'maxes']:
        clusters[col] = clusters[col].apply(lambda x: x[:9])
    return clusters

def create_current_list(diagnosis, medication, patient):
    # create current list
    cur_list = [float(pd.Timestamp.today().weekday()), float(dt.now().hour), 2.0]
    if diagnosis == 'Anxiety':
        cur_list = cur_list + [1.0, 1.0, 0.0]
    else:
        cur_list = cur_list + [0.0, 0.0, 1.0]
    if medication == 'Zoloft 75mg':
        cur_list = cur_list + [0.0, 1.0, 0.0]
    elif medication == 'sertraline 200mg':
        cur_list = cur_list + [0.0, 0.0, 1.0]
    else:
        cur_list = cur_list + [1.0, 0.0, 0.0]
    return cur_list

def send_email_fun():
    email = os.environ['EMAIL_ADDRESS']
    password = os.environ['EMAIL_PASS']
    recipient='ageary6@gatech.edu'

    mail=smtplib.SMTP('smtp.gmail.com', 587)
    mail.ehlo()
    mail.starttls()
    mail.login(email,password)

    email_body="Our algorithm found that you usually enter tasks around this time--Do you have any tasks to enter? Visit [LINK] if you do."
    header='To:'+recipient+'\n'+'From:'+email+'\n'+'subject: Do you have any tasks to record?\n'
    full_content=header+email_body

    mail.sendmail(email, recipient, full_content)
    mail.close()

def choose_send_email(clusters, cur_list):
    for index, row in clusters.iterrows():
        send_email = True
        if row['mins'] > cur_list:
            send_email = False
        if row['maxes'] < cur_list:
            send_email = False
        if send_email:
            send_email_fun()
            break

def send_email_notifications_with_model():
    populate_dummy_data()
    clusters = pd.read_csv('data/clustering_results.csv')
    clusters = format_clusters(clusters)
    medication = pull_medication()
    diagnosis = pull_diagnosis()
    patient = pull_patient()
    cur_list = create_current_list(diagnosis, medication, patient)
    choose_send_email(clusters, cur_list)




