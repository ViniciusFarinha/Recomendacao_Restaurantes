import streamlit as st
import pickle
from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
import os



st.set_page_config(page_title='Recomenda Restaurantes')
csv_path = 'Recomendacao_Restaurantes/examples/df_recomend.csv'

def load_data(url):
    df_recomend = pd.read_csv(url)  # 👈 Download the data
    return df_recomend

df_recomend = load_data("https://raw.githubusercontent.com/ViniciusFarinha/Recomendacao_Restaurantes/main/examples/df_recomend.csv")
st.dataframe(df_recomend)



# Elementos de Texto
st.markdown('# Recomendação de Restaurantes')
st.markdown('##### **Olá, este é meu programa de recomendação de restaurantes! Se você está interessado em conhecer lugares novos similares aos que você já gosta, experimente o programa abaixo!**')

#Imagem--------------------------------
# Defina o caminho da imagem
image_path = 'Recomendacao_Restaurantes/Images/yelp.jpg'

try:
    # Use 'with open' para abrir a imagem
    with open(image_path, 'rb') as file:
        # Abra a imagem com o módulo PIL (Pillow)
        image = Image.open(file)

        # Exiba a imagem no aplicativo Streamlit
        st.image(image)
except FileNotFoundError as e:
    print(f"O arquivo {image_path} não foi encontrado.")
    print(f"Detalhes do erro: {e}")
except Exception as e:
    print(f"Ocorreu um erro ao abrir a imagem {image_path}.")
    print(f"Detalhes do erro: {e}")
# ------------------------------------------------
st.markdown('**Diga o seu nome e escolha um restaurante que você gosta**')


# -----Model-----------------------------

# Defina o caminho do arquivo pickle
pickle_path = 'Recomendacao_Restaurantes/examples/grafo_modelo.pkl'

try:
    # Use 'with open' para abrir o arquivo pickle
    with open(pickle_path, 'rb') as model_file:
        # Leia o conteúdo do arquivo pickle
        G = pickle.load(model_file)
except FileNotFoundError as e:
    print(f"O arquivo {pickle_path} não foi encontrado.")
    print(f"Detalhes do erro: {e}")
except Exception as e:
    print(f"Ocorreu um erro ao abrir o arquivo {pickle_path}.")
    print(f"Detalhes do erro: {e}")

#-----------------------------------

def pesquisa_restaurante(restaurant_name, G, df_recomend):
    
    # Encontrando o ID do restaurante com base no nome
    restaurant_ids = df_recomend[df_recomend['name'] == restaurant_name]['id'].unique()
    if not restaurant_ids:
        return [], []
    restaurant_id = restaurant_ids[0]

    # Encontrando os usuários que avaliaram o restaurante
    neighbors = list(G.neighbors(restaurant_id))
    user_consumed_rest = []

    # Para cada usuário, encontrar os restaurantes que ele avaliou
    for user_id in neighbors:
        user_consumed = list(G.neighbors(user_id))
        user_consumed_rest += user_consumed

    # Remover o restaurante original da lista
    user_consumed_rest = [rest for rest in user_consumed_rest if rest != restaurant_id]

    # Contagem de restaurantes para Score
    restaurant_count = Counter(user_consumed_rest)

    # Filtrando os nomes dos restaurantes recomendados
    recommended_restaurant_ids = list(set(user_consumed_rest))
    recommended_restaurants = df_recomend[df_recomend['id'].isin(recommended_restaurant_ids)]['name'].unique().tolist()

    # Criando a pontuação dos restaurantes
    Score_restaurants = [(rest, restaurant_count[rest_id]) for rest, rest_id in zip(recommended_restaurants, recommended_restaurant_ids)]

    return recommended_restaurants, Score_restaurants


