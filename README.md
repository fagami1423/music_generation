# Music Generation using Tensorflow
his project aims to generate and continue music using various machine-learning models. Specifically, we utilize the Long Short-Term Memory (LSTM) model and the Variational Autoencoder (VAE) for music generation. Our LSTM architecture includes 1024 Recurrent Neural Network (RNN) units and is initialized with the Glorot uniform distribution. The input music tokens are first passed through a learnable embedding layer to create 256-dimensional vectors, which are then recursively fed into the LSTM layer.

Here are the useful documents to read before starting the project
magenta docs - https://github.com/PacktPublishing/hands-on-music-generation-with-magenta

jam machine - https://github.com/m41w4r3exe/the-jam-machine
https://hub.docker.com/r/misnaej/the_jam_machine

https://colinraffel.com/projects/lmd/

### The project folder structure 
```
-- models
|   |-- melody
        |-- primers
        |-- bundles
        |-- helper.utils.py
        |-- rnn_model.py
|   |-- Music_Vae
        |-- helper_utils.py
        |-- music_vae_model.py
|-- music/
|-- output/
    |--drums
    |--sample
    |--merge
    |--mixer
|-- Training/
|-- .gitignore
|-- .gitignore
|-- docker-compose.yml
|-- main.py
|-- README.md
|-- requirements.txt
```
Create virtual environment and activate 

Install the packages
```
pip install -r requirements.txt
```
### To tun the project 
```
uvicorn main:app --reload
```

The default url for the application will be 
```
http://localhost:8000/docs
```
Using Docker
```
docker compose up -d        
```
