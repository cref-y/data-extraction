from flask import Flask, request, jsonify
from data_extraction import remove_background,image_preprocess,extract_ocr_results,extract_id_info
import os
import logging

# Remove the PORT import from config since we'll handle it directly
# from config import PORT

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set port before creating the app
port = int(os.environ.get("PORT", 8080))
app = Flask(__name__)

@app.route("/", methods=["GET"])
def health_check():
    logger.info("Health check endpoint called")
    return jsonify({"status": "healthy"}), 200

@app.route("/extract_data", methods=["POST"])
def process_id_card():
    try:
        data = request.get_json()
        input_image = data.get("image_path") 
        if not input_image:
            return jsonify({"error": "No image path provided"}), 400
        output_image = remove_background(input_image)
        sharpened = image_preprocess(output_image)
        ocr_results = extract_ocr_results(sharpened)
        extracted_info = extract_id_info(ocr_results)
        return jsonify({"extracted_info": extracted_info}), 200
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run()