from imagekitio import ImageKit
from django.conf import settings

def get_imagekit_client():
    """ Returns an instance of the ImageKit client """
    # En la versión 4.0.0, no debemos pasar base_url al menos que queramos
    # cambiar el endpoint de la API. El url_endpoint es para generación de URLs.
    return ImageKit(
        private_key=settings.IMAGEKIT_PRIVATE_KEY
    )

def upload_image_to_imagekit(file_content, file_name, folder="general/"):
    """
    Uploads an image to ImageKit and returns the response.
    
    :param file_content: The image file content (bytes or file-like object)
    :param file_name: The name of the file to save in ImageKit
    :param folder: The folder in ImageKit where the image will be stored
    :return: The API response from ImageKit
    """
    ik = get_imagekit_client()
    
    upload_response = ik.files.upload(
        file=file_content,
        file_name=file_name,
        folder=folder,
        use_unique_file_name=True,
        is_private_file=False,
    )
    
    return upload_response

def delete_image_from_imagekit(file_id):
    """
    Deletes an image from ImageKit by its file_id.
    
    :param file_id: The ID of the file to delete in ImageKit
    :return: True if successful, raises exception otherwise
    """
    if not file_id:
        return False
        
    ik = get_imagekit_client()
    try:
        ik.files.delete(file_id)
        return True
    except Exception as e:
        print(f"Error deleting from ImageKit: {str(e)}")
        return False
