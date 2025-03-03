import streamlit as st
import math
from fpdf import FPDF
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

st.title("TFP Billing Calculator")
st.header("Beta 1.1 - JRT")

clientname = st.text_input("Client Name: ")
patientname = st.text_input("Patient Name: ")
species = st.text_input("Species: ").lower().strip()
weight = st.number_input("Patient Weight: ")

# Initialize session state variables
if 'billing_values' not in st.session_state:
    st.session_state.billing_values = []
if 'itemized_billing' not in st.session_state:
    st.session_state.itemized_billing = []

def main():
    confinementdays = st.number_input("How many days to charge: ")
    if weight <= 5:
        daily_rate_charge = (confinementdays * 1000)
    elif weight <= 10:
        daily_rate_charge = (confinementdays * 1500)
    elif weight <= 20:
        daily_rate_charge = (confinementdays * 2500)
    elif weight <= 30:
        daily_rate_charge = (confinementdays * 3000)
    elif weight <= 40:
        daily_rate_charge = (confinementdays * 3500)
    elif weight <= 50:
        daily_rate_charge = (confinementdays * 5000)
    else:
        daily_rate_charge = (confinementdays * 5500)
    st.write(daily_rate_charge)
    if st.button("Save to Bill", key="daily_rate_charge"):
        st.session_state.billing_values.append(daily_rate_charge)
        st.session_state.itemized_billing.append(("Daily Rate Charge", daily_rate_charge))
    
    if weight <= 5:
        daily_med_rate_1 = 100
        daily_med_rate_2 = 200 
    elif weight <= 10:
        daily_med_rate_1 = 200
        daily_med_rate_2 = 400 
    elif weight <= 20:
        daily_med_rate_1 = 300
        daily_med_rate_2 = 600 
    elif weight <= 30:
        daily_med_rate_1 = 400
        daily_med_rate_2 = 800 
    elif weight <= 40:
        daily_med_rate_1 = 500
        daily_med_rate_2 = 1000 
    elif weight <= 50:
        daily_med_rate_1 = 600
        daily_med_rate_2 = 1200 
    else:
        daily_med_rate_1 = 700
        daily_med_rate_2 = 1400

    meds = st.text_input("Input meds/consumables/lab tests: ").lower()
    if meds in ["orni", "atro", "coforta", "doxy", "ampi", "tolfine", "calmivet", "fercob", "septo", "tramadol", "metoc", "tranex", "dexa", "ascorbic", "phytomenadione", "dupha", "furo", "cefurox", "salbutamol", "metro", "dcm", "bromhex"]:
        dose_number = st.number_input("How many doses? ")
        to_bill = (dose_number * daily_med_rate_1)
        st.write(to_bill)
        dose_number = int(dose_number)
        if st.button("Save to Bill", key="meds1"):
            st.session_state.billing_values.append(to_bill)
            st.session_state.itemized_billing.append((f"{meds} {dose_number} dose/s", to_bill))

    elif meds in ["marbo", "oxytocin", "diphen", "epi", "omep", "ome", "ceftriaxone", "ceftri", "coamox"]:
        dose_number = st.number_input("How many doses? ")
        to_bill = (dose_number * daily_med_rate_2)
        st.write(to_bill)
        dose_number = int(dose_number)
        if st.button("Save to Bill", key="meds2"):
            st.session_state.billing_values.append(to_bill)
            st.session_state.itemized_billing.append((f"{meds} {dose_number} dose/s", to_bill))


    elif meds in ["ivermectim", "ivermec", "ivomec", "ivermectin"]:
        dose_number = st.number_input("How many doses? ")
        if weight <= 5:
            ivermecrate = 1000
        elif weight <= 10:
            ivermecrate = 1100
        elif weight <= 15:
            ivermecrate = 1200
        elif weight <= 20:
            ivermecrate = 1300
        elif weight <= 25:
            ivermecrate = 1400
        elif weight <= 30:
            ivermecrate = 1500
        elif weight <= 35:
            ivermecrate = 1600
        elif weight <= 40:
            ivermecrate = 1700
        elif weight <= 45:
            ivermecrate = 1800
        elif weight <= 50:
            ivermecrate = 1900
        else:
            ivermecrate = 2000
        ivermecprice = (dose_number * ivermecrate)
        dose_number = int(dose_number)
        st.write(ivermecprice)
        if st.button("Save to Bill", key="meds3"):
            st.session_state.billing_values.append(ivermecprice)
            st.session_state.itemized_billing.append((f"Ivermectin {dose_number} dose/s", ivermecprice))

    elif meds == "convenia":
        dose_number = st.number_input("How many doses? ")
        dose_number = int(dose_number)
        if weight >= 6:
            conveniarate = 1500 + (math.floor(weight) - 5) * 250
        else:
            conveniarate = 1500
        conveniaprice = (dose_number * conveniarate)
        st.write(conveniaprice)
        if st.button("Save to Bill", key="meds4"):
            st.session_state.billing_values.append(conveniaprice)
            st.session_state.itemized_billing.append((f"Convenia {dose_number} dose/s", conveniaprice))

    elif meds in ["vincristine", "vinc"]:
        dose_number = st.number_input("How many doses? ")
        dose_number = int(dose_number)
        if weight >= 6:
            vincrate = 3500 + (math.floor(weight) - 5) * 100
        else:
            vincrate = 3500
        vincprice = (dose_number * vincrate)
        st.write(vincprice)
        if st.button("Save to Bill", key="meds5"):
            st.session_state.billing_values.append(vincprice)
            st.session_state.itemized_billing.append((f"Vincristine {dose_number} dose/s", vincprice))

    elif meds in ["canglob", "canglob p", "canglob d"]:
        dose_number = st.number_input("How many doses? ")
        dose_number = int(dose_number)
        if weight >= 11:
            canglobrate = 1500 + (math.floor(weight) - 10) * 250
        else:
            canglobrate = 1500
        canglobprice = (dose_number * canglobrate)
        st.write(canglobprice)
        if st.button("Save to Bill", key="meds6"):
            st.session_state.billing_values.append(canglobprice)
            st.session_state.itemized_billing.append((f"Canglob {dose_number} dose/s", canglobprice))

    elif meds in ["imido", "imidocarb"]:
        dose_number = st.number_input("How many doses? ")
        dose_number = int(dose_number)
        if weight >= 11:
            imidorate = 3500 + (math.floor(weight) - 10) * 250
        else:
            imidorate = 3500
        imidoprice = (dose_number * imidorate)
        st.write(imidoprice)
        if st.button("Save to Bill", key="meds7"):
            st.session_state.billing_values.append(imidoprice)
            st.session_state.itemized_billing.append((f"Imidocarb {dose_number}", imidoprice))

    elif meds == "librela":
        if weight >= 6:
            librerate = 3500 + (math.floor(weight) - 5) * 250
        else:
            librerate = 3500
        st.write(librerate)
        if st.button("Save to Bill", key="meds8"):
            st.session_state.billing_values.append(librerate)
            st.session_state.itemized_billing.append(("Librela", librerate))

    elif meds in ["cbc bc", "cbc chem", "cbcbc"]:
        cbcbc_rate = 3800
        cbcbc_number = st.number_input("How many CBC + BC to charge? ")
        cbcbc_number = int(cbcbc_number)
        to_bill = (cbcbc_number * cbcbc_rate)
        st.write(to_bill)
        if st.button("Save to Bill", key="meds9"):
            st.session_state.billing_values.append(to_bill)
            st.session_state.itemized_billing.append((f"CBC + BC {cbcbc_number} test/s", to_bill))

    elif meds in ["cbc", "cbc only"]:
        cbc_rate = 1500
        cbc_number = st.number_input("How many CBC to charge? ")
        cbc_number = int(cbc_number)
        to_bill = (cbc_number * cbc_rate)
        st.write(to_bill)
        if st.button("Save to Bill", key="meds10"):
            st.session_state.billing_values.append(to_bill)
            st.session_state.itemized_billing.append((f"CBC {cbc_number} test/s", to_bill))

    elif meds in ["bc", "blood chem", "blood chemistry", "chem"]:
        bc_rate = 2700
        bc_number = st.number_input("How many BC to charge? ")
        bc_number = int(bc_number)
        to_bill = (bc_number * bc_rate)
        st.write(to_bill)
        if st.button("Save to Bill", key="meds11"):
            st.session_state.billing_values.append(to_bill)
            st.session_state.itemized_billing.append((f"Blood Chemistry {bc_number} tests", to_bill))

    elif meds in ["iv line", "iv fluids", "iv", "iv cannula", "infusion pump"]:
        ivline = st.number_input("How many IV lines to charge? ")
        ivfluids = st.number_input("How many IV fluid bottles to charge? ")
        ivcannula = st.number_input("How many IV cannulas to charge? ")
        infusionpump = st.number_input("How many days of infusion pump to charge? ")
        to_bill = (ivline * 50) + (ivfluids * 250) + (ivcannula * 50) + (infusionpump * 250)
        ivline = int(ivline)
        ivfluids = int(ivfluids)
        ivcannula = int(ivcannula)
        infusionpump =  int(infusionpump)
        st.write(to_bill)
        if st.button("Save to Bill", key="meds12"):
            st.session_state.billing_values.append(to_bill)
            st.session_state.itemized_billing.append((f"IV Line {ivline} pc/s \nIV Fluids {ivfluids} bottle/s \nIV Cannula {ivcannula} pc/s \nInfusion Pump {infusionpump} days", to_bill))

    elif meds == "oxygen" or meds == "oxygen therapy":
        to_bill = st.number_input("How much to charge Oxygen therapy? ")
        st.write(to_bill)
        if st.button("Save to Bill", key="meds13"):
            st.session_state.billing_values.append(to_bill)
            st.session_state.itemized_billing.append(("Oxygen Therapy", to_bill))

    elif meds == "diazepam":
        diazepamvial = st.number_input("How many vials of Diazepam?")
        to_bill = (diazepamvial * 1500)
        diazepamvial = int(diazepamvial)
        st.write(to_bill)
        if st.button("Save to Bill", key="meds14"):
            st.session_state.billing_values.append(to_bill)
            st.session_state.itemized_billing.append((f"Diazepam {diazepamvial} vial/s", to_bill))

    elif meds == "towel" or meds == "towels":
        towelcount = st.number_input("How many towels to charge? ")
        to_bill = (towelcount * 60)
        towelcount = int(towelcount)
        st.write(to_bill)
        if st.button("Save to Bill", key="meds15"):
            st.session_state.billing_values.append(to_bill)
            st.session_state.itemized_billing.append((f"Towel {towelcount} pc/s", to_bill))

    elif meds == "underpads" or meds == "pads" or meds == "underpad" or meds == "pad":
        padcount = st.number_input("How many underpad/s to charge? ")
        to_bill = (padcount * 30)
        padcount = int(padcount)
        st.write(to_bill)
        if st.button("Save to Bill", key="meds16"):
            st.session_state.billing_values.append(to_bill)
            st.session_state.itemized_billing.append((f"Underpads {padcount} piece/s", to_bill))
    
    elif meds == "icu":
        icudays = st.number_input("How many days in ICU? ")
        to_bill = (icudays * 1000)
        icudays = int(icudays)
        st.write(to_bill)
        if st.button("Save to Bill", key="meds17"):
            st.session_state.billing_values.append(to_bill)
            st.session_state.itemized_billing.append((f"ICU Charges {icudays} day/s", to_bill))

    elif meds == "medical boarding" or meds == "boarding":
        boarding_days = st.number_input("How many days in boarding? ")
        to_bill = (boarding_days * 1000)
        boarding_days = int(boarding_days)
        st.write(to_bill)
        if st.button("Save to Bill", key="meds18"):
            st.session_state.billing_values.append(to_bill)
            st.session_state.itemized_billing.append((f"Medical Boarding Charges {boarding_days} day/s", to_bill))


    elif meds in ["gastro", "hepatic" , "cardiac" , "renal" , "urinary"]:
        rcfood_cans = st.number_input("How many cans? ")
        to_bill = (rcfood_cans * 450)
        rcfood_cans = int(rcfood_cans)
        st.write(to_bill)
        if st.button("Save to Bill", key="meds19"):
            st.session_state.billing_values.append(to_bill)
            st.session_state.itemized_billing.append((f"RC {(meds.capitalize())} {rcfood_cans} can/s", to_bill))


    elif meds in ["reco" , "recovery"]:
        reco_cans = st.number_input("How many cans? ")
        to_bill = (reco_cans * 350)
        reco_cans = int(reco_cans)
        st.write(to_bill)
        if st.button("Save to Bill", key="meds20"):
            st.session_state.billing_values.append(to_bill)
            st.session_state.itemized_billing.append((f"RC RECOVERY {reco_cans} can/s", to_bill))
    
    elif meds == "starter":
        starter_cans = st.number_input("How many cans? ")
        to_bill = (reco_cans * 250)
        starter_cans = int(starter_cans)
        st.write(to_bill)
        if st.button("Save to Bill", key="meds21"):
            st.session_state.billing_values.append(to_bill)
            st.session_state.itemized_billing.append((f"RC STARTER {starter_cans} can/s", to_bill))


    st.write(st.session_state.itemized_billing)

