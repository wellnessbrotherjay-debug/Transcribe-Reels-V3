try:
    from moviepy import VideoFileClip
    print("Import SUCCESS")
    try:
        # Check if we can instantiate it (dummy check)
        print("VideoFileClip is:", VideoFileClip)
    except:
        pass
except Exception as e:
    print(f"Import FAILED: {e}")