restaurantes = ['Aprazível',
 'Braseiro',
 'NOSSO',
 'Ferro e Farinha',
 'Nomangue',
 'Churrascaria Palace',
 'Teva',
 'Haru Sushi Bar',
 'Cervantes',
 'Garota de Ipanema',
 'Via Sete',
 'Oteque',
 'Marius Degustare',
 'El Born',
 'Lasai',
 'ORO',
 'TT Burger',
 'Grado',
 'Pérgula',
 'CT Boucherie',
 'Santa Satisfação',
 'Artigiano',
 'Puro',
 'Pici Trattoria',
 'Otto Bar e Restaurante',
 'Zazá',
 'Tragga',
 'Tacacá do Norte',
 'Joaquina',
 'Rotisseria Sírio Libaneza',
 'CoLAB',
 'A Polonesa',
 'Fat Choi',
 'Filé de Ouro',
 'ino.',
 'Prana Vegetariano',
 'Malta Beef Club',
 'Zuka',
 'Mauá',
 'Amir',
 'Restaurante Broth',
 'Quadrucci',
 'Gabbiano',
 'Miam Miam',
 'Comuna',
 'Bar Astor',
 'Rubaiyat Rio',
 'Maè Noi',
 "L'etoile",
 'Alfaia',
 'Porta do Sol',
 'Space Storm',
 'Giuseppe Grill',
 'Bar do Horto',
 'Antiquarius',
 'SUD - O Pássaro Verde Café',
 'Bucaneiros',
 'Pomodorino',
 'Casa do Sardo',
 "L'Atelier Mimolette",
 'Adegão Português',
 'Restaurante Siri',
 'Rian',
 'Bar Urca',
 'Irajá Gastrô',
 'Nova Capela',
 'Braseiro da Gávea',
 'Espaço 7zero6',
 'Cantina da Praça',
 'Barraca da Chiquita',
 'Eleven Rio',
 'Quitéria',
 'Massa',
 'Veggie Govinda',
 'Gurumê Ipanema',
 'Manoel e Juaquim',
 'Lima Restobar',
 'Le Blé Noir',
 'Dom Cavalcanti',
 'Gracioso',
 'Yeasteria Ponto Cervejeiro',
 'Aconchego Carioca',
 'Azteka',
 'Botequim Informal',
 'Aloha',
 'Bar do Mineiro',
 'La Carioca Cevicheria',
 'Mamma Jamma',
 'Empório Grão e Cia',
 'Bangalô',
 'Casa da Suíça',
 'Cais do Oriente',
 'Estação Baião de Dois',
 'La Bocca',
 'Olympe',
 'Hachiko',
 'Mr. Lam',
 "Galeto Sat's",
 'Restaurante Shirley',
 "L'atelier du Cuisinier",
 'Casa Momus',
 'Carmelo',
 'A Marisqueira',
 'Felice Terrazza',
 'La Villa',
 'Galetos Copa Rio',
 'New Natural',
 'Restaurante Mosteiro',
 'Restaurante Sá',
 'Vikings',
 'Capitão Jacques',
 "Luigi's",
 'Hollandaise',
 'Eça',
 'Pabu Izakaya',
 'Naturalie Bistrô',
 'Martinez',
 'Cipriani',
 'Posí',
 'Cantina Donanna',
 'Boteco Belmonte',
 'Tango',
 'Restaurante Meu Cantão',
 'Fratelli',
 'Lorenzo Bistrô',
 'Espírito Santa Restaurante',
 'Julius Brasserie',
 'Miako Culinária Japonesa',
 'Mercearia da Praça',
 "L'Ulivo Cucina e Vini",
 'B de Burger',
 'Manoel & Juaquim',
 'Nam Thai',
 'Yumê',
 'Riso Bistrô',
 'Adega Perola',
 'Gurumê Fashion Mall',
 'Meza Bar',
 'Cachambeer',
 'Armazém São Thiago - Bar do Gomez',
 'Noi',
 'Café Lamas',
 'Terra Brasilis',
 'Sushi Leblon',
 'Mitsuba',
 'Chez Claude',
 'Camolese',
 'Zacks',
 'Degrau',
 'Le Vin Bistro',
 'Azur',
 "L'Entrecôte de Paris",
 'Restaurante da Praça',
 'Fellini Restaurante',
 'Mangue Seco',
 'Da Brambini',
 'Sushi Akyrio',
 'Térèze',
 'Delírio Tropical',
 'Frédéric Epicerie',
 'Galli',
 'Bingo',
 'Mironga',
 'Qué Quieres',
 'Casa do Filé',
 'Casa Carandaí',
 'O Crack dos Galetos',
 'Na Brasa Colúmbia',
 'Bacalhau & Cia',
 'Pensão da Nonna',
 'La Carmelita',
 'Restaurante Garagem 60',
 'Restaurante Galeto Castelo',
 'Assis Garrafaria',
 'Rosty',
 'Da Cozinha Café',
 'Da Roberta',
 'Filet e Folhas',
 'Vokos Grego',
 'Restaurante OJO',
 'La Trattoria',
 "Ekko's",
 'Severyna Ponto Como',
 'Restaurante VAMO',
 'O Caranguejo Restaurante',
 'Mee',
 'Bar Bracarense',
 'Rolé',
 'Taj Mahal Restaurante',
 'Benza!',
 'Empório Jardim',
 'Bar Sobe',
 'Rústico',
 'Bazzar à Vins',
 'Winehouse',
 'Majorica',
 'Bistrô Ouvidor',
 "Chez L'ami Martin",
 'Carioca da Gema',
 'Gula Gula',
 'Pulê Restaurante e Bar',
 'Mitsuo Japinha',
 'Puro Sabor de Ipanema',
 'Bar do David',
 'Guacamole',
 'Oscar',
 'Da Laje',
 'Salitre',
 'Alessandro & Frederico',
 'Gaia Art & Café',
 'Cortiço Carioca',
 'Beco do Hamburguer',
 'Rota 66',
 'O Peixe Vivo',
 'Djalma Burger Bistrô',
 'Alloro al Miramar',
 'Zona Zen',
 'Cortés',
 'Caverna',
 'Stalos',
 'Guimas Restaurante',
 'La Nave',
 'Severyna de Laranjeiras',
 'Plage Café',
 'Las Vegans',
 'Armazém Cardosão',
 'Le Blond',
 'La Mole',
 'Rancho Português',
 'Sindicato do Arpoador',
 'Papa Fina',
 'Café do Alto',
 'Azumi',
 'Carretão',
 'Galeto & Cia',
 'Food Truck Mosteirinho',
 'Bacalhau do Rei',
 'Mamma Rosa',
 'Botequim dos Amigos',
 'Org Bistrô',
 'Galeto do Leblon',
 'Granola',
 'O Bom Galeto',
 'Beluga',
 'Petit',
 'La Bicyclette',
 'Hanguk House',
 'Bar do Arnaudo',
 'Formidable',
 'Ginger Mamut',
 'Príncipe de Mônaco',
 'SAL',
 'Naga',
 'Êtta',
 'Espaço Pura Vida',
 'Conexão Mandacarú',
 'Armazém 331',
 'Cantina do Gaúcho',
 'Gutessen',
 'Estrelas da Babilônia',
 'Steak Me',
 'Zaza Café',
 'Birreria Escondido',
 'Canastra',
 'Salomé Bistrô',
 'Capricciosa',
 'Fasano al Mare',
 'Majestade',
 'Restaurante Demi-Glace',
 'Joaquina Bar & Restaurante',
 'Restaurante Escondidinho',
 'La Maison',
 "Hell's Burguer",
 'Pappa Jack',
 'Prima Bruschetteria',
 'Adega do Pimenta',
 "Assador Rio's",
 'Pizzaria do Chico',
 'Cedro do Líbano',
 'Os Ximenes',
 'Rainha',
 'Seu Vidal',
 'Venga!',
 'Stambul Comida Árabe',
 'Grand Cru',
 'Botequim Casual',
 'Pobre Juan',
 'Bier en Cultuur',
 'O Nosso Churrasqueto',
 'La Fiorentina',
 'Da Silva',
 'Corrientes 348',
 'Jappa',
 'Mega Matte',
 'Restaurante da Vinci',
 'Skinna Restaurante',
 'Epifania',
 'Famous Burger',
 'Botequim Vaca Atolada',
 'Simon Boccanegra',
 'Venga',
 'Zee Champanheria',
 'Tacos and Wraps',
 'Bio Carioca',
 "Canto d'Alice",
 'Bráz Pizzaria',
 'Jack Salada',
 'Portella',
 'Lopes',
 'Camelo',
 'Feyzi',
 'Da Casa da Táta',
 'Cozinha Artagão',
 'La Sagrada Família',
 'SoHo',
 'Baalbek',
 'Bistrô da Ponte',
 'Restaurante Via Farani',
 'LapaMaki',
 'HOB Hamburgueria',
 'Mr Trip Rock Bar',
 'Bar Brasil',
 'Roberta Sudbrack',
 'I Piatti',
 'Anna Ristorante',
 'Bagatelle',
 'Intihuasi',
 'RIBA',
 'Flambée',
 'Italian Comfort BBQ',
 'Broz',
 'Das Chefs Restaurante',
 'Estação Toledo',
 'Os Imortais',
 'Serdani',
 'Bar do Cícero',
 'Bar do Lado',
 'Galitos Grill',
 'Gero',
 'Natu Sucos',
 'Rio Park Lanches Bar',
 'Restaurante Nativo',
 'Pizzaria Caravelle',
 'Brasinha Ipanema Galeto',
 'Pavelka',
 'Balada Mix',
 'Improviso',
 'Churrascaria Carretão',
 'Arpô Restobar',
 'Confeitaria Colombo',
 'Ráscal',
 'Clássico Beach Club Urca',
 'Nori Cozinha Oriental',
 'Japa B',
 'Lapamaki Ipanema',
 'Angu do Gomes',
 'Paris 6',
 'Casa Graviola',
 'Faenza',
 'Garota',
 'Bar Tropeço',
 "Habib's Quiosque",
 'Madero',
 'Caravela do Visconde',
 'Kimura Culinária Japonesa',
 'Meating Homemade',
 'Capadócia',
 'Banana Tropical',
 'Lapamaki',
 'Seu Pires',
 'Verdin',
 'Restaurante Os Esquilos',
 'San Izakaya',
 'Don Camillo',
 'Frederico',
 'Outback Steakhouse',
 'Cultivar Brasil',
 'Yosuki',
 'Faraj',
 'Cantinho Cearense',
 'Restaurante Berbigão',
 'Joana Pizza Bar',
 "Antica Osteria dell'Angolo",
 'Oliva',
 'Sobrenatural',
 'Gabbiano Al Mare',
 'Pomodoro',
 'Clara Café',
 'Adega Portugália',
 'Gallo Carioca',
 'Pizzeria La Mamma',
 'Buda Sushi',
 'D.R.I',
 'Bar e Restaurante Bismarque',
 'Taberna Atlântica',
 'Spaghettilândia',
 'Metrópole',
 "Restaurante Maxim's",
 'Talho',
 'Laguna',
 'Kaiten Sushi Bar',
 'Casa da Ostra',
 'Reserva T.T. Burger',
 'Fórmula 1',
 'Bar D´Hôtel',
 'Fazendola']



