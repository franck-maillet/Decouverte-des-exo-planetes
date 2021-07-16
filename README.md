# Exoplanet Discovery
Le but de cet outil est de prédire en fonction des caractéristiques receuillies sur de nouvelles planètes, la possibilité ou non d'y trouvé de la vie

## Composition du Git

* [Origine du projet](#origine-du-projet)
* [Technologies](#technologies)
* [Bases de Données](#bases-de-données)
* [Statut](#statut)
* [La Team](#la-team)

## Origine du projet

Lors d’un **Sprint** de 30 heures, organisé par la __Wild Code School__ nous avons été amené à présenter une projet sur le thème de l'espace.
Nous avons décidé de se concentrer sur les *caractéristiques des exoplanètes* habitables afin d’entrainer un algorithme de *Machine Learning* pour déterminer si une nouvelle exoplanète est habitable.

La **WebApp** crée se divise en 3 sections : 
- Une présentation des techniques d’identification  des exoplanètes
- Une études des caractéristiques permettant de déterminer si une exoplanète est habitable
- Un algoritme de ML (XGboost) qui détermine si les nouvelles exoplanètes découvertes sont habitables ou non.

### Adresse du site :

Le site est hébergé directement sur les serveurs mis à disposition par *Streamlit* :

https://share.streamlit.io/mickaelkohler/exoplanet_discovery/main/Exoplanet_discovery.py


## Technologies 

Projet fait entièrement en **Python**

Utilisations des librairies suivantes : 
 - Pandas
 - Scikit-learn
 - Plotly
 - Streamlit


## Bases de données 

La [base de données de **NASA Exoplanet Archive**](https://exoplanetarchive.ipac.caltech.edu/cgi-bin/TblView/nph-tblView?app=ExoTbls&config=PS) ont été utilisées pour obtenir l’ensemble des datas sur les exoplanètes.

La [base de données de **Planetary Habitability Laboratory**](http://phl.upr.edu/projects/habitable-exoplanets-catalog/data/database) a permis d’obtenir le nom des exoplanètes habitables. 

## Statut

Le hackathon a eu lieu du *11/04 au 12/04/2021*.

## La Team

Le projet a été réalisé par les élèves de la **Wild Code School** : 
- Antoine Carre
- Franck Maillet
- Michael Kohler
- Mickaël Caceres
