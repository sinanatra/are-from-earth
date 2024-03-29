# Men are from Earth, Women are from Earth, and Ai are from Earth too.

[![Watch the video](https://github.com/sinanatra/are-from-earth/assets/20107875/1dd6350f-bb0f-4e29-800a-a9cdb75b2480)](https://vimeo.com/412366901)
[Watch the video](https://vimeo.com/412366901)


The disproportionate often irresponsive use of Machine learning Algorithms risks to emphasise stereotypes already present in data. Whenever data reflects biases of the broader society, the learning algorithm captures and learns from these stereotypes.

On this website we visualise how text embeddings trained on Google News represent gender.

------

Requirements
----------

Install PIP requirements with `pip install -r requirements.txt`.

Remember to insert a `.txt` or `.bin` embedding file in `gender.py`, you can create one here: `https://github.com/sinanatra/create-text-embedding`

or fetch it from here: `https://nlp.stanford.edu/projects/glove/` 

And to download spacy modules from here: `https://spacy.io/usage/models`

-----

Start
-----

Run `FLASK_APP=server.py flask run` to start.

Run `FLASK_APP=server.py FLASK_DEBUG=1 flask run` to start in debugging mode.