# Widgets

# Layout com colunas para entrada de nome e seleção de restaurante
col1, col2 = st.columns(2)
with col1:
    nome = st.text_input('Qual o seu nome?', key='nome')
    if nome:  # Somente mostrar a mensagem de prazer se o nome for inserido
        st.write(f'Prazer, {nome}!')
with col2:
    restaurantes = df_recomend['name'].unique().tolist()  # Supondo que 'df_recomend' é seu dataframe
    restaurant_name = st.selectbox('Qual restaurante você gosta?', options=restaurantes)

if st.button('Me Recomende!'):
    if nome and restaurant_name:
        recomendacoes, scores = pesquisa_restaurante(restaurant_name, G, df_recomend)
        # Filtrar df_recomend para obter as informações dos restaurantes recomendados
        info_recomendacoes = df_recomend[df_recomend['name'].isin(recomendacoes)][['name','category' ,'rating', 'price']].drop_duplicates()
        if recomendacoes:
            st.markdown(f'#### As pessoas que gostam de _{restaurant_name}_ também costumam gostar de:')
            for _, row in info_recomendacoes.iterrows():
                cols = st.columns([2, 1, 1, 1])
                with cols[0]:
                    st.markdown(f"**{row['name']}**")
                with cols[1]:
                    st.markdown(f"**Rating:** {row['rating']}")
                with cols[2]:
                    st.markdown(f"**Preço:** {'$' * int(row['price'])}")
                with cols[3]:                       
                    st.markdown(f"**Categoria:** { (row['category'])}")
            
                # Apresentar contagens com estilo
            st.markdown("#### Contagem de Recomendações por usuário:")
            st.dataframe(pd.DataFrame(scores, columns=['Restaurante', 'Contagem']))

            sentimentos = df_recomend['sentiment']  # Substitua 'sentiment' pela coluna relevante
            sentimento_medio = sentimentos.mean()
            sentimento_escolhido = df_recomend[df_recomend['name'] == restaurant_name]['sentiment'].iloc[0]
            
            st.markdown(f'#### Gráfico de sentimento:')
            st.write('O sentimento é uma medida feita a partir das reviews dos usuários. Quanto mais próxima de 1, mais positiva.Quanto mais próxima de -1, pior.')
            
            # Criando o gráfico
            fig, ax = plt.subplots()
            ax.barh(['Sentimento Médio dos Restaurantes', restaurant_name], [sentimento_medio, sentimento_escolhido], color=['blue', 'red'])
            ax.set_xlabel('Sentimento')
            st.pyplot(fig)
            
            st.markdown(f'###### O sentimento de _{restaurant_name}_ é {sentimento_escolhido} referente à média de sentimentos {sentimento_medio}:')
        else:
            st.error(f"Desculpe, não encontramos recomendações para o restaurante '{restaurant_name}'.")
    else:
        st.warning("Por favor, informe o seu nome para continuar.")


#Imagem

image2 = Image.open('Recomendacao_Restaurantes\Images\Logo.jpg')

st.image(image2)




st.markdown('##### Este programa foi criado utilizando os dados da Yelp. Portanto, os dados utilizados para a criação do modelo são escassos, dado que a API da empresa permite poucas requests. Apesar disso, o modelo se comporta muito bem. Aproveite!')

st.markdown('##### Caso queira conhecer mais sobre o trabalho te convido à conhecer meu GitHub e LinkedIn:')

st.markdown('#### [![Portfolio](https://img.shields.io/badge/Portfolio-FF5722?style=for-the-badge&logo=todoist&logoColor=white)]( https://viniciusfarinha.my.canva.site/)')
st.markdown('#### [![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/ViniciusFarinha)')
st.markdown('####  [![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/viniciusfarinha)')