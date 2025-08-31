# file: merge_audio_chunks_memory.py
import io
from pydub import AudioSegment
import os

def merge_audio_chunks_memory(chunks_bytes_list, output_file="my_voice_audiobook.wav", export_format="wav", save_to_disk=False):
    """
    Merge audio chunks (BytesIO) into a single audiobook.
    
    Args:
        chunks_bytes_list: list of BytesIO objects (audio chunks)
        output_file: final output filename
        export_format: "wav" or "mp3"
        save_to_disk: if True, saves the merged file to disk
    Returns:
        merged_audio_bytes: BytesIO of merged audiobook
    """
    if not chunks_bytes_list:
        print("❌ No chunks provided")
        return None

    # Load first chunk
    try:
        combined_audio = AudioSegment.from_file(chunks_bytes_list[0])
    except Exception as e:
        print(f"❌ Failed to load first chunk: {e}")
        return None

    # Merge remaining chunks
    for i, chunk_bytes in enumerate(chunks_bytes_list[1:], 1):
        try:
            audio = AudioSegment.from_file(chunk_bytes)
            combined_audio += audio
        except Exception as e:
            print(f"⚠️ Warning: Failed chunk {i}: {e}")
            continue

    # Export to BytesIO
    output_bio = io.BytesIO()
    combined_audio.export(output_bio, format=export_format)
    output_bio.seek(0)

    # Optional: save to disk
    if save_to_disk:
        combined_audio.export(output_file, format=export_format)
        print(f"💾 Merged audiobook saved as {output_file}")

    # Info
    duration_sec = len(combined_audio) / 1000
    print(f"🎉 Audiobook merged successfully!")
    print(f"⏱ Duration: {duration_sec/60:.1f} min ({duration_sec:.0f} sec)")
    print(f"📊 Approx size: {len(output_bio.getbuffer()) / (1024*1024):.1f} MB (in memory)")

    return output_bio
