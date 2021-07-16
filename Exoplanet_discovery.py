import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier


@st.cache
def load_df(url):
    df = pd.read_csv(url)
    return df


# option
st.set_page_config(page_title="Exoplanet Discovery",
                   page_icon="🚀",
                   layout="wide",
                   initial_sidebar_state="expanded")


#############
## sidebar ##
############# 

st.sidebar.title('Exoplanet Discovery')
st.sidebar.subheader('Navigation')

categorie = st.sidebar.radio("Categories", ("Accueil", "Observer les Exoplanètes",
                                            "Les Exoplanètes habitables",
                                            "L'IA à l'aide des Astrophysicien"))

st.sidebar.title(' ')
option = st.sidebar.beta_expander("Options")
option.markdown(
    """
    L'option _Montre moi la data_ affichera les données 
    qui ont permis de réaliser les graphiques, sous forme de tableaux. 
    """)
show = option.checkbox('Montre moi la data')

expander = st.sidebar.beta_expander("Sources")
expander.markdown(
    """
    __Les bases des données utilisées__ : 

    [NASA Exoplanet Archives](https://exoplanetarchive.ipac.caltech.edu/cgi-bin/TblView/nph-tblView?app=ExoTbls&config=PS) : 
    Data brutes sur les exoplanètes et leur système solaire.

    [Planetary Habitability Laboratory](http://phl.upr.edu/projects/habitable-exoplanets-catalog/data/database) : 
    Détermine quelles sont les exoplanètes habitables ou inhabitables.
    """)

expander.info('Résiliation des **Pirates Ducks** : _Antoine, Franck, Michaël, Mickaël_')
expander.info('Hackathon organisé par la **WildCodeSchool** le 12/05/2021')


##########
## DATA ##
##########

# modifier selon la localisation de la BD
phl_db = 'http://www.hpcf.upr.edu/~abel/phl/hec2/database/phl_exoplanet_catalog.csv'
nea_db = 'https://raw.githubusercontent.com/MickaelKohler/Exoplanet_Discovery/main/planets.csv'

planets = load_df(nea_db)
plan_hab = load_df(phl_db)


###############
## MAIN PAGE ##
###############

