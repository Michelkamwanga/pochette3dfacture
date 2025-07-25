import streamlit as st
from fpdf import FPDF
from datetime import datetime, date
from random import randint
import os

st.set_page_config(page_title="Facture GomaPochette3D", layout="centered")
st.image("logo.jpeg", width=150)
st.title("🧾 GÉNÉRATEUR DE FACTURE - GomaPochette3D")

# Liste des marques
marques = ["iPhone", "Samsung", "Huawei", "Xiaomi", "Autre"]

nom = st.text_input("Nom du client")
date_cmd = st.date_input("Date de commande", value=date.today())

marque = st.selectbox("Marque de téléphone", marques)

# Champ texte libre pour saisir le modèle
modele = st.text_input("Modèle du téléphone (ex: Galaxy S22 Ultra, iPhone 14 Pro, etc.)")

prix_unitaire = st.number_input("Prix unitaire de la pochette ($)", min_value=1.0, step=0.5)
quantite = st.number_input("Quantité", min_value=1, step=1, value=1)

if st.button("✅ Générer la facture"):
    if not nom.strip():
        st.error("Merci de saisir le nom du client.")
    elif not modele.strip():
        st.error("Merci de saisir le modèle du téléphone.")
    else:
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
