## MyFox
# Author : Angelius007

API : https://api.myfox.me/

Implémentation Custom pour interfaçage avec les API MyFox (racheté par Somfy)

Préconisations :
- Installer le plugin "custom-ui" via HACS pour changer la couleur des icônes

Après installation :
- Pour pouvoir mettre des couleurs sur les icônes
    - installer Custom-ui : https://github.com/Mariusthvdb/custom-ui
    - ajouter dans le configuration.yaml la ligne : 
        homeassistant: !include custom_components/myfox/customize.yaml



Pour les Tests :

- Commencer par remplir le fichier "init_cache.txt"
    - "CLIENT_ID": "xxx" -> A recuperer sur api.myfox.me
    - "CLIENT_SECRET": "xxx" -> A recuperer sur api.myfox.me
    - "MYFOX_USER": "xxx" -> Email compte MyFox
    - "MYFOX_PSWD": "xxx"  -> Pswd MyFox
