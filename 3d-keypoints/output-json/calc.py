import json
import math

# Load OpenPose JSON output
with open("side_keypoints.json", "r") as f:
    data = json.load(f)

# Check if at least one person is detected
if len(data["people"]) > 0:
    keypoints = data["people"][0]["pose_keypoints_2d"]

    # Extract keypoint coordinates
    nose = (keypoints[0 * 3], keypoints[0 * 3 + 1])  # Nose (approximate head top)
    right_ankle = (keypoints[11 * 3], keypoints[11 * 3 + 1])  # Right ankle
    left_ankle = (keypoints[14 * 3], keypoints[14 * 3 + 1])  # Left ankle

    # Compute estimated body height in pixels
    body_height_pixels = max(right_ankle[1], left_ankle[1]) - nose[1]

    if body_height_pixels > 0:
        # Convert from pixels to cm using known real-world height
        real_body_height_cm = 173  # Given real-world height in cm
        pixel_to_cm_scale = real_body_height_cm / body_height_pixels

        # Extract shoulder and hip coordinates
        right_shoulder = (keypoints[2 * 3], keypoints[2 * 3 + 1])
        left_shoulder = (keypoints[5 * 3], keypoints[5 * 3 + 1])
        right_hip = (keypoints[9 * 3], keypoints[9 * 3 + 1])
        left_hip = (keypoints[12 * 3], keypoints[12 * 3 + 1])

        # Compute distances in pixels
        shoulder_distance_px = math.sqrt((left_shoulder[0] - right_shoulder[0])**2 +
                                         (left_shoulder[1] - right_shoulder[1])**2)
        hip_distance_px = math.sqrt((left_hip[0] - right_hip[0])**2 +
                                    (left_hip[1] - right_hip[1])**2)

        # Convert pixel distances to cm
        shoulder_distance_cm = shoulder_distance_px * pixel_to_cm_scale
        hip_distance_cm = hip_distance_px * pixel_to_cm_scale

        print(f"Shoulder Distance: {shoulder_distance_cm:.2f} cm")
        print(f"Hip Distance: {hip_distance_cm:.2f} cm")
        print(f"body height pixels: {body_height_pixels:.2f}")

    else:
        print("Error: Could not determine body height in pixels.")

else:
    print("No person detected in the JSON file.")

