import streamlit as st
import pandas as pd
import numpy as np
import folium
import datetime

from streamlit_folium import st_folium
from datetime import datetime
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static

# Configuração na página toda
st.set_page_config(layout='wide')

def get_data(path):
    # Carrega o arquivo
    data = pd.read_csv( path )
    return data

def data_wipe(data):
    # remove ids duplicados
    data=data.drop_duplicates(subset=['id']) 

    # remove linhas com número de quartos fora do normal
    data=data[(data['bedrooms'] != 0) & (data['bedrooms'] != 11) & (data['bedrooms'] != 33)]

    # converte a coluna date de string para data
    data['date']=pd.to_datetime(data['date']).dt.strftime('%Y-%m-%d')

    # retira só o mês da coluna date
    data['Month'] = pd.DatetimeIndex(data['date']).month

    # cria a coluna de estação do ano e a popula conforme o período de compra
    data['seasonality']=data['Month'].apply(lambda x: 'spring' if (x >= 3) & (x < 6) else
                                                      'summer' if (x >= 6) & (x < 9) else
                                                      'fall' if (x >= 9) & (x < 12) else
                                                      'winter')
    # cria um novo dataframe com as colunas que iremos utilizar na análise
    data1 = data[['id','zipcode','date','waterfront','sqft_lot','bedrooms','condition',
                  'grade','price','seasonality','lat','long']].copy().rename(columns={'long': 'lon'})

    # calcula a mediana por código postal e salva na variável
    median_region=data[['price', 'zipcode']].groupby('zipcode').median().reset_index().rename(columns={'price':'median_price_region'})

    # junta a mediana da região por no dataframe1
    data1=pd.merge(data1, median_region, on='zipcode', how='inner')

    # cria a coluna status de preenche a recomendação relacionando o preço com a média da região e a condição
    data1['status']='NA'
    data1['status']=data1[['price', 'median_price_region', 'condition']].apply(lambda x: 'compra' if (x['price'] < x['median_price_region'])&(x['condition'] >=3) else 'não_compra', axis=1)

    # calcula a mediana por estação do ano e salva na variável
    median_seazon=data1[['price', 'seasonality']].groupby('seasonality').median().reset_index().rename(columns={'price': 'median_price_seazon'})

    # junta a mediana de estação do ano no dataframe1
    data1=pd.merge(data1, median_seazon, on='seasonality', how='inner')

    # calcula o preço de venda e insere na coluna 'sale_price'
    low_selling_price=1.1
    high_selling_price=1.3
    data1['sale_price']=data1[['price', 'median_price_seazon', 'median_price_region']].apply(lambda x: x['price'] * high_selling_price if (x['price'] <= x['median_price_seazon'])&(x['price'] <= x['median_price_region']) else x['price']*low_selling_price, axis=1)

    # calcula o lucro e insere na coluna profit
    data1['profit']=data1['sale_price']-data1['price']
    return data1

