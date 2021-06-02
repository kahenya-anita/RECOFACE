
from io import BytesIO

import base64

from django.core.exceptions import ValidationError
import cloudinary.uploader as uploader
from django.utils.datastructures import MultiValueDictKeyError

from PIL import Image, ImageDraw
import requests



class CloudinaryResourceHandler:
    """This class contains methods for handling Cloudinary
    Resources, ie images and vidoes."""

    def upload_image(self, image):
        """Upload an image to cloudinary and return the url.
        The image should be an instance of Django's UploadedFile
        class. Read more about the UploadedFile class here
        https://docs.djangoproject.com/en/2.2/ref/files/uploads/#django.core.files.uploadedfile.UploadedFile
        Image file is first validated before being uploaded.
        """
        try:
            result = uploader.upload(image)
            url = result.get('url')
            return url
        # Cloudinary might still throw an error if validation fails.
        except Exception as e:
            raise ValidationError({
                'image':
                ('Image is either corrupted or of an unkown format. '
                    'Please try again with a different image file.')
            }) from e

    def upload_image_from_request(self, request):
        """Upload an image directly from a request object.
        params:
            request - incoming request object
        Return:
            the url if upload is successful.
        """
        try:
            image_main = request.FILES['image_main']

            if image_main:
                url = self.upload_image(image_main)
                return url

        except MultiValueDictKeyError:
            # This error will be raised if `image_main` is not an
            # uploaded file. There is no need to raise an error in that
            # case
            pass

    def upload_video(self, video):
        """Upload a video file to Cloudinary.
        First validate that the video file is of supported size
        and format before uploading.
        params:
            video - Video file to be uploaded
        Return:
            Cloudinary video url if upload is successful
        """
        try:

            res = uploader.upload_large(
                video, resource_type="video")
            url = res.get('url')
            return url
        except Exception as e:
            # Cloudinary might throw an error during upload
            raise ValidationError({
                'video': ('Video is either corrupted or of an unkown format.'
                          'Please try again with a different video file.')
            }) from e

    def upload_video_from_request(self, request):
        """Upload a video direclty from a request object.
        If users submit a video link, we return that link to be
        saved to the database.
        If they submit a video file, we upload the file to Cloudinary
        and return the url to be saved to the database."""

        video_file = request.FILES.getlist('video')
        video_link = request.data.get('video')
        if video_file:
            # We only allow users to upload maximum of one video
            url = self.upload_video(video_file[0])
            return url
        elif video_link:
            return video_link

    def get_cloudinary_public_id(self, url):
        """Get the `public_id` of a Cloudinary resource from the url.
        params:
            url - Url of the resource
        returns:
            public_id of the cloudinary resource if the url is valid
            Raise Validation error if it is not a Cloudinary url
        """
        # validate that the url is a valid cloudinary url first. If it is not
        # then a ValidationError is raised. You should handle this exception
        # and implement logic to fit your needs if the url isn't Cloudinary's

        file_name = url.split('/')[-1]
        public_id = file_name.split('.')[0]
        return public_id

    def delete_cloudinary_resource(self, instance, payload):
        """Delete a Cloudinary resource.
        params:
            instance - instance of the model from which to delete the resource.
            payload - dictionary where the key is the field to find the
                      resource and the value is the url to delete from field.
        We check the field to confirm that the value is stored there and
        proceed to delete it from the database and also from Cloudinary.
        Return:
            updated_fields - Dictionary containting the updated values of
                             our model. Should be passed to the serailizer
                             for updating.
        """
        # we need to ensure that the payload is an instance of a dictionary
        # and can be converted to one before we proceed.

        updated_fields = {}

        deleted_image_others = payload.get('image_others')
        deleted_video = payload.get('video')

        image_list_in_DB = instance.image_others.copy() if instance.image_others else []  # noqa
        video_in_DB = instance.video
        if deleted_image_others:
            for image in deleted_image_others:
                if image in image_list_in_DB:
                    try:
                        public_image_id = self.get_cloudinary_public_id(image)
                        uploader.destroy(public_image_id, invalidate=True)
                        instance.image_others.remove(image)
                    except ValidationError:
                        # if the image is not from cloudinary, we simply delete
                        # it from the DB
                        instance.image_others.remove(image)
            updated_fields['image_others'] = instance.image_others

        if video_in_DB == deleted_video:

            try:
                # because video urls don't have to be cloudinary urls,
                # we first try and check if it's a cloudinary resource
                # before deleting it.
                public_video_id = self.get_cloudinary_public_id(deleted_video)

            except ValidationError:
                # if the video in the DB is not a cloudinary url, we just pass
                # but still delete it from the DB in the `finally`
                # statement below
                pass

            finally:
                # as long as the video link in the request matches that in
                # the database we delete that video from the database.
                instance.video = None

            updated_fields['video'] = None

        instance.save()
        return updated_fields


def detect_faces(path):
    """Detects faces in an image."""
    from google.cloud import vision
    import io
    client = vision.ImageAnnotatorClient()
    source = vision.ImageSource(image_uri=path)
    image = vision.Image(source=source)

    response = client.face_detection(image=image)
    faces = response.face_annotations

    # Names of likelihood from google.cloud.vision.enums
    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                       'LIKELY', 'VERY_LIKELY')

    if len(faces) == 0:
        return

 

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

    return faces

def img_to_base64_str(img):
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    buffered.seek(0)
    img_byte = buffered.getvalue()
    img_str = "data:image/png;base64," + base64.b64encode(img_byte).decode()

    return img_str

def highlight_faces(image, faces, output_filename):
    """Draws a polygon around the faces, then saves to output_filename.
    Args:
      image: a file containing the image with the faces.
      faces: a list of faces found in the file. This should be in the format
          returned by the Vision API.
      output_filename: the name of the image file to be created, where the
          faces have polygons drawn around them.
    """
    im = Image.open(requests.get(image, stream=True).raw)
    draw = ImageDraw.Draw(im)
    # Sepecify the font-family and the font-size
    for face in faces:
        box = [(vertex.x, vertex.y)
               for vertex in face.bounding_poly.vertices]
        draw.line(box + [box[0]], width=5, fill='#00ff00')
        # Place the confidence value/score of the detected faces above the
        # detection box in the output image
        draw.text(((face.bounding_poly.vertices)[0].x,
                   (face.bounding_poly.vertices)[0].y - 30),
                  str(format(face.detection_confidence, '.3f')) + '%',
                  fill='#FF0000')
    return img_to_base64_str(im)
    # im.save(output_filename)
