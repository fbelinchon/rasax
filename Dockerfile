ARG RASA_VERSION
FROM rasa/rasa:${RASA_VERSION}-full

USER 0

RUN pip install --upgrade pip
RUN python -m spacy download es_core_news_sm
RUN python -m spacy link es_core_news_sm es

USER 1001