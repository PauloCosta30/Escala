import streamlit as st
import pandas as pd
import os

# Nome do arquivo Excel
FILE_NAME = "escala_lab.xlsx"

# Função para carregar ou criar o arquivo Excel
def load_data():
    if os.path.exists(FILE_NAME):
        return pd.read_excel(FILE_NAME)
    else:
        return pd.DataFrame(columns=["Data", "Período", "Sala", "Nome"])

# Função para salvar os dados no Excel
def save_data(df):
    df.to_excel(FILE_NAME, index=False)

# Carregar dados
escala = load_data()

st.title("Gerenciamento de Escala de Laboratório")

# Inputs do usuário
nome = st.text_input("Nome:")
data = st.date_input("Escolha a data:")
periodo = st.selectbox("Período:", ["Manhã", "Tarde"])
sala = st.selectbox("Sala:", ["Sala 1", "Sala 2", "Sala 3"]) 

# Verificar se a sala já está ocupada na data e período escolhidos
if st.button("Reservar"):
    if nome.strip() == "":
        st.warning("Por favor, insira seu nome.")
    else:
        if ((escala["Data"] == str(data)) & (escala["Período"] == periodo) & (escala["Sala"] == sala)).any():
            st.error("Essa sala já está ocupada nesse período e data.")
        else:
            # Adicionar a reserva
            nova_reserva = pd.DataFrame({"Data": [str(data)], "Período": [periodo], "Sala": [sala], "Nome": [nome]})
            escala = pd.concat([escala, nova_reserva], ignore_index=True)
            save_data(escala)
            st.success("Reserva realizada com sucesso!")

# Exibir tabela com reservas
st.subheader("Escala Atual")
st.dataframe(escala)