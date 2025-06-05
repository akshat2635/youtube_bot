from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound

def get_transcript(video_id: str) -> str:
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

        try:
            transcript = transcript_list.find_manually_created_transcript(['en'])
        except NoTranscriptFound:
            try:
                transcript = transcript_list.find_generated_transcript(['en'])
            except NoTranscriptFound:
                all_languages = transcript_list._generated_transcripts.keys() or transcript_list._manually_created_transcripts.keys()
                try:
                    transcript = transcript_list.find_transcript(all_languages).translate('en')
                except Exception:
                    raise NoTranscriptFound(video_id, ['en'], transcript_list)

        transcript_data = transcript.fetch()
        return " ".join([item.text for item in transcript_data])

    except (TranscriptsDisabled, NoTranscriptFound):
        return ""
