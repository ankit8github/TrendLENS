import matplotlib.pyplot as plt

def plot_sentiment_bar(sentiment, score):
    labels = ['Positive', 'Negative', 'Neutral']
    values = [score if sentiment.upper() == l.upper() else 0 for l in labels]
    colors = ['green', 'red', 'gray']

    fig, ax = plt.subplots()
    ax.bar(labels, values, color=colors)
    ax.set_ylim(0, 1)
    return fig
