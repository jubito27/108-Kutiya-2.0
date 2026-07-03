import yt_dlp

def generate_js_array(playlist_url):
    # yt-dlp options to only extract metadata (fast), not download the videos
    ydl_opts = {
        'extract_flat': True,
        'quiet': True,
        'skip_download': True
    }
    
    print("Fetching playlist data from YouTube. Please wait...")
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extract playlist info
            info = ydl.extract_info(playlist_url, download=False)
            
            if not info or 'entries' not in info:
                print("Error: Could not find playlist entries. Make sure the link contains 'list=' parameter.")
                return
            
            entries = info['entries']
            total_videos = len(entries)
            
            # Start formatting the JavaScript array
            output_lines = ["const officialTracks = ["]
            
            for index, entry in enumerate(entries):
                if not entry:
                    continue
                
                # Safely handle missing titles
                raw_title = entry.get('title')
                if raw_title is None:
                    title = f'Video {index+1}'
                else:
                    title = raw_title.replace('"', '\\"')
                
                yt_id = entry.get('id', '') or ''
                meta = f"Day {index + 1}"  # Default meta
                
                # Format the exact line
                line = f'    {{ title: "{title}", meta: "{meta}", ytId: "{yt_id}" }}'
                
                # Add a comma if it's not the last item
                if index < total_videos - 1:
                    line += ","
                
                output_lines.append(line)
            
            output_lines.append("];")
            
            # Save the formatted output to a text file
            file_name = "playlist_tracks.txt"
            with open(file_name, "w", encoding="utf-8") as f:
                f.write("\n".join(output_lines))
                
            print(f"\nSuccess! Extracted {total_videos} videos (some may be unavailable).")
            print(f"The formatted code has been saved to '{file_name}' in the same folder.")
            
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        print("Please make sure you entered a valid YouTube Playlist link.")

if __name__ == "__main__":
    print("--- YouTube Playlist Code Generator ---")
    url = input("Enter the YouTube Video/Playlist URL: ").strip()
    
    if url:
        generate_js_array(url)
    else:
        print("No URL provided. Exiting.")
