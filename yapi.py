from typing import Any, Sequence

class yApi():
    def __init__(self, youtube: Any = None, 
                 parts: Sequence[str] = None) -> None:
        
        self.youtube = youtube
        self.parts = ','.join(parts)
    
    def get_search_data(self, **kwargs: Any) -> dict:
        video_data = self.youtube.search().list(part=self.parts, **kwargs).execute()
        return video_data
    
    def get_video_data(self, **kwargs: Any) -> dict:
        video_data = self.youtube.videos().list(part=self.parts, **kwargs).execute()
        return video_data
    
