import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from PIL import Image
import cv2
import os
import json
import numpy as np

# Initialize Moondream model
model = AutoModelForCausalLM.from_pretrained(
    "vikhyatk/moondream2",
    revision="2025-06-21",
    trust_remote_code=True,
    device_map={"": "cuda"}
)

model.compile()


def analyze_beach_crowd(video_path, frames_per_second=1):
    """
    Analyzes a beach video to determine if it's crowded or not.
    
    Args:
        video_path (str): Path to the video file in videos/ folder
        frames_per_second (int): Number of frames to extract per second (default: 1)
    
    Returns:
        dict: JSON-parseable results with crowd analysis for each frame and summary
    """
    full_video_path = os.path.join("videos", video_path)
    
    # Check if video exists
    if not os.path.exists(full_video_path):
        return {
            "error": f"Video file not found: {full_video_path}",
            "success": False
        }
    
    # Open video capture
    cap = cv2.VideoCapture(full_video_path)
    
    if not cap.isOpened():
        return {
            "error": f"Could not open video: {full_video_path}",
            "success": False
        }
    
    # Get video properties
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / fps
    
    # Calculate frame interval
    frame_interval = int(fps / frames_per_second)
    
    results = {
        "video": video_path,
        "duration_seconds": round(duration, 2),
        "total_frames_analyzed": 0,
        "frames_per_second": frames_per_second,
        "frame_analyses": [],
        "summary": {
            "is_crowded": False,
            "crowd_level": "unknown",
            "conclusion": ""
        }
    }
    
    frame_count = 0
    analyzed_frames = 0
    
    # Simple query for beach crowd analysis
    crowd_query = """Look at this beach image and determine if it's crowded or not.

Consider ONLY the sandy beach area (ignore water, sky, buildings).
A beach is CROWDED if:
- There are many people visible
- Little free sand space available for laying down
- The area feels busy and occupied

A beach is NOT CROWDED if:
- There are few or no people
- Plenty of free sand space available
- The area feels open and spacious

Answer with just one word: yes or no
(yes = crowded, no = not crowded)"""
    
    print(f"Analyzing video: {video_path}")
    print(f"Duration: {duration:.2f}s, FPS: {fps}, Total frames: {total_frames}")
    print(f"Extracting {frames_per_second} frame(s) per second...\n")
    
    while cap.isOpened():
        ret, frame = cap.read()
        
        if not ret:
            break
        
        # Extract frame at specified interval
        if frame_count % frame_interval == 0:
            # Convert BGR to RGB for PIL
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Convert to PIL Image
            pil_image = Image.fromarray(frame_rgb)
            
            # Query the model
            encoded_image = model.encode_image(pil_image)
            response = model.query(encoded_image, crowd_query)
            answer = response["answer"].strip().lower()
            
            # Parse the response
            is_crowded = "yes" in answer
            
            frame_result = {
                "frame_number": frame_count,
                "timestamp_seconds": round(frame_count / fps, 2),
                "is_crowded": is_crowded,
                "raw_response": answer
            }
            
            results["frame_analyses"].append(frame_result)
            analyzed_frames += 1
            
            print(f"Frame {frame_count} ({frame_count/fps:.2f}s): Crowded={is_crowded}")
        
        frame_count += 1
    
    cap.release()
    results["total_frames_analyzed"] = analyzed_frames
    
    # Calculate summary statistics
    if analyzed_frames > 0:
        crowded_count = sum(1 for f in results["frame_analyses"] if f["is_crowded"] is True)
        
        # Determine overall crowd level
        if analyzed_frames > 0:
            crowd_ratio = crowded_count / analyzed_frames
            if crowd_ratio >= 0.7:
                results["summary"]["is_crowded"] = True
                results["summary"]["crowd_level"] = "high"
            elif crowd_ratio >= 0.4:
                results["summary"]["is_crowded"] = True
                results["summary"]["crowd_level"] = "medium"
            else:
                results["summary"]["is_crowded"] = False
                results["summary"]["crowd_level"] = "low"
        
        # Generate conclusion
        results["summary"]["conclusion"] = generate_conclusion(results)
    
    return results


def parse_crowd_response(response):
    """
    Parses the model response to extract structured data.
    
    Args:
        response (str): Raw response from the model
    
    Returns:
        dict: Parsed data with is_crowded
    """
    parsed = {
        "is_crowded": None
    }
    
    try:
        # Extract CROWDED status
        if "CROWDED:" in response:
            crowded_part = response.split("CROWDED:")[1].strip().lower()
            parsed["is_crowded"] = "yes" in crowded_part
    except (ValueError, IndexError) as e:
        print(f"Warning: Could not parse response '{response}': {e}")
    
    return parsed


def generate_conclusion(results):
    """
    Generates a natural language conclusion from the analysis results.
    
    Args:
        results (dict): Analysis results dictionary
    
    Returns:
        str: Natural language conclusion
    """
    summary = results["summary"]
    crowd_level = summary["crowd_level"]
    
    if crowd_level == "low":
        return "The beach is not crowded. There's plenty of free space available."
    elif crowd_level == "medium":
        return "The beach has moderate attendance. Some free space is still available."
    else:
        return "The beach is crowded. Limited free space is available."


# Example usage
if __name__ == "__main__":
    # Example: analyze a video file
    video_file = "beach_video.mp4"  # Change this to your video file name
    
    # Run analysis
    analysis_results = analyze_beach_crowd(video_file, frames_per_second=1)
    
    # Print results as JSON
    print("\n" + "="*50)
    print("ANALYSIS RESULTS (JSON):")
    print("="*50)
    print(json.dumps(analysis_results, indent=2))
    
    # Save results to file
    output_file = f"analysis_{video_file.rsplit('.', 1)[0]}.json"
    with open(output_file, "w") as f:
        json.dump(analysis_results, f, indent=2)
    
    print(f"\nResults saved to: {output_file}")