main()

if st.button("Get Total"):
    total_billing = sum(st.session_state.billing_values)
    st.write("Total Billing: ", total_billing)

if st.button("Generate Bill"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="The Furr Project QC", ln=True, align="C")
    pdf.cell(200, 10, txt="Billing Statement", ln=True, align="C")
    pdf.cell(200, 10, txt=f"Client Name: {clientname}", ln=True, align="L")
    pdf.cell(200, 10, txt=f"Patient Name: {patientname}", ln=True, align="L")
    pdf.cell(200, 10, txt=f"Species: {species}", ln=True, align="L")
    pdf.cell(200, 10, txt=f"Weight: {weight}", ln=True, align="L")
    pdf.cell(200, 10, txt="Billing Details", ln=True, align="C")
    for name, value in st.session_state.itemized_billing:
        pdf.cell(200, 10, txt=f"{name}: {int(value)}", ln=True, align="L")
    total_billing = sum(st.session_state.billing_values)
    pdf.cell(200, 10, txt=f"Total Billing: {total_billing}", ln=True, align="L")
    pdf.output("billing.pdf")

    with open("billing.pdf", "rb") as pdf_file:
        PDFbyte = pdf_file.read()

    st.download_button(label="Download Bill",
                       data=PDFbyte,
                       file_name=f"{patientname} Billing.pdf",
                       mime="application/octet-stream")
