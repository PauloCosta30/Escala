import streamlit
import pandas
import openpyxl
import streamlit as st
import pandas as pd
import os


import streamlit as st
import pandas as pd
import io  # Para salvar o Excel na memória

FILE_NAME = "escala_lab.xlsx"

# Carregar dados
def load_data():
    try:
        return pd.read_excel(FILE_NAME)
    except FileNotFoundError:
        return pd.DataFrame(columns=["Data", "Período", "Sala", "Nome"])

# Salvar dados
def save_data(df):
    df.to_excel(FILE_NAME, index=False, engine="openpyxl")

# Carregar a escala
escala = load_data()

st.title("Gerenciamento de Escala de Laboratório")

# Criar um buffer de memória para salvar o Excel antes de baixar
output = io.BytesIO()
with pd.ExcelWriter(output, engine="openpyxl") as writer:
    escala.to_excel(writer, index=False)
output.seek(0)

# Botão para baixar o Excel
st.download_button(
    label="Baixar Planilha",
    data=output,
    file_name="escala_lab.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
)

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