import yt_dlp
import sys

def generate_js_array(playlist_url):
    # yt-dlp options to only extract metadata (fast), not download the videos
    ydl_opts = {
        'extract_flat': True,
        'quiet': True
    }
    
    print("Fetching playlist data from YouTube. Please wait...")
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extract playlist info
            info = ydl.extract_info(playlist_url, download=False)
            
            if 'entries' not in info:
                print("Error: Could not find playlist entries. Make sure the link contains 'list=' parameter.")
                return
            
            entries = info['entries']
            total_videos = len(entries)
            
            # Start formatting the JavaScript array
            output_lines = ["const officialTracks = ["]
            for index, entry in enumerate(entries):
                if entry is None:
                    continue
                    
                # Clean up title for JavaScript (escape double quotes)
                title = entry.get('title', f'Video {index+1}').replace('"', '\\"')
                yt_id = entry.get('id', '')
                meta = f"Day {index + 1}" # Or whatever default meta you want
                
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
                
            print(f"\nSuccess! Successfully extracted {total_videos} videos.")
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