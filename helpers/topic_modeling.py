# helpers/topic_modeling.py

from bertopic import BERTopic

def extract_topics(texts, top_n=5):
    topic_model = BERTopic()
    topics, probs = topic_model.fit_transform(texts)

    # Get top n topics (excluding outlier topic -1)
    freq = topic_model.get_topic_info()
    top_topics = freq[freq.Topic != -1].head(top_n)

    topic_details = []
    for topic_id in top_topics.Topic:
        words = topic_model.get_topic(topic_id)
        topic_details.append({
            "Topic ID": topic_id,
            "Top Words": ", ".join([w for w, _ in words])
        })

    return topic_details, topic_model.visualize_topics()
