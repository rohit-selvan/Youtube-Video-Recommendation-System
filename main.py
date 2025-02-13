import tkinter as tk
from tkinter import messagebox
import requests
import webbrowser

API_KEY =  # Replace with your YouTube Data API key

class YouTubeRecommender(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("YouTube Video Recommender")
        self.geometry("700x500")
        self.configure(bg="#f0f4f8")
        self.create_widgets()

    def create_widgets(self):
        # Title
        tk.Label(self, text="YouTube Video Recommender", font=("Verdana", 24, "bold"), bg="#f0f4f8", fg="#2c3e50").pack(pady=20)
        
        # Keyword Entry
        tk.Label(self, text="Enter a keyword or topic:", font=("Verdana", 14), bg="#f0f4f8").pack(pady=5)
        self.keyword_entry = tk.Entry(self, font=("Verdana", 14), width=50)
        self.keyword_entry.pack(pady=10)
        
        # Search Button
        tk.Button(self, text="Search", command=self.search_videos, font=("Verdana", 14), bg="#3498db", fg="white", width=15).pack(pady=10)
        
        # Results Display
        self.result_text = tk.Text(self, font=("Verdana", 12), height=15, width=80, state=tk.DISABLED, wrap=tk.WORD)
        self.result_text.pack(pady=10)

    def search_videos(self):
        keyword = self.keyword_entry.get().strip()
        if not keyword:
            messagebox.showwarning("Input Error", "Please enter a keyword.")
            return
        
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, "Fetching recommendations...\n")
        self.result_text.config(state=tk.DISABLED)
        self.update()

        videos = self.fetch_videos(keyword)
        if videos:
            self.display_results(videos)
        else:
            messagebox.showerror("Error", "No videos found or failed to fetch data.")

    def fetch_videos(self, keyword):
        url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={keyword}&type=video&maxResults=5&key={API_KEY}"
        try:
            response = requests.get(url)
            data = response.json()
            videos = [
                {
                    "title": item["snippet"]["title"],
                    "url": f"https://www.youtube.com/watch?v={item['id']['videoId']}"
                }
                for item in data.get("items", [])
            ]
            return videos
        except Exception as e:
            print(f"Error fetching videos: {e}")
            return None

    def display_results(self, videos):
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete("1.0", tk.END)
        for i, video in enumerate(videos, start=1):
            self.result_text.insert(tk.END, f"{i}. {video['title']}\n")
            self.result_text.insert(tk.END, f"   Watch: {video['url']}\n\n")
        self.result_text.config(state=tk.DISABLED)
        self.result_text.bind("<Double-1>", lambda e: self.open_link(videos))

    def open_link(self, videos):
        selection = self.result_text.index(tk.CURRENT).split(".")[0]
        try:
            video_index = int(selection) - 1
            webbrowser.open(videos[video_index]["url"])
        except (ValueError, IndexError):
            pass

if __name__ == "__main__":
    app = YouTubeRecommender()
    app.mainloop()
