"""
YouTube Search Helper Module
Fetches relevant YouTube video links for study topics
"""

from youtubesearchpython import VideosSearch
import time

# Cache to store search results to avoid redundant API calls
CACHE = {}

def search_yt(query, max_results=5):
    """
    Search YouTube for relevant videos
    
    Args:
        query (str): Search query/topic
        max_results (int): Maximum number of results to return
        
    Returns:
        list: List of dictionaries containing video info (title, url, duration, channel)
    """
    try:
        # Check cache first
        if query in CACHE:
            return CACHE[query]
        
        # Search YouTube
        videos_search = VideosSearch(query, limit=max_results)
        results = videos_search.result()
        
        if results and 'result' in results:
            video_list = []
            
            for video in results['result']:
                video_info = {
                    'title': video.get('title', 'Unknown'),
                    'url': video.get('link', ''),
                    'duration': video.get('duration', 'Unknown'),
                    'channel': video.get('channel', {}).get('name', 'Unknown'),
                    'thumbnail': video.get('thumbnails', [{}])[0].get('url', '')
                }
                video_list.append(video_info)
            
            # Cache the results
            CACHE[query] = video_list
            return video_list
        
        return []
        
    except Exception as e:
        print(f"YouTube search error: {str(e)}")
        return []


def get_best_video(query):
    """
    Get the best/most relevant video for a topic
    
    Args:
        query (str): Search query/topic
        
    Returns:
        dict or None: Best video info or None if not found
    """
    try:
        results = search_yt(query, max_results=1)
        if results:
            return results[0]
        return None
    except Exception as e:
        print(f"Error getting best video: {str(e)}")
        return None


def clear_cache():
    """Clear the search cache"""
    global CACHE
    CACHE = {}
