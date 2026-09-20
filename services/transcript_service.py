from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled


def fetch_transcript(video_id: str) -> str:
    try:
        api = YouTubeTranscriptApi()

        transcript_list = api.fetch(
            video_id=video_id,
            languages=["en"]
        )

        transcript_data = transcript_list.to_raw_data()

        transcript = " ".join(
            chunk["text"]
            for chunk in transcript_data
        )

        return transcript

    except TranscriptsDisabled:
        raise RuntimeError(
            "No captions available for this video."
        )