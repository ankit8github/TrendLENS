import matplotlib.pyplot as plt
from wordcloud import WordCloud

def plot_top_items_bar(counter_data, title, color='skyblue'):
    top_items = counter_data.most_common(10)
    labels, values = zip(*top_items)

    fig, ax = plt.subplots()
    ax.barh(labels[::-1], values[::-1], color=color)
    ax.set_title(title)
    ax.set_xlabel("Frequency")
    plt.tight_layout()
    return fig

def generate_wordcloud(text_list):
    all_text = ' '.join(text_list)
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_text)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis("off")
    plt.tight_layout()
    return fig
