import streamlit as st
from fpdf import FPDF
from datetime import datetime, date
from random import randint
import os

# --- Config ---
st.set_page_config(page_title="Facture GomaPochette3D", layout="centered")
st.image("logo.jpeg", width=150)
st.title("🧾 GÉNÉRATEUR DE FACTURE - GomaPochette3D")

model_options = {
    "iPhone": [
        "iPhone 15 Pro Max", "iPhone 15 Pro", "iPhone 15", "iPhone 15 Plus",
        "iPhone 14 Pro Max", "iPhone 14 Pro", "iPhone 14", "iPhone 14 Plus",
        "iPhone 13 Pro Max", "iPhone 13 Pro", "iPhone 13", "iPhone 13 Mini",
        "iPhone 12 Pro Max", "iPhone 12 Pro", "iPhone 12", "iPhone 12 Mini",
        "iPhone 11 Pro Max", "iPhone 11 Pro", "iPhone 11",
        "iPhone XS Max", "iPhone XS", "iPhone XR", "iPhone X",
        "iPhone 8 Plus", "iPhone 8", "iPhone 7 Plus", "iPhone 7", "iPhone SE (2020)", "iPhone SE (2022)"
    ],
    "Samsung": [
        "Galaxy S24 Ultra", "Galaxy S24+", "Galaxy S24",
        "Galaxy S23 Ultra", "Galaxy S23+", "Galaxy S23",
        "Galaxy S22 Ultra", "Galaxy S22+", "Galaxy S22",
        "Galaxy Note 20 Ultra", "Galaxy Note 20",
        "Galaxy Z Fold5", "Galaxy Z Flip5", "Galaxy Z Fold4", "Galaxy Z Flip4",
        "Galaxy A73", "Galaxy A72", "Galaxy A71", "Galaxy A70",
        "Galaxy A54", "Galaxy A53", "Galaxy A52", "Galaxy A51", "Galaxy A50",
        "Galaxy M54", "Galaxy M53", "Galaxy M52", "Galaxy M51",
        "Galaxy S21 FE", "Galaxy S20 FE"
    ],
    "Huawei": [
        "Mate 60 Pro", "Mate 50 Pro", "Mate 40 Pro", "Mate 30 Pro", "Mate 20 Pro", "Mate 10 Pro",
        "P60 Pro", "P50 Pro", "P40 Pro", "P30 Pro", "P20 Pro",
        "Nova 12 Pro", "Nova 11", "Nova 10", "Nova 9", "Nova 8i", "Nova 7i",
        "Y9s", "Y9 Prime", "Y8p", "Y7a", "Y6p", "Y5p"
    ],
    "Xiaomi": [
        "Xiaomi 14 Ultra", "Xiaomi 14 Pro", "Xiaomi 14",
        "Xiaomi 13 Ultra", "Xiaomi 13 Pro", "Xiaomi 13",
        "Mi 11 Ultra", "Mi 11 Pro", "Mi 11", "Mi 10T Pro", "Mi 10",
        "Redmi Note 13 Pro+", "Redmi Note 13 Pro", "Redmi Note 13",
        "Redmi Note 12 Pro+", "Redmi Note 12 Pro", "Redmi Note 12",
        "Redmi Note 11 Pro", "Redmi Note 11",
        "Poco F6 Pro", "Poco F6", "Poco X6 Pro", "Poco X6", "Poco X5 Pro", "Poco X5",
        "Poco M6 Pro", "Poco M5", "Poco C65", "Poco C55"
    ],
    "Autre": ["Autre"]
}

with st.form("form_facture"):
    nom = st.text_input("Nom du client")
    date_cmd = st.date_input("Date de commande", value=date.today())
    marque = st.selectbox("Marque de téléphone", list(model_options.keys()))
    modele = st.selectbox("Modèle", model_options[marque])
    prix_unitaire = st.number_input("Prix unitaire de la pochette ($)", min_value=1.0, step=0.5)
    quantite = st.number_input("Quantité", min_value=1, step=1, value=1)
    submitted = st.form_submit_button("✅ Générer la facture")

if submitted:
    prix_total = prix_unitaire * quantite
    id_facture = f"GP-{datetime.now().strftime('%Y%m%d')}-{randint(1000,9999)}"

    class FacturePDF(FPDF):
        def header(self):
            if os.path.exists("logo.png"):
                self.image("logo.png", 10, 8, 33)
            self.set_font("Arial", 'B', 14)
            self.cell(0, 10, "GomaPochette3D", ln=True, align='R')
            self.set_font("Arial", '', 10)
            self.cell(0, 10, "Adresse : Goma, RDC", ln=True, align='R')
            self.cell(0, 10, "WhatsApp : +243 975 582 294", ln=True, align='R')
            self.set_text_color(0, 0, 255)
            self.set_font("Arial", 'U', 10)
            self.cell(0, 10, "Instagram: https://www.instagram.com/pochette3dgoma", ln=True, align='R', link="https://www.instagram.com/pochette3dgoma")
            self.cell(0, 10, "TikTok: https://www.tiktok.com/@pochette3d.goma", ln=True, align='R', link="https://www.tiktok.com/@pochette3d.goma")
            self.cell(0, 10, "Facebook: https://www.facebook.com/pochette3dgoma", ln=True, align='R', link="https://www.facebook.com/pochette3dgoma")
            self.cell(0, 10, "WhatsApp: https://wa.me/243975582294", ln=True, align='R', link="https://wa.me/243975582294")
            self.set_text_color(0, 0, 0)
            self.ln(5)

        def footer(self):
            self.set_y(-15)
            self.set_font('Arial', 'I', 8)
            self.cell(0, 10, 'Merci pour votre commande ! / Thank you for your order!', 0, 0, 'C')

        def body(self, nom, date_cmd, marque, modele, prix_unitaire, quantite, prix_total, id_facture):
            self.set_font("Arial", 'B', 12)
            self.cell(0, 10, f"Facture N°: {id_facture}", ln=True)
            self.set_font("Arial", '', 12)
            self.cell(0, 10, f"Nom du client : {nom}", ln=True)
            self.cell(0, 10, f"Date : {date_cmd.strftime('%d/%m/%Y')}", ln=True)
            self.cell(0, 10, f"Marque/Modèle : {marque} - {modele}", ln=True)
            self.cell(0, 10, f"Prix unitaire : ${prix_unitaire:.2f}", ln=True)
            self.cell(0, 10, f"Quantité : {quantite}", ln=True)
            self.set_font("Arial", 'B', 12)
            self.cell(0, 10, f"Montant total : ${prix_total:.2f}", ln=True)
            self.ln(10)

            self.set_font("Arial", 'B', 11)
            self.cell(0, 10, "Résumé / Summary", ln=True)
            self.set_font("Arial", '', 11)
            self.multi_cell(0, 8, f"""Cette facture confirme l'achat de {quantite} pochette(s) personnalisée(s) pour {marque} {modele} au nom de {nom}. 
Merci pour votre confiance.

This invoice confirms the purchase of {quantite} customized phone case(s) for {marque} {modele} under the name of {nom}.
Thank you for choosing GomaPochette3D.""")

    pdf = FacturePDF()
    pdf.add_page()
    pdf.body(nom, date_cmd, marque, modele, prix_unitaire, quantite, prix_total, id_facture)

    file_name = f"Facture_{id_facture}.pdf"
    pdf.output(file_name)

    with open(file_name, "rb") as f:
        st.success(f"✅ Facture générée : {id_facture}")
        st.download_button("📄 Télécharger la facture PDF", f, file_name, mime="application/pdf")
