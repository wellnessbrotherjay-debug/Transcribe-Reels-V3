try:
    import cv2
    print(f"CV2 Import SUCCESS: {cv2.__version__}")
except Exception as e:
    print(f"CV2 Import FAILED: {e}")

try:
    import scenedetect
    print(f"SceneDetect Import SUCCESS: {scenedetect.__version__}")
    from scenedetect import open_video, SceneManager
    from scenedetect.detectors import ContentDetector
    print("SceneDetect objects imported successfully")
except Exception as e:
    print(f"SceneDetect Import FAILED: {e}")

try:
    from moviepy import VideoFileClip
    print("MoviePy Import SUCCESS (v2 style)")
except Exception as e:
    print(f"MoviePy Import FAILED: {e}")