if categorie == 'Accueil':
    st.title('Exoplanet Discovery')
    st.subheader('Notre mission : _Donner vie à la data_')

    st.markdown(
        """
        Fermi était septique :

        _« S'il y avait des civilisations extraterrestres, leurs représentants 
        devraient être déjà chez nous. Où sont-ils donc ? »_
        
        Si la question n'a pas de réponse, c'est le principe même de ce paradoxe, 
        elle souligne tout de même la volonté qu'à l'homme de pouvoir rencontrer son alter-égo.

        Si ce n'est pas des civilisations extraterrestres qui nous ont trouvé, alors c'est à nous de les chercher. 
        Les pieds sur terre, la tête dans les étoiles. Nous scrutons le ciel pour 
        trouver une terre qui nous ressemble. Ce sont les _Exoplanètes_.
        """
    )

    col1, col2 = st.beta_columns(2)
    with col1:
        st.title(" ")
        st.markdown(
            """
            Il faut attendre __1995 pour que la première exoplanète apparaisse__ devant nos yeux et 
            relance la course à la recherche de la vie. Mars n’est plus le seul horizon. 
            L’espoir se propage à présent jusqu’au confins de l’univers.

            C’est aujourd’hui __4383 exoplanètes__ qui ont été découvertes. 

            Dans ce total toutefois, seulement __moins de 1,5% sont considérées remplissant 
            suffisamment de conditions pour accueillir une forme de vie__. 
            """
        )
    with col2:

        temp_tab = planets.groupby((planets['disc_year'] // 10) * 10).count()
        decad_disc = temp_tab[['pl_name']].rename(columns={'pl_name': 'Découvertes'})
        decad_disc['Augmentation'] = ''
        for i in range(1, 5):
            decad_disc.iloc[i, 1] = (((decad_disc.iloc[i, 0] - decad_disc.iloc[i-1, 0]) / decad_disc.iloc[i-1, 0]) * 100).round()

        fig = px.bar(decad_disc, x=decad_disc.index, y="Découvertes", 
                     title="Evolution du nombre d'exoplanètes découvertes",
                     text='Augmentation',
                     color_discrete_sequence=['darkblue']*len(decad_disc))
        fig.update_traces(texttemplate='%{text:.2s}%')
        fig.update_layout(showlegend=True, font_family='IBM Plex Sans', title_x=0.5,
                          xaxis=dict(title="Pourcentage d'évolution d'une décénnie sur l'autre"),
                          yaxis=dict(title="Nombre d'exoplanètes découvertes"),
                          uniformtext_minsize=10, uniformtext_mode='hide',
                          margin=dict(l=40, r=70, b=70, t=70),
                          legend=dict(x=0, y=0.96, traceorder="normal",
                                      bgcolor='rgba(0,0,0,0)',
                                      font=dict(size=12)))
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown(
        """
        Nous vous proposons de partir ensemble pour un voyage dans les méandres de l’univers. 
        Où les températures ardentes flirtent avec le zéro absolu et où le vide est la règle et la vie l’exception.

        Partons ensemble à la rencontre des exoplanetes
        """)

    st.title(" ")
    col1, col2, col3 = st.beta_columns([1, 4, 1])
    with col2:
        st.image("https://github.com/MickaelKohler/Exoplanet_Discovery/raw/main/Ressources/galaxy-red-green-illustration-wallpaper.png",
                 caption="Ceci n'est pas une exoplanète")

    expander = st.beta_expander("Les technologies utilisées")
    expander.write('Plusieurs librairies de _Python_ ont été utilisées pour la réalisation de ce site : ')
    col1, col2, col3, col4 = expander.beta_columns(4)
    with col1:
        st.write('__Gestion des base de données__')
        st.image('https://raw.githubusercontent.com/MickaelKohler/Exoplanet_Discovery/main/Ressources/tool_pandas.png')
    with col2:
        st.write('__Création du modèle de ML__')
        st.image('https://raw.githubusercontent.com/MickaelKohler/Exoplanet_Discovery/main/Ressources/1200px-Scikit_learn_logo_small.svg.png')
    with col3:
        st.write('__Création des graphiques__')
        st.image('https://raw.githubusercontent.com/MickaelKohler/Exoplanet_Discovery/main/Ressources/logo_plotly.png')
    with col4:
        st.write('__Création de la WebApp__')
        st.image('https://raw.githubusercontent.com/MickaelKohler/Exoplanet_Discovery/main/Ressources/1*u9U3YjxT9c9A1FIaDMonHw.png')

    col1, col2 = expander.beta_columns([7, 1])
    with col2:
        st.title(" ")
        st.write('_une production_')
        st.image('https://raw.githubusercontent.com/MickaelKohler/Exoplanet_Discovery/main/Ressources/Logo%20pirate%20duck.png')


elif categorie == "Observer les Exoplanètes":
    st.title('Comment découvrir des Exoplanètes')
    st.subheader("La découverte d'un nouveau Monde")

    st.markdown(
        """
        Le 6 octobre 1995, les astronomes Michel Mayor et Didier Queloz, annoncent la découverte d'une première 
        exoplanète. Cette planète, nommée __51 Pegasi B__, se  situe à une cinquantaine 
        d'années lumière de la Terre dans la constelation du Pégase.
        """
    )

    fig = px.histogram(planets, x="disc_year", color="discoverymethod",
                       title="<b>Le nombre de planètes découvertes par années et par méthodes</b>",
                       nbins=10, color_discrete_sequence=px.colors.sequential.Agsunset_r,
                       labels="Méthode de découverte")
    fig.update_layout(xaxis_title="Années de découverte", yaxis_title="Nombre d'Exoplanet")
    st.plotly_chart(fig, use_container_width=True)

    if show:
        df_hist = pd.pivot_table(planets, index='disc_year', values='pl_name', columns='discoverymethod',
                                 aggfunc='count', margins=True).fillna(0)
        st.dataframe(df_hist)
    
    st.markdown("""
    ___Qu'est ce que la méthode des vitesses radiales___

    La force de gravité des planètes modifie le déplacement de leur étoile.
    Les capteurs situés sur Terre vont détecter des spectres passant d'une couleur bleu à une couleur rouge. 
    Le décalage de temps durant le changement de couleurs permet de déduire des paramètres 
    physiques comme la vitesse, la masse et la distance.
    
    ___Et la méthode la méthode du transit ?___

    Cette méthode consiste en l'observation d'une répétition constante d'une __variation de luminosité__ d'une étoile.
    Lorsqu'une planète passe devant une étoiles, elle crée une zone d'ombre 
    qui font varier la luminosité captée depuis la Terre.
    """)

    col1, col2, col3 = st.beta_columns([1, 3, 1])
    lk = 'https://raw.githubusercontent.com/MickaelKohler/Exoplanet_Discovery/main/Ressources/Astronomical_Transit.gif'
    with col2:
        st.markdown(f"![Alt Text]({lk})")

    fig = px.scatter(data_frame=planets, x="sy_disterr1", y="pl_orbper",
                     title="<b>Les méthodes utilisées en fonction de la période orbitale et de la distance à la Terre</b>",
                     color='discoverymethod',)
    fig.update_layout(xaxis_title="Distance à la Terre (al)", yaxis_title="Période orbitale autour de l'étoile")
    fig.update_xaxes(range=[-2, 200])
    fig.update_yaxes(range=[0, 200])
    st.plotly_chart(fig, use_container_width=True) 

    st.subheader("La contribution de Kepler dans la recherches d'exoplanètes")
    st.markdown(
        """
        Les méthodes de détection des exoplanètes peuvent être appliquées sur Terre mais aussi directement depuis 
        l'espace. Elles nécessitent l'utilisation d'équipement spécifiques capable d'enregistrer l'image des spectres 
        lumineux. Ces équipements peuvent aller du plus pointus aux simple télescope ou appareil photo.
        """)

    # Groupe les objectifs photos et groupes les telescopes
    planets2 = planets.copy()
    planets2["disc_telescope"] = planets2["disc_telescope"].apply(lambda x: "Objectif photo" if str(x) == 'Canon 400mm f/2.8L' else x)
    planets2["disc_telescope"] = planets2["disc_telescope"].apply(lambda x: "Objectif photo" if str(x) == 'Mamiya 645 80mm f/1.9' else x)
    planets2["disc_telescope"] = planets2["disc_telescope"].apply(lambda x: "Objectif photo" if str(x) == 'Canon 200mm f/1.8L' else x)
    planets2["disc_telescope"] = planets2["disc_telescope"].apply(lambda x: x if (str(x) == '0.95 m Kepler Telescope' or str(x) == 'Objectif photo') else "Telescope")

    fig = px.histogram(planets2, x="disc_telescope", color="discoverymethod",
                       title="<b>Nombre de planètes détectées par type de téléscope</b>"
                       ).update_xaxes(categoryorder="total descending")

    fig.update_layout(xaxis_title="Type de telescope",
                      yaxis_title="Nombre de planètes détéctées",
                      title_text='Max température par Date en fonction des opinions', title_x=0.5)

    col1, col2 = st.beta_columns([2, 1])
    with col1:
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.title('')
        st.markdown(
            """
            En 2009, l'engin spatial Kepler est envoyé en orbite avec l'objectif de 
            recenser les planètes similaire à la Terre.
            
            Il a été conçu pour utiliser la méthode des transits par l'intermédiaire d télescope de 0.98 mètre 
            de diamètre équipé d'un détecteur mesurant l'intensité lumineuse des étoiles.
            
            La mission de Kepler s'est terminée en 2019 après la découverte record de plus de 2600 exoplanètes. 
            """)


elif categorie == "Les Exoplanètes habitables":
    st.title('Les caractéristiques des Exoplanètes habitables')
    st.subheader('Où sont elles et quels sont leurs projets')
    
    phl_sample = plan_hab[['P_NAME', 'S_TYPE_TEMP', 'P_TYPE', 'S_AGE', 'P_DISTANCE', 'S_TEMPERATURE']]
    zone_hab = pd.merge(planets, phl_sample, left_on='pl_name', right_on='P_NAME', how='left')
    habit = zone_hab[zone_hab['P_HABITABLE'].isin([1, 2])]

    st.markdown(
        """
        On dénombre dans la base de données plus de *** exoplanètes et seulement *** qui sont considérées 
        comme pouvant potentiellement habriter la vie.
        """
    )

    # réparition des planètes
    constelation = planets[planets['P_HABITABLE'].isin([1, 2])][['pl_name', 'hostname', 'S_CONSTELLATION']]
    constelation.dropna(inplace=True)
    fig = px.sunburst(constelation, path=['S_CONSTELLATION', 'hostname', 'pl_name'], maxdepth=2,
                      color_discrete_sequence=px.colors.sequential.Peach_r)
    fig.update_layout(title="<b>Où sont localisées les planètes habitables ?</b>",
                      margin=dict(l=10, r=10, b=10, t=40))

    col1, col2 = st.beta_columns([3, 1])
    with col1:
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.title(" ")
        st.markdown(
            """
            Le tableau interactif ci-contre vous présente la position de l’ensemble des exoplanètes habitables.
            Vous avez :
            - _Sur le cercle intérieur_ : les constellations.
            - _Sur le cercle extérieur_ : les systèmes solaire.
            
            Vous pouvez cliquer sur le système pour afficher les noms des exoplanètes habitables qui le composent. 
            """)

    planet_name = habit[habit.index == habit['sy_dist'].idxmin()].iloc[0, 0]
    planet_distance = (habit['sy_dist'].min()*3.26156).round(2)
    st.markdown(
        f"""
        __Où se situe la planète la plus proche ?__ La planète potentiellement habitables 
        la plus proche est __{planet_name}__, qui est située à {planet_distance} années lumières.

        A savoir, qu'il faudait _76 624 993 ans_ de voyage à la sonde _Voyager 1_ pour atteindre cette exoplanète.
        
        Pour qu'une planète soit considéré comme habitable, elle doit être située dans la __Zone Habitable__ 
        qui est la région de l’espace où les conditions sont favorables à l’apparition de la vie, 
        telle que nous la connaissons sur Terre.

        Les limites des zones habitables sont calculées à partir des éléments connus de la biosphère de la Terre, 
        comme sa position dans le Système solaire et la quantité d'énergie qu'elle reçoit du Soleil.  
        
        Le graphique ci-dessous permet de bien percevoir cette _Zone Habitable_, 
        les exoplanètes devant s'éloigner à mesure que son étoile gagne en puissance.       
        """
    )

    # zone habitable
    clean_zone = zone_hab[(zone_hab['P_DISTANCE'] < 2) &
                          (zone_hab['S_TEMPERATURE'] > 2500) &
                          (zone_hab['S_TEMPERATURE'] < 8000)]
    clean_zone['P_HABITABLE'] = clean_zone['P_HABITABLE'].apply(lambda x: 'Non Habitable' if x == 0 else 'Habitable')
    inHab = clean_zone[clean_zone['P_HABITABLE'] == 'Non Habitable']
    hab = clean_zone[clean_zone['P_HABITABLE'] == 'Habitable']

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            text=inHab['pl_name'],
            mode='markers',
            x=inHab['P_DISTANCE'],
            y=inHab['S_TEMPERATURE'],
            marker=dict(color='coral', opacity=0.3),
            name='Non Habitable'
        )
    )
    fig.add_trace(
        go.Scatter(
            text=hab['pl_name'],
            mode='markers',
            x=hab['P_DISTANCE'],
            y=hab['S_TEMPERATURE'],
            marker=dict(color='forestgreen'),
            name='Habitable'
        )
    )
    fig.update_layout(
        title='<b>La situation des planètes habitables selon la chaleur du soleil et la distance</b>',
        yaxis=dict(title="Température du soleil (en kelvins)"),
        xaxis=dict(title="Distance planète/étoile (en année-lumière)"),
        margin=dict(l=10, r=10, b=10, t=70))
    st.plotly_chart(fig, use_container_width=True)

    expander = st.beta_expander("Illustration de la zone habitable dans notre système solaire")
    expander.image('https://raw.githubusercontent.com/MickaelKohler/Exoplanet_Discovery/main/Ressources/zone_habitable_systeme_solaire_espace_stellaire_1024x1024.jpg')

    st.markdown("---")
    
    # Comparatif Habitable/inhabitable
    st.subheader("Qu'est ce qui caractérise une planète habitable ?")
    st.markdown(
        """
        La _Zone Habitable_ met en avant la nécessité de déterminer les critères 
        qui font qu’une exoplanète soit suspectée comme pouvant être habitable. 

        On peut donc tenter de comparer les caractéristiques des exoplanètes 
        considérées comme habitables de l’ensemble des exoplanètes.

        Restons dans les étoiles et essayons de répondre à la question : 
        _Quelle type d’étoile favorise la présence d’exoplanètes habitables ?_
        """
    )

    # Sun Type
    sType = pd.DataFrame(zone_hab['S_TYPE_TEMP'].value_counts(normalize=True)*100).rename(columns={'S_TYPE_TEMP': 'Exoplanètes'})
    sType_hab = habit['S_TYPE_TEMP'].value_counts(normalize=True)*100
    sType_tab = pd.concat([sType, sType_hab], axis=1).reindex(index=['O', 'B', 'A', 'F', 'G', 'K', 'M'])
    sType_tab = sType_tab.fillna(0).rename(columns={'S_TYPE_TEMP': 'Habitables'}).round(2)

    fig = px.bar(sType_tab, x=sType_tab.index, y=["Exoplanètes", "Habitables"], barmode='group',
                 title="<b>La répartition des exoplanètes selon le type de leur étoile</b> (en pourcents)",
                 color_discrete_map={'Exoplanètes': 'deepskyblue', 'Habitables': 'coral'})
    fig.update_traces(texttemplate='%{text}%', textposition='outside')
    fig.update_layout(showlegend=True, font_family='IBM Plex Sans',
                      xaxis=dict(title="Catégorie d'étoile"),
                      yaxis=dict(title=None),
                      uniformtext_minsize=10,
                      uniformtext_mode='hide',
                      margin=dict(l=10, r=10, b=10),
                      legend=dict(x=0, y=1, traceorder="normal", bgcolor='rgba(0,0,0,0)', font=dict(size=12)))
    texts = [sType_tab["Exoplanètes"], sType_tab["Habitables"]]
    for i, t in enumerate(texts):
        fig.data[i].text = t

    if show:
        col1, col2 = st.beta_columns([1, 3])
        with col2:
            st.plotly_chart(fig, use_container_width=True)
        with col1:
            st.title(' ')
            st.dataframe(sType_tab)
    else:
        st.plotly_chart(fig, use_container_width=True)
   
    col1, col2 = st.beta_columns([1, 2])
    with col1:
        st.markdown(
            """
            On peut constater que ce sont surtout les étoiles de type K et M qui comprennent 
            le plus d’exoplanètes habitables. Ce qui s’explique sans doute par 
            le faite que ce sont les plus petites et donc les moins chaudes. 

            Le tableau ci-contre explique la différence entre chaque type.
            """)

    with col2:
        sol_typ = pd.DataFrame(data=[['> 25 000 K', 'bleue', 'azote, carbone, hélium et oxygène'],
                                     ['10 000–25 000 K', 'bleue-blanche', 'hélium, hydrogène'],
                                     ['7 500–10 000 K', 'blanche', 'hydrogène'],
                                     ['6 000–7 500 K', 'jaune-blanche',
                                      'métaux : fer, titane, calcium, strontium et magnésium'],
                                     ['5 000–6 000 K', 'jaune (comme le Soleil)',
                                      'calcium, hélium, hydrogène et métaux'],
                                     ['3 500–5 000 K', 'orange', 'métaux et monoxyde de titane'],
                                     ['< 3 500 K', 'rouge', 'métaux et monoxyde de titane']],
                               index=['O', 'B', 'A', 'F', 'G', 'K', 'M'],
                               columns=['température', 'couleur conventionnelle', "raies d'absorption"])
        st.write(sol_typ)
    
    # Sun Age
    sAge = planets.groupby((zone_hab['S_AGE'] // 2) * 2).count()[['pl_name']]
    sAge.iloc[5, 0] = sAge.iloc[5:, 0].sum()
    sAge['norm'] = ((sAge['pl_name']*100) / sAge['pl_name'].sum()).round(2)
    sAge = sAge.drop(columns=['pl_name']).drop([12, 14]).rename(columns={'norm': 'Exoplanètes'})

    sAge_hab = habit.groupby((habit['S_AGE'] // 2) * 2).count()[['pl_name']]
    sAge_hab['norm'] = ((sAge_hab['pl_name']*100) / sAge_hab['pl_name'].sum()).round(2)
    sAge_hab = sAge_hab.drop(columns=['pl_name']).rename(columns={'norm': 'Habitables'})

    sAge_tab = pd.concat([sAge, sAge_hab], axis=1).fillna(0).round(2)
    sAge_tab.rename(index={0: '<2', 2: '2-4', 4: '4-6', 6: '6-8', 8: '8-10', 10: '+10'}, inplace=True)

    fig = px.bar(sAge_tab, x=sAge_tab.index, y=["Exoplanètes", "Habitables"],
                 title="<b>La répartition des exoplanètes selon l'age de leur étoile</b> (en pourcents)",
                 barmode='group',
                 color_discrete_map={'Exoplanètes': 'deepskyblue', 'Habitables': 'coral'})
    fig.update_traces(texttemplate='%{text}%', textposition='outside')
    fig.update_layout(showlegend=True, font_family='IBM Plex Sans',
                      xaxis=dict(title="Age de l'étoile (Gy)"),
                      yaxis=dict(title=None),
                      uniformtext_minsize=10, uniformtext_mode='hide',
                      margin=dict(l=10, r=10, b=10),
                      legend=dict(x=0, y=1, traceorder="normal",
                                  bgcolor='rgba(0,0,0,0)',
                                  font=dict(size=12)))
    texts = [sAge_tab["Exoplanètes"], sAge_tab["Habitables"]]
    for i, t in enumerate(texts):
        fig.data[i].text = t

    if show:
        col1, col2 = st.beta_columns([3, 1])
        with col1:
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            st.title(' ')
            st.dataframe(sAge_tab, height=360)
    else:
        st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        """
        Toujours dans les étoiles, on remarque que les exoplanètes observées sont essentiellement situées 
        sur les __étoiles les plus jeunes__, même si aucune tranche d’âge ne sort du lot. 

        Pour que la vie puisse apparaître sur une planète, il ne suffit pas qu'elle soit dans l'écosphère de son 
        étoile ; son système planétaire doit se situer __assez près du centre de la galaxie__ pour avoir suffisamment 
        d'éléments lourds qui favorisent la formation de planètes telluriques et des 
        atomes nécessaires à la vie (fer, cuivre, etc).

        Mais ce système devra également se situer __assez loin du centre galactique__ pour éviter des dangers tels que 
        le trou noir au centre de la galaxie et les supernova.

        Mais l'exoplanète en elle même doit présenter des conditions intrinsèque pour 
        être une bonne candidate pour accueillir la vie. 
        """
    )

    # Exoplanet type
    pType = pd.DataFrame(zone_hab['P_TYPE'].value_counts(normalize=True)*100).rename(columns={'P_TYPE': 'Exoplanètes'})
    pType_hab = habit['P_TYPE'].value_counts(normalize=True)*100
    pType_tab = pd.concat([pType, pType_hab], axis=1).reindex(index=['Miniterran', 'Subterran', 'Terran',
                                                                     'Superterran', 'Neptunian', 'Jovian'])
    pType_tab = pType_tab.fillna(0).round(2).rename(columns={'P_TYPE': 'Habitables'})

    fig = px.bar(pType_tab,
                 x=pType_tab.index,
                 y=["Exoplanètes", "Habitables"],
                 title="<b>La répartition des exoplanètes selon leur type</b> (en pourcents)",
                 barmode='group',
                 color_discrete_map={'Exoplanètes': 'deepskyblue', 'Habitables': 'coral'})
    fig.update_traces(texttemplate='%{text}%', textposition='outside')
    fig.update_layout(showlegend=True, font_family='IBM Plex Sans',
                      xaxis=dict(title="Type d'exoplanète"),
                      yaxis=dict(title=None),
                      uniformtext_minsize=10, uniformtext_mode='hide',
                      margin=dict(l=10, r=10, b=10),
                      legend=dict(x=0,
                                  y=1,
                                  traceorder="normal",
                                  bgcolor='rgba(0,0,0,0)',
                                  font=dict(size=12)))
    texts = [pType_tab["Exoplanètes"], pType_tab["Habitables"]]
    for i, t in enumerate(texts):
        fig.data[i].text = t

    col1, col2 = st.beta_columns([3, 1])
    with col1:
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        if show:
            st.title(" ")
            st.dataframe(pType_tab)
        else:
            st.title(" ")
            st.markdown(
                """
                Les type d'exoplanet selon
                la masse de la terre (MT): 
                - _Miniterran_ : -0,1 MT
                - _Subterran_ : 0,1 à 0,5 MT
                - _Terran_ : 0,5 à 2 MT
                - _Superterran_ : 2 à 10 MT
                - _Neptunian_ : 10 à 50 MT
                - _Jovian_ : +50 MT 
                """
            )
    
    st.markdown(
        """
        Les exoplanète habitables sont essentiellement situées sur des planètes équivalentes 
        à la terre ou légèrement plus grosse. Comme pour la _Zone Habitable_, la conditions de 
        validité pour être considérée comme une exoplanète habitable est très restreinte. 

        Ces conditions ne sont bien sur pas limitatives. Il existe de nombreux critères à prendre en compte. 
        De nombreuses variables qui peuvent être étudiées par un algorithme afin de 
        pouvoir créer un modèle permettant de repérer les exoplanètes.
        """
    )


elif categorie == "L'IA à l'aide des Astrophysicien":
    st.title("L'intelligence artificielle à la recherche de la vie")
    st.subheader("Comment le Machine Learning peut venir à l'aide des Astrophysicien")
    st.title(" ")

    st.markdown(
        """
        Lors de notre recherche de la base de donnée parfaite (BDP), nous avons trouvé une base de donnée 
        hébergée par _Planetary Hability Laboratory_ qui tente de répertorier et identifier les exoplanètes habitables.

        Toutefois, leur base de donnée ne prend pas en considération les dernières 
        exoplanètes découvertes à partir de début 2020. 

        Nous avons donc tenté d’entrainer un __algorithme de Machine Learning__ pour déterminer, 
        selon les caractéristiques de chaque exoplanète, si elle peut être catégorisée comme habitable ou non, 
        dans le but de catégoriser celles qui n’ont pas été identifiée.
        """
    )

    df_exoplanet_vf = planets.copy()

    # Selecting all numerical column from dataframe
    numeical_columns_list = df_exoplanet_vf.select_dtypes(include=np.number).columns.tolist()
    df_exoplanet_num = df_exoplanet_vf[numeical_columns_list]

    # Selecting main categorical columns
    df_exoplanet_cat = df_exoplanet_vf[['pl_letter', 'discoverymethod', 'disc_locale']]

    # setting them into numerical value using factorization
    df_exoplanet_cat['pl_letter'] = df_exoplanet_cat['pl_letter'].factorize()[0]
    df_exoplanet_cat['discoverymethod'] = df_exoplanet_cat['discoverymethod'].factorize()[0]
    df_exoplanet_cat['disc_locale'] = df_exoplanet_cat['disc_locale'].factorize()[0]

    # merging dataset of selected columns 
    df_exoplanet_rf = df_exoplanet_num.join(df_exoplanet_cat)

    # ...and splitting dataset on 'P_HABITABLE' none or not
    df_exoplanet_rf_1 = df_exoplanet_rf[df_exoplanet_rf['P_HABITABLE'].notna()]
    df_exoplanet_rf_2 = df_exoplanet_rf[df_exoplanet_rf['P_HABITABLE'].isna()]

    # filling missing values with the mean of each column
    df_exoplanet_rf_1.fillna(df_exoplanet_rf_1.mean(), inplace=True)

    # starting ML with XGboost
    y = df_exoplanet_rf_1["P_HABITABLE"]
    X = df_exoplanet_rf_1.drop("P_HABITABLE", axis=1)

    # training data
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=50)

    # fitting model on training data
    model = XGBClassifier().fit(X, y)

    # making prediction on unknown dataset
    df_exoplanet_rf_2["predictions"] = model.predict(df_exoplanet_rf_2.drop(columns='P_HABITABLE'))

    df_test = df_exoplanet_vf[['pl_name', 'discoverymethod']]
    df_final = pd.merge(df_test, df_exoplanet_rf_2, left_index=True, right_index=True)
    df_final = df_final[['pl_name', 'disc_year', 'discoverymethod_x', 'predictions']]
    df_final.loc[df_final['predictions'] == 0, 'predictions'] = 'Inhabitable'

    df_final.rename(columns={'pl_name': "Nom de l'Exoplanète",
                             'discoverymethod_x': 'Méthode utilisée',
                             'disc_year': 'Découverte',
                             'predictions': 'Prédiction'}, inplace=True)
    
    st.title(' ')
    ML_off = True
    col1, col2 = st.beta_columns([1, 3])
    with col1:
        st.markdown(
            """
            __Cliquez sur le bouton ci-dessous__ pour rechercher de nouvelles planètes 
            ayant le potentielle d'être habitable. 
            """
        )
        if st.button('Rechercher la vie'):
            ML_off = False
            st.markdown(
                """
                Comme vous pouvez le voir, __aucune nouvelle exoplanète ne 
                remplit les conditions__ pour pouvoir accueillir la vie. 

                La recherche continue…

                _« I want to believe »_
                """
            )
    with col2:
        if ML_off:
            display_tab = df_final.copy()
            display_tab['Prédiction'] = ' '
            st.dataframe(display_tab, height=550)
        else:
            st.dataframe(df_final, height=550)

    expander = st.beta_expander("Explication du modèle retenu")
    expander.markdown(
        """
        ___Quel modèle a été retenu ?___

        Nous avons testé les algorithmes de classification les plus 
        pertinents afin de prédire si une planète est habitable.

        Lors de ces tests, les algorithmes, ci-dessous, ont produit les résultats les plus proches 
        de la réalités (scores), c'est à dire en comparant nos résultats aux informations à notre disposition.

        Bien que les meilleurs scores soient supérieurs à celui du XGBoost, que nous avons choisit, 
        ce dernier a été plus à même de prédire les planètes habitables connues.
        """)
        
    # New dataframe with score of different test
    dataScore = {'Test': ['SGDClassifier', "DecisionTreeClassifier", "KNeighborsClassifier", "BaggingClassifier",
                          "RandomForestClassifier", "AdaBoostClassifier", "XGBoost"],
                 "Score": [0.990069513406156, 0.984111221449851, 0.991062562065541, 0.990069513406156,
                           0.991062562065541, 0.985104270109235, 0.9890764647467726]}
    pd.DataFrame.from_dict(dataScore)

    fig = px.histogram(data_frame=dataScore,
                       x="Test",
                       y="Score",
                       title="Score des différents test").update_xaxes(categoryorder="total descending")

    fig.update_yaxes(range=[0.97, 1])
    fig.update_layout(xaxis_title="Score", yaxis_title="Test")

    expander.plotly_chart(fig, use_container_width=True) 

    expander.markdown(
        """
        ___Qu'est-ce que le XGBoost ?___

        XGBoot est la Extrême Gradient Boosted Trees, plus simplement 
        il s'agit d'une forêt d'arbres de décision optimisée.

        "Un arbre de décision est un outil d'aide à la décision représentant 
        un ensemble de choix sous la forme graphique d'un arbre. 
        Les différentes décisions possibles sont situées aux extrémités des branches (les « feuilles » de l'arbre), 
        et sont atteintes en fonction de décisions prises à chaque étape" 
        [source](https://fr.wikipedia.org/wiki/Arbre_de_d%C3%A9cision)
        """
    )