def filters (data1):
    # Títulos do dashboard                                                                                     
    st.title('Analise compra e venda-House Rocket')
    st.header('Compra e Venda')

    # Criação das colunas
    c1, c2 = st.columns((1,1))

    # Interação de filtro da coluna 1
    with c1:

        water_f = st.checkbox('De frente para o mar ?')
        sugest_compr=st.multiselect('Sugestão de compra', data1['status'].sort_values().unique(),'compra')
        filt_cond=st.multiselect('Condições do Imóvel', data1['condition'].sort_values().unique())
        filt_bed=st.multiselect('Quantidade de quartos', data1['bedrooms'].sort_values().unique())

    # Interação de filtro da coluna 2
    with c2:
        # Filtro de data 
        min_date=datetime.strptime(data1['date'].min(),'%Y-%m-%d')
        max_date=datetime.strptime(data1['date'].max(),'%Y-%m-%d')
        f_date = st.slider('Data de compra (ano-mes-dia)', min_date, max_date, max_date)
        # Filtro de preço de compra
        min_price=int(data1['price'].min())
        max_price=int(data1['price'].max())
        avg_price=int(data1['price'].min())
        f_price=st.slider('Preço de compra', min_price, max_price, max_price)
        # Filtro de preço de venda 
        min_sale_price=int(data1['sale_price'].min())
        max_sale_price=int(data1['sale_price'].max())
        avg_sale_price=int(data1['sale_price'].min())
        f_sale_price=st.slider('Preço de venda', min_sale_price, max_sale_price, max_sale_price)
        
    if water_f:
        water_check = data1[data1['waterfront'] == 1]
    else:
        water_check = data1.copy()

    water_check['date'] = pd.to_datetime(water_check['date'])
    filt_price = water_check.loc[(water_check['date'] <= f_date) &
                                 (water_check['price'] <= f_price) &
                                 (water_check['sale_price'] <= f_sale_price)]

    if (sugest_compr != []) & (filt_cond != []) & (filt_bed != []):
        f_compr = filt_price.loc[(filt_price['status'].isin(sugest_compr)) & 
                                 (filt_price['condition'].isin(filt_cond)) & 
                                 (filt_price['bedrooms'].isin(filt_bed)), :]
    elif (sugest_compr == []) & (filt_cond != []) & (filt_bed != []):
        f_compr = filt_price.loc[(filt_price['condition'].isin(filt_cond)) & 
                                 (filt_price['bedrooms'].isin(filt_bed)), :]
    elif (sugest_compr != []) & (filt_cond == []) & (filt_bed != []):
        f_compr = filt_price.loc[(filt_price['status'].isin(sugest_compr)) &  
                                 (filt_price['bedrooms'].isin(filt_bed)), :]
    elif (sugest_compr != []) & (filt_cond != []) & (filt_bed == []):
        f_compr = filt_price.loc[(filt_price['status'].isin(sugest_compr)) & 
                                 (filt_price['condition'].isin(filt_cond)),:]
    elif (sugest_compr == []) & (filt_cond == []) & (filt_bed != []):
        f_compr = filt_price.loc[(filt_price['bedrooms'].isin(filt_bed)),:]
    elif (sugest_compr != []) & (filt_cond == []) & (filt_bed == []):
        f_compr = filt_price.loc[(filt_price['status'].isin(sugest_compr)),:]
    elif (sugest_compr == []) & (filt_cond != []) & (filt_bed == []):
        f_compr = filt_price.loc[(filt_price['condition'].isin(filt_cond)),:]
    else:
        f_compr = filt_price.copy()
    return f_compr

# Visualização do dataframe e textos resumidos
def inform_down (inf_down):
    def style_text (text):
        st.markdown(f"<h2 style='text-align: left; padding:0px; font-size: {24}px;'>{text}</h2>",
                    unsafe_allow_html=True)
        return None
    def maps (inf_down):

        # Cria um mapa de fundo
        m = folium.Map(control_scale=True,location=[inf_down['lat'].mean(), inf_down['lon'].mean()],zoom_start=9)

        # Cria o plugin de clusterização
        marker_cluster = MarkerCluster().add_to(m)

        # Adicione os marcadores ao cluster
        for index, row in inf_down.iterrows():
            tooltip_text = f"ID: {row['id']}<br>Preço: US$ {row['price']:,.2f}<br>Preço de venda: US$ {row['sale_price']:,.2f}<br>Lucro: US$ {row['profit']:,.2f}"
            folium.Marker(location=[row['lat'], row['lon']],tooltip=tooltip_text).add_to(marker_cluster)

        # Adicione o mapa ao Streamlit
        folium_static(m)
        return None
    c3, c4 = st.columns((1,1))
    with c3:
        st.dataframe(inf_down, height=510)
        style_text('Total de imóveis: {}'.format(len(inf_down['id'])))
        style_text('Total da compra: US$ {:,.2f}'.format(sum(inf_down['price'])))
        style_text('Total da venda: US$ {:,.2f}'.format(sum(inf_down['sale_price'])))
        style_text('Lucro: US$ {:,.2f}'.format(sum(inf_down['profit'])))
        style_text('Preço médio de compra: US$ {:,.2f}*'.format(inf_down['price'].mean()))
        style_text('Preço mediano de compra: US$ {:,.2f}*'.format(inf_down['price'].median()))
        style_text('Preço médio de venda: US$ {:,.2f}*'.format(inf_down['sale_price'].mean()))
        style_text('Preço mediano de venda: US$ {:,.2f}*'.format(inf_down['sale_price'].median()))
        st.write('*Por imóvel')
    with c4:
        maps(inf_down)
        f_compr_percen=100*(sum(inf_down['profit'])/sum(inf_down['price']))
        percen="Lucro total de {:.2f}%".format(f_compr_percen)
        st.header(percen)
        @st.cache_data
        def convert_df(df):
            return df.to_csv().encode('utf-8')
        csv = convert_df(inf_down)
        st.download_button(label="Download to CSV", data=csv, file_name='large_df.csv', mime='text/csv',)
    return None    

if __name__ == "__main__":
    path = 'dataset/kc_house_data.csv'
    data = get_data(path)
    data1 = data_wipe(data)
    inf_down = filters(data1)
    inform_down(inf_down)