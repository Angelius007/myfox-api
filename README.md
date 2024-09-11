## MyFox
# Author : Angelius007

API : https://api.myfox.me/

Préconisations :

Après installation :
- Pour pouvoir mettre des couleurs sur les icônes
    - installer Custom-ui : https://github.com/Mariusthvdb/custom-ui
    - ajouter dans le configuration.yaml la ligne : 
        homeassistant: !include custom_components/myfox/customize.yaml



Pour les Tests :

- Commencer par remplir le fichier "init_cache.txt"
    - "CLIENT_ID": "xxx" -> A r ecuperer sur api.myfox.me
    - "CLIENT_SECRET": "xxx" -> A recuperer sur api.myfox.me
    - "MYFOX_USER": "xxx" -> Email compte MyFox
    - "MYFOX_PSWD": "xxx"  -> Pswd MyFox
