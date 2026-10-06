# 🎼 Music Generation with Deep Learning

The machine-learning backend of an **AI music generation platform** (a team capstone project). It generates melodies, polyphonic pieces and drum tracks with RNN, LSTM and VAE models, and serves them to the [music_frontend](https://github.com/fagami1423/music_frontend) web app.

![Python](https://img.shields.io/badge/Python-3.8-3776AB?logo=python&logoColor=white)
![TensorFlow](https://img.shields.io/badge/TensorFlow-FF6F00?logo=tensorflow&logoColor=white)
![Magenta](https://img.shields.io/badge/Google-Magenta-ff4081)

## ✨ What's inside
| Module | Description |
|---|---|
| `melody/` | Monophonic and polyphonic generation with Magenta models: Basic, Lookback and Attention RNN, Polyphony RNN and Performance RNN (with dynamics) |
| `drums/` | Drum pattern generation with Drums RNN |
| `Music_VAE/` | MusicVAE experiments for interpolating between melodies and creating variations |
| `test.py` | A character-level **LSTM** trained on folk songs in ABC notation (TensorFlow), which generates new tunes |
| `Transformer_Genre_Evaluation.ipynb` | Evaluates generated music by genre with a Transformer-based approach |

## 🧠 Approach
- **Primer-based continuation:** start from a user's MIDI primer and generate a continuation with a chosen model, temperature and length
- **LSTM:** 1,024 units, Glorot-uniform initialization and a 256-dimensional token embedding
- **Visualization:** generated MIDI is plotted with `visual_midi`; `muspy` is used for music processing and evaluation

## 🚀 Getting started
```bash
git clone https://github.com/fagami1423/music_generation.git
cd music_generation
pip install -r requirements.txt
python test.py
```
> The full REST API integration is on the [`API-Integratioin`](https://github.com/fagami1423/music_generation/tree/API-Integratioin) branch.

## 🛠️ Tech stack
Python · TensorFlow · Magenta · note-seq · MusPy · visual_midi · Jupyter

## 📚 References
- [Hands-On Music Generation with Magenta](https://github.com/PacktPublishing/hands-on-music-generation-with-magenta)
- [The Jam Machine](https://github.com/m41w4r3exe/the-jam-machine)
- [Lakh MIDI Dataset](https://colinraffel.com/projects/lmd/)

## 👤 Author
**Raj Kumar Phagami**: [GitHub](https://github.com/fagami1423)
