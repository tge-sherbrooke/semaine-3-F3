# Formatif F3 — Capteur I2C AHT20

**Cours** : 243-413-SH — Introduction aux objets connectes
**Semaine** : 3
**Type** : Formative (non notee)
**Retries** : Illimites - poussez autant de fois que necessaire!

---

## Progressive Milestones

Ce formatif utilise des **jalons progressifs** avec retroaction detaillee:

| Jalon | Points | Verification |
|-------|--------|-------------|
| **Milestone 1** | 25 pts | Script existe, syntaxe valide, tests locaux executes |
| **Milestone 2** | 35 pts | I2C initialise, capteur AHT20 cree, lecture temperature/humidite |
| **Milestone 3** | 40 pts | Logique de retry, gestion d'erreurs, qualite du code |

**Chaque test echoue vous dit**:
- Ce qui etait attendu
- Ce qui a ete trouve
- Une suggestion pour corriger

---

## Objectif

Ce formatif vise a verifier que vous etes capable de :
1. Configurer et initialiser la communication I2C
2. Lire un capteur AHT20 (temperature et humidite)
3. Implementer une logique de retry (comme pour le DHT22)
4. Gerer les erreurs de communication

---

## Workflow de soumission

```
+-------------------------------------------------------------+
|                    WORKFLOW FORMATIF F3                     |
+-------------------------------------------------------------+
|                                                             |
|  1. Sur le Raspberry Pi                                     |
|     +-- Installer les dependances (uv pip install ...)      |
|     +-- Connecter le capteur AHT20 via STEMMA QT            |
|     +-- Verifier l'adresse I2C (sudo i2cdetect -y 1)        |
|                                                             |
|  2. Creer aht20_sensor.py                                   |
|     +-- Importer board et adafruit_ahtx0                    |
|     +-- Initialiser I2C et le capteur                       |
|     +-- Implementer la logique de retry                     |
|     +-- Lire temperature et humidite                        |
|                                                             |
|  3. Executer les tests locaux                               |
|     +-- python3 validate_pi.py                              |
|     +-- Corriger les erreurs si necessaire                  |
|                                                             |
|  4. Pousser vers GitHub                                     |
|     +-- git add .                                           |
|     +-- git commit -m "feat: lecture AHT20 avec retry"      |
|     +-- git push                                            |
|                                                             |
|  5. GitHub Actions valide automatiquement                   |
|                                                             |
+-------------------------------------------------------------+
```

---

## Instructions detaillees

### Etape 1 : Installer les dependances

```bash
# Installer la librairie AHT20
uv pip install adafruit-circuitpython-ahtx0
```

### Etape 2 : Verifier la connexion I2C

```bash
# Scanner le bus I2C
sudo i2cdetect -y 1
```

Vous devriez voir `38` pour le capteur AHT20.

### Etape 3 : Creer aht20_sensor.py

```python
#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = ["adafruit-circuitpython-ahtx0", "adafruit-blinka"]
# ///
"""Lecture du capteur AHT20 via I2C avec logique de retry."""

import board
import adafruit_ahtx0
import time

MAX_RETRIES = 3

def read_aht20():
    """Lit le capteur AHT20 avec retry en cas d'erreur."""
    i2c = board.I2C()
    sensor = adafruit_ahtx0.AHTx0(i2c)

    for attempt in range(MAX_RETRIES):
        try:
            temperature = round(sensor.temperature, 1)
            humidity = round(sensor.relative_humidity, 1)
            return temperature, humidity
        except Exception as e:
            print(f"Tentative {attempt + 1}/{MAX_RETRIES}: {e}")
            time.sleep(1)

    raise RuntimeError(f"Echec apres {MAX_RETRIES} tentatives")

def main():
    temp, humidity = read_aht20()
    print(f"Temperature: {temp} C")
    print(f"Humidite: {humidity} %RH")

if __name__ == "__main__":
    main()
```

### Etape 4 : Executer les tests locaux

```bash
python3 validate_pi.py
```

### Etape 5 : Pousser votre travail

```bash
git add .
git commit -m "feat: lecture AHT20 avec retry"
git push
```

---

## Cablage STEMMA QT

| Fil | Raspberry Pi |
|-----|--------------|
| Rouge (VIN) | 3.3V |
| Noir (GND) | GND |
| Bleu (SDA) | GPIO 2 |
| Jaune (SCL) | GPIO 3 |

**IMPORTANT** : VIN doit etre connecte a 3.3V, PAS 5V!

---

## Comparaison AHT20 vs BMP280

| Caracteristique | AHT20 | BMP280 |
|-----------------|-------|--------|
| Adresse I2C | 0x38 | 0x76 ou 0x77 |
| Temperature | Oui | Oui |
| Humidite | Oui | Non |
| Pression | Non | Oui |
| Altitude | Non | Oui (calculee) |

Les deux capteurs peuvent etre utilises ensemble sur le meme bus I2C!

---

## Pourquoi la logique de retry?

Meme si I2C est plus fiable que le protocole one-wire du DHT22,
des erreurs peuvent survenir:
- Connexion lache
- Conflit sur le bus I2C avec plusieurs capteurs
- Problemes de timing lors de l'initialisation

Le pattern de retry est une bonne pratique professionnelle
qui rend votre code plus robuste.

---

## Livrables

Dans ce depot, vous devez avoir :

- [ ] `aht20_sensor.py` — Script de lecture du capteur AHT20
- [ ] `.test_markers/` — Dossier cree par `validate_pi.py`

---

Bonne chance!
