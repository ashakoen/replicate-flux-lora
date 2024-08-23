import json
import sys

import replicate
from dotenv import load_dotenv
from loguru import logger

load_dotenv()

# Configure Loguru
logger.remove()  # Remove the default handler
logger.add(
    sys.stderr, format="{time} {level} {message}", filter="my_module", level="INFO"
)
logger.add(
    "image_generator.log",
    rotation="10 MB",
    format="{time} {level} {message}",
    level="INFO",
)


class ImageGenerator:
    def __init__(self):
        self.replicate_model = None
        logger.info("ImageGenerator initialized")

    def set_model(self, replicate_model):
        self.replicate_model = replicate_model
        logger.info(f"Model set to: {replicate_model}")

    def generate_images(self, params):
        if not self.replicate_model:
            error_message = (
                "No Replicate model set. Please set a model before generating images."
            )
            logger.error(error_message)
            raise ImageGenerationError(error_message)

        try:
            # Remove the Flux model from params and store it separately
            flux_model = params.pop("flux_model", "dev")

            # Add the Flux model choice to the input parameters
            params["model"] = flux_model

            logger.info(
                f"Generating images with params: {json.dumps(params, indent=2)}"
            )
            logger.info(f"Using Replicate model: {self.replicate_model}")

            output = replicate.run(self.replicate_model, input=params)

            logger.success(f"Images generated successfully. Output: {output}")
            return output
        except Exception as e:
            error_message = f"Error generating images: {str(e)}"
            logger.exception(error_message)
            raise ImageGenerationError(error_message)


class ImageGenerationError(Exception):
    pass