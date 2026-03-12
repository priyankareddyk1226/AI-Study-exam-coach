from yt_search import search_yt, get_best_video

materials = {

    "Algebra":
    "https://www.youtube.com/watch?v=grnP3mduZkM",

    "Calculus":
    "https://www.youtube.com/watch?v=WUvTyaaNkzM",

    "Mechanics":
    "https://www.youtube.com/results?search_query=mechanics+physics+tutorial",

    "Organic":
    "https://www.youtube.com/results?search_query=organic+chemistry+tutorial"

}
VIDEO_LINKS = {
    "arrays": 
    "https://www.youtube.com/watch?v=QJNwK2uJyGs",
    "linked list":
      "https://www.youtube.com/watch?v=njTh_OwMljA",
    "stacks": 
    "https://www.youtube.com/watch?v=wjI1WNcIntg",
    "queues": 
    "https://www.youtube.com/watch?v=okr-XE8yTO8",
    "number system": 
    "https://www.youtube.com/watch?v=RS3QWZ7V6h0",
    "boolean algebra": 
    "https://www.youtube.com/watch?v=6tMZQ7K1d6M",
    "oop concepts": 
    "https://www.youtube.com/watch?v=pTB0EiLXUC8",
    "collections": 
    "https://www.youtube.com/watch?v=RBSGKlAvoiM",
    "basics": 
    "https://www.youtube.com/watch?v=rfscVS0vtbw",
    "functions": 
    "https://www.youtube.com/watch?v=9Os0o3wzS_I",
    "oop": 
    "https://www.youtube.com/watch?v=Ej_02ICOIgs"
}

def get_youtube_link_for_topic(topic):
    """
    Get relevant YouTube link for a specific topic
    
    Args:
        topic (str): The topic to search for
        
    Returns:
        str: YouTube video URL or search results page
    """
    # Check if topic has a predefined link
    if topic in materials:
        return materials[topic]
    
    # Check if topic is in our video links database
    if topic.lower() in VIDEO_LINKS:
        return VIDEO_LINKS[topic.lower()]
    
    # Search YouTube for the topic
    try:
        best_video = get_best_video(f"{topic} tutorial lecture")
        if best_video and 'url' in best_video:
            return best_video['url']
    except Exception as e:
        print(f"Error fetching YouTube link: {str(e)}")
    
    # Fallback to search results page
    search_query = topic.replace(" ", "+") + "+tutorial"
    return f"https://www.youtube.com/results?search_query={search_query}"