
import yt_dlp
import json

def fetch_playlist_with_ytdlp(playlist_url):
    """
    Fetch playlist videos using yt-dlp
    
    Args:
        playlist_url: Full YouTube playlist URL
    
    Returns:
        Dictionary with video titles as keys and video URLs as values
    """
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,  # Don't download, just extract metadata
        'dump_single_json': True,
    }
    
    videos = {}
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extract playlist info
            playlist_info = ydl.extract_info(playlist_url, download=False)
            
            if 'entries' in playlist_info:
                for entry in playlist_info['entries']:
                    if entry:  # Sometimes entries can be None
                        title = entry.get('title', '').lower()
                        video_id = entry.get('id', '')
                        
                        if title and video_id:
                            # Clean up title
                            title = title.replace(' - official video', '').replace(' (official)', '')
                            video_url = f"https://www.youtube.com/watch?v={video_id}"
                            videos[title] = video_url
            
    except Exception as e:
        print(f"Error extracting playlist: {e}")
        return {}
    
    return videos

def update_music_library_ytdlp(playlist_url, music_file_path="musicLibrary.py"):
    """
    Update musicLibrary.py using yt-dlp
    """
    print("Fetching playlist videos...")
    new_videos = fetch_playlist_with_ytdlp(playlist_url)
    
    if not new_videos:
        print("No videos found or error occurred")
        return
    
    # Read existing music library
    try:
        with open(music_file_path, 'r') as f:
            content = f.read()
        
        # Extract existing music dictionary
        exec(content)
        existing_music = locals().get('music', {})
        
    except FileNotFoundError:
        existing_music = {}
    
    # Merge dictionaries
    existing_music.update(new_videos)
    
    # Write back to file
    with open(music_file_path, 'w') as f:
        f.write("music = {\n")
        for title, url in existing_music.items():
            f.write(f'    "{title}": "{url}",\n')
        f.write("}\n")
    
    print(f"Updated music library with {len(new_videos)} new videos")
    print("Sample entries:")
    for i, (title, url) in enumerate(list(new_videos.items())[:5]):
        print(f"  '{title}': '{url}'")

# Example usage:
if __name__ == "__main__":
    # Your playlist URL
    PLAYLIST_URL = "https://www.youtube.com/watch?v=vC8qJfVYxZY&list=PLcntfnW2Yy8PapiGtkAh8_uGv8nHZeQES&pp=gAQB"
    
    update_music_library_ytdlp(PLAYLIST_URL)
    

music = {
    "you & me": "https://www.youtube.com/watch?v=IAvw60x0Kn4",
    "mvp" : "https://www.youtube.com/watch?v=gP4k_iruyAM",
    "playlist" : "https://www.youtube.com/watch?v=vC8qJfVYxZY&list=PLcntfnW2Yy8PapiGtkAh8_uGv8nHZeQES&pp=gAQB",
}
