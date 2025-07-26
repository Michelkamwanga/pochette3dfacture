import streamlit as st
from fpdf import FPDF
from datetime import datetime, date
from random import randint
import os
import urllib.parse

st.set_page_config(page_title="Facture GomaPochette3D", layout="centered")
st.image("logo.jpeg", width=150)
st.title("🧾 GÉNÉRATEUR DE FACTURE - GomaPochette3D")

# Modèles des marques (version réduite ici, à compléter selon besoin)
model_options = {
    "iPhone": ["iPhone 15 Pro Max", "iPhone 15 Pro", "iPhone 15", "iPhone 15 Plus",
        "iPhone 14 Pro Max", "iPhone 14 Pro", "iPhone 14", "iPhone 14 Plus",
        "iPhone 13 Pro Max", "iPhone 13 Pro", "iPhone 13", "iPhone 13 mini",
        "iPhone 12 Pro Max", "iPhone 12 Pro", "iPhone 12", "iPhone 12 mini",
        "iPhone SE (2022)", "iPhone 11 Pro Max", "iPhone 11 Pro", "iPhone 11",
        "iPhone XR", "iPhone XS", "iPhone XS Max", "iPhone X", "Autre"],
    "Samsung": ["Galaxy S24 Ultra", "Galaxy S24+", "Galaxy S24",
        "Galaxy S23 Ultra", "Galaxy S23+", "Galaxy S23",
        "Galaxy S22 Ultra", "Galaxy S22+", "Galaxy S22",
        "Galaxy A54", "Galaxy A34", "Galaxy A14",
        "Galaxy Note 20 Ultra", "Galaxy Note 20",
        "Galaxy Z Fold 5", "Galaxy Z Flip 5",
        "Galaxy S21 Ultra", "Galaxy S21+",
        "Galaxy M14", "Autre"],
    "Huawei": ["P60 Pro", "P60", "P50 Pro", "P50",
        "Mate 40 Pro", "Mate 40", "Mate 30 Pro", "Mate 30",
        "Nova 10 Pro", "Nova 9",
        "Y9 Prime",
        "Honor 70", "Autre"],
    "Xiaomi": ["Redmi Note 13", "Poco X6", "Mi 11", "Autre"],
    "Autre": ["Autre"]
}

# Champs utilisateur
nom = st.text_input("👤 Nom du client")
numero_client = st.text_input("📞 Numéro WhatsApp du client (ex: 24397XXXXXXX)")
date_cmd = st.date_input("📅 Date de commande", value=date.today())
marque = st.selectbox("📱 Marque de téléphone", list(model_options.keys()))
modele_selectionne = st.selectbox("📲 Modèle", model_options[marque])

# Saisie manuelle si "Autre"
if modele_selectionne == "Autre":
    modele = st.text_input("✏️ Saisir le modèle manuellement")
else:
    modele = modele_selectionne

prix_unitaire = st.number_input("💵 Prix unitaire ($)", min_value=1.0, step=0.5)
quantite = st.number_input("🔢 Quantité", min_value=1, step=1, value=1)

# Génération
if st.button("✅ Générer la facture"):
    prix_total = prix_unitaire * quantite
    id_facture = f"GP-{datetime.now().strftime('%Y%m%d')}-{randint(1000,9999)}"

    class FacturePDF(FPDF):
        def header(self):
            if os.path.exists("logo.jpeg"):
                self.image("logo.jpeg", 10, 8, 33)
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

        def body(self, nom, numero, date_cmd, marque, modele, prix_unitaire, quantite, prix_total, id_facture):
            self.set_font("Arial", 'B', 12)
            self.cell(0, 10, f"Facture N°: {id_facture}", ln=True)
            self.set_font("Arial", '', 12)
            self.cell(0, 10, f"Nom du client : {nom}", ln=True)
            self.cell(0, 10, f"Téléphone : +{numero}", ln=True)
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
    pdf.body(nom, numero_client, date_cmd, marque, modele, prix_unitaire, quantite, prix_total, id_facture)

    file_name = f"Facture_{id_facture}.pdf"
    pdf.output(file_name)

    with open(file_name, "rb") as f:
        st.success(f"✅ Facture générée : {id_facture}")
        st.download_button("📄 Télécharger la facture PDF", f, file_name, mime="application/pdf")

    # Message WhatsApp pré-rempli
    message = f"Bonjour {nom}, voici votre facture N° {id_facture} pour votre commande de {quantite} pochette(s) {marque} {modele}.\nMontant total : ${prix_total:.2f}.\nMerci pour votre confiance !"
    encoded_message = urllib.parse.quote(message)
    whatsapp_url = f"https://wa.me/{numero_client}?text={encoded_message}"
    st.markdown(f"[📤 Envoyer la facture via WhatsApp]({whatsapp_url})", unsafe_allow_html=True)
