import streamlit as st
from scripts.raspador_da_wikilai import raspar
from scripts.extrator_de_verbetes import extrair_verbetes, limpar_links_duplicados

if 'df_verbetes' not in st.session_state:
    st.session_state.df_verbetes = raspar()
    print('Dados raspados com sucesso.')

st.title('Ferramenta de Links da WikiLAI')
st.write('Esta é a ferramenta da Fiquem Sabendo para adicionar os links referentes aos verbetes da WikiLAI ao texto inserido na caixa de texto abaixo. \
         Também é possível adicionar manualmente os links por meio do seguinte [arquivo](https://docs.google.com/spreadsheets/d/1eL56U-RMZPI7JPmOo08aEp9zQ1bNkE1erV0tf5KQzZc/edit#gid=135196774).')

texto_usuario = st.text_area("Insira o texto da newsletter aqui:", height=600)


if st.button('Adicionar os links ;)'):

    st.write('Texto formatado com links:')
    
    texto_formatado = extrair_verbetes(st.session_state.df_verbetes, texto_usuario)
    
    texto_formatado = limpar_links_duplicados(texto_formatado)
    
    st.markdown(texto_formatado, unsafe_allow_html=False)