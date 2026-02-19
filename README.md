# Formatif F3 — Capteurs I2C AHT20 + VCNL4200

**Cours** : 243-413-SH — Introduction aux objets connectes
**Semaine** : 3
**Type** : Formative (non notee)
**Retries** : Illimites - poussez autant de fois que necessaire!

---

> **Pratique autonome** -- Ce formatif est une evaluation formative (non notee). Contrairement au laboratoire guide, vous devez completer les taches de maniere autonome. Les tests automatiques vous donnent une retroaction immediate a chaque push.

## Ce que vous avez appris en labo

Le laboratoire de la semaine 3 vous a guide a travers :

- Detection de plusieurs peripheriques I2C avec `i2cdetect` (AHT20 et VCNL4200)
- Lecture du capteur AHT20 avec le pattern de retry
- Combinaison de deux capteurs heterogenes (AHT20 + VCNL4200) sur le meme bus I2C
- Comprehension de la difference entre I2C et one-wire

Ce formatif vous demande d'appliquer ces competences de maniere autonome.

---

## Progressive Milestones

Ce formatif utilise des **jalons progressifs** avec retroaction detaillee:

| Jalon | Points | Verification |
|-------|--------|-------------|
| **Milestone 1** | 25 pts | Script existe, syntaxe valide, tests locaux executes |
| **Milestone 2** | 35 pts | I2C initialise, capteur AHT20 cree, lecture temperature/humidite |
| **Milestone 3** | 40 pts | Logique de retry, gestion d'erreurs, qualite du code |
| **Milestone 4** | 25 pts | Integration multi-capteurs VCNL4200 (proximite + lumiere) |

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
5. Integrer un deuxieme capteur VCNL4200 (proximite et lumiere) sur le meme bus I2C

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

Vous devriez voir `38` pour le capteur AHT20 et `51` pour le VCNL4200 (si connecte).

### Etape 3 : Creer aht20_sensor.py

```python
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

## Capteurs I2C utilises

| Caracteristique | AHT20 | VCNL4200 |
|-----------------|-------|----------|
| Adresse I2C | 0x38 | 0x51 |
| Temperature | Oui | Non |
| Humidite | Oui | Non |
| Proximite | Non | Oui |
| Lumiere ambiante (lux) | Non | Oui |
| Connecteur | STEMMA QT | STEMMA QT |
| Produit Adafruit | 4566 | 6064 |

Les deux capteurs se connectent en daisy-chain via cable STEMMA QT sur le meme bus I2C!

### Materiel requis

- Raspberry Pi avec I2C active
- AHT20 (Adafruit 4566) — temperature + humidite
- VCNL4200 (Adafruit 6064) — proximite + lumiere ambiante
- Cable STEMMA QT pour connexion daisy-chain

---

## Milestone 4 : Integration multi-capteurs (VCNL4200)

Apres avoir complete les Milestones 1-3 avec l'AHT20, creez un script
`multi_capteurs.py` qui combine les deux capteurs :

```python
# /// script
# requires-python = ">=3.9"
# dependencies = ["adafruit-circuitpython-ahtx0", "adafruit-circuitpython-vcnl4200", "adafruit-blinka"]
# ///
"""Lecture multi-capteurs AHT20 + VCNL4200 via I2C."""

import board
import adafruit_ahtx0
import adafruit_vcnl4200

i2c = board.I2C()
aht = adafruit_ahtx0.AHTx0(i2c)
vcnl = adafruit_vcnl4200.Adafruit_VCNL4200(i2c)

print(f"Temperature: {aht.temperature:.1f} C")
print(f"Humidite: {aht.relative_humidity:.1f} %RH")
print(f"Proximite: {vcnl.proximity}")
print(f"Lumiere: {vcnl.lux:.1f} lux")
```

Ce script doit :
- Importer `adafruit_ahtx0` et `adafruit_vcnl4200`
- Creer les deux objets capteurs sur le meme bus I2C
- Lire `.proximity` et `.lux` du VCNL4200
- Afficher les donnees environnementales et spatiales combinees

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

- [ ] `aht20_sensor.py` — Script de lecture du capteur AHT20 (Milestones 1-3)
- [ ] `multi_capteurs.py` — Script multi-capteurs AHT20 + VCNL4200 (Milestone 4)
- [ ] `.test_markers/` — Dossier cree par `validate_pi.py`

---

Bonne chance!
