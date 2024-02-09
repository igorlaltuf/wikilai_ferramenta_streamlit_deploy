import os
import requests
from bs4 import BeautifulSoup
import pandas as pd

def raspar():
    """
    Raspa dados da página de "Todas as páginas" da WikiLai e salva em um arquivo CSV.
    
    Retorna:
        DataFrame: Um DataFrame contendo os verbetes e os links raspados da WikiLai.
        
    Efeitos colaterais:
        Salva um arquivo 'links_wikilai.csv' no diretório 'data/treated' com os dados raspados.
    """
    
    diretorio_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    caminho_arquivo_destino = os.path.join(diretorio_base, 'data', 'treated', 'links_wikilai.csv')

    # Raspar dados da WikiLai
    url = 'https://wikilai.fiquemsabendo.com.br/wiki/Especial:Todas_as_p%C3%A1ginas'  # Página com verbetes

    resposta = requests.get(url)

    if resposta.status_code == 200:
        soup = BeautifulSoup(resposta.content, 'html.parser')
        
        links = soup.select('ul.mw-allpages-chunk li a')
        
        dados = []
        
        for link in links:
            title = link.get('title')
            href = 'https://wikilai.fiquemsabendo.com.br' + link.get('href')
            dados.append([title, href])
        
        df = pd.DataFrame(dados, columns=['verbete', 'link'])
        
        df.to_csv(caminho_arquivo_destino, sep=';', index=False)
        
        print("Arquivo 'links_wikilai.csv' salvo com sucesso no diretório:", caminho_arquivo_destino)
        
        return df
    
    else:
        print("Falha ao acessar a página:", resposta.status_code)
        
        return pd.DataFrame()