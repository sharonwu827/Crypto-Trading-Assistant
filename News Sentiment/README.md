# News Sentiment

## Data
- Training & testing dataset via Kaggle (all-data.csv)
- API via [cryptonews-api](https://cryptonews-api.com/)

## Models Attempted
- [finbert-tone](https://huggingface.co/yiyanghkust/finbert-tone)
- [finbert](https://huggingface.co/ProsusAI/finbert)
- LSTM on training Dataset (poor generalization)
- Vader sentiment analysis
- [distilRoberta](https://huggingface.co/mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis)
- [BERT Uncased Sentiment](https://huggingface.co/nlptown/bert-base-multilingual-uncased-sentiment)
- Hybrid Approach (similar to the social media sentiment analysis approach)

## Models Used
- [finbert-tone](https://huggingface.co/yiyanghkust/finbert-tone) on title (best performing)
- [finbert-tone](https://huggingface.co/yiyanghkust/finbert-tone) on full article text
- Vader
