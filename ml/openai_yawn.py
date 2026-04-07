# import base64
# from dotenv import load_dotenv
# from openai import OpenAI
# import cv2
# import numpy as np

# load_dotenv()
# client = OpenAI()

# PROMPT = (
#     "Look at the person's face.\n"
#     "Is the person yawning?\n"
#     "Answer ONLY one word: NORMAL or YAWNING."
# )

# def confirm_yawn_with_openai(frame: np.ndarray) -> bool:
#     # Encode frame to JPEG
#     success, buf = cv2.imencode(".jpg", frame)
#     if not success:
#         return False

#     image_b64 = base64.b64encode(buf).decode("utf-8")

#     response = client.responses.create(
#         model="gpt-4.1-mini",
#         input=[{
#             "type": "message",
#             "role": "user",
#             "content": [
#                 {"type": "input_text", "text": PROMPT},
#                 {
#                     "type": "input_image",
#                     "image_url": f"data:image/jpeg;base64,{image_b64}"
#                 }
#             ]
#         }]
#     )

#     result = response.output_text.strip().upper()
#     return result == "YAWNING"
