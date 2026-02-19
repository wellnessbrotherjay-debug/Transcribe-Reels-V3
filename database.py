from supabase import create_client, Client
import streamlit as st
import datetime
import os

class DatabaseManager:
    def __init__(self):
        self.url = os.getenv("SUPABASE_URL")
        self.key = os.getenv("SUPABASE_KEY")
        self.supabase: Client = None

    def connect(self):
        if not self.url or not self.key:
            return False
        try:
            self.supabase = create_client(self.url, self.key)
            return True
        except Exception as e:
            st.error(f"Failed to connect to Supabase: {e}")
            return False

    def save_transcript(self, url, text, summary=None, metadata=None):
        if not self.supabase:
            return False
        
        data = {
            "url": url,
            "text": text,
            "summary": summary,
            "created_at": datetime.datetime.utcnow().isoformat(),
            "metadata": metadata or {}
        }
        try:
            # Upsert is trickier in Supabase without a unique constraint violation handling or specific upsert call
            # Assuming 'url' is a unique key or primary key in the table "transcripts"
            self.supabase.table("transcripts").upsert(data, on_conflict="url").execute()
            return True
        except Exception as e:
            st.error(f"Error saving to Supabase: {e}")
            return False

    def get_all_transcripts(self):
        if not self.supabase:
            return []
        try:
            response = self.supabase.table("transcripts").select("*").order("created_at", desc=True).execute()
            return response.data
        except Exception as e:
            st.error(f"Error fetching from Supabase: {e}")
            return []

    def search_transcripts(self, query):
        if not self.supabase:
            return []
        try:
            # Simple text search on the 'text' column using ilike
            # For full vector search, we'd need a different setup with embeddings
            response = self.supabase.table("transcripts").select("*").ilike("text", f"%{query}%").order("created_at", desc=True).execute()
            return response.data
        except Exception as e:
            st.error(f"Error searching Supabase: {e}")
            return []
