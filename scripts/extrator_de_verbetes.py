import os
import pandas as pd
import re

# Obter o diretório do script atual
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construir caminhos relativos ao script atual
data_dir = os.path.join(script_dir, os.pardir, 'data')
treated_dir = os.path.join(data_dir, 'treated')
output_dir = os.path.join(data_dir, 'output')

# Caminhos dos arquivos
sinonimos_file_path = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vSu6wT2iL175IvTqD0TF1kIKt-GHnPOXcBuJHAGfxW-vNgpfQjV6tNDO2fuKvcggkFyAVljIKQZKiPw/pub?gid=135196774&single=true&output=csv'
links_file_path = os.path.join(treated_dir, 'links_wikilai.csv')
output_file_path = os.path.join(output_dir, 'newsletter_com_links.txt')


def extrair_verbetes(verbetes_raspados, texto_newsletter):
    """
    Adiciona as tags <a> na primeira ocorrência dos verbetes da WikiLai 
    que aparecem no texto da newsletter. 

    Retorna:
        DataFrame: Um DataFrame contendo o texto com os links.
        
    """
           
    verbetes_sinonimos = pd.read_csv(sinonimos_file_path, sep=',')
    todos_os_verbetes = pd.concat([verbetes_raspados, verbetes_sinonimos], ignore_index=True)
        
    for index, row in todos_os_verbetes.iterrows():
        verbete = row['verbete']
        href = row['link']
        regex = r'\b' + re.escape(verbete) + r'\b'
        texto_newsletter, _ = re.subn(regex, f'<a href="{href}">{verbete}</a>', texto_newsletter, count=1, flags=re.IGNORECASE)

    print('Extraindo verbetes do texto.')
    return texto_newsletter



def limpar_links_duplicados(texto_newsletter):
    """
    Remove tags <a> duplicadas que contêm o mesmo href no texto da newsletter.
    
    Parâmetros:
        texto_newsletter (str): O texto da newsletter após a substituição dos verbetes pelos links.
    
    Retorna:
        str: O texto da newsletter com tags <a> duplicadas removidas.
    """
    hrefs_encontrados = {}
    regex_links = re.compile(r'<a href="(.*?)">(.*?)</a>')

    def substituir_duplicados(match):
        href, texto = match.groups()
        if href in hrefs_encontrados:
            return texto
        hrefs_encontrados[href] = True
        return match.group(0)

    texto_newsletter_limpo = regex_links.sub(substituir_duplicados, texto_newsletter)
    
    return texto_newsletter_limpo
