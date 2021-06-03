from ast import Str
from django.db.models import fields
from graphene.types.scalars import String
from faces.models import Face, Image, Landmark
from faces.utils import CloudinaryResourceHandler, detect_faces, highlight_faces
import graphene
from graphene_django import DjangoObjectType
from graphene_file_upload.scalars import Upload
import cloudinary


class UploadMutation(graphene.Mutation):
    class Arguments:
        file = String(required=True)
        name = String()

    success = graphene.Boolean()

    def mutate(self, info, file, name, **kwargs):
        # do something with your file
        if file:
            cloudinary.config(
                cloud_name="homeline",
                api_key="391647762764684",
                api_secret="ZkIKMSYSAv6ITaFQx3h6VdT3F_M"
            )
            result = cloudinary.uploader.upload(file)
            url = result.get('url')
            faces = detect_faces(url)
            if faces:
               
                face_with_bound = highlight_faces(url, faces, "text.png")
                res = cloudinary.uploader.upload(face_with_bound)
                face_with_bound_url =  res.get('url')
                image = Image.objects.create(image_src=url, name=name, image_with_face_bound_src=face_with_bound_url)
                for face in faces:

                    # print(face)
                    # print('anger: {}'.format(likelihood_name[face.anger_likelihood]))
                    # print('joy: {}'.format(likelihood_name[face.joy_likelihood]))
                    # print('surprise: {}'.format(likelihood_name[face.surprise_likelihood]))
                    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                                       'LIKELY', 'VERY_LIKELY')
                    vertices = (['({},{})'.format(vertex.x, vertex.y)
                                for vertex in face.bounding_poly.vertices])
                    
                    face_model = Face.objects.create(
                        image=image,
                        surprise_likelihood=likelihood_name[face.surprise_likelihood],
                        headwear_likelihood=likelihood_name[face.headwear_likelihood],
                        blurred_likelihood=likelihood_name[face.blurred_likelihood],
                        under_exposed_likelihood=likelihood_name[face.under_exposed_likelihood],
                        anger_likelihood=likelihood_name[face.anger_likelihood],
                        sorrow_likelihood=likelihood_name[face.sorrow_likelihood],
                        joy_likelihood=likelihood_name[face.joy_likelihood],
                        landmarking_confidence=face.landmarking_confidence,
                        detection_confidence=face.detection_confidence,
                        tilt_angle=face.tilt_angle,
                        roll_angle=face.tilt_angle,
                        vertices=vertices
                    )

                    for landmark in face.landmarks:
                        Landmark.objects.create(
                            type=landmark.type_,
                            position_x=landmark.position.x,
                            position_y=landmark.position.y,
                            position_z=landmark.position.z,
                            face=face_model
                        )

                return UploadMutation(success=True)
        return UploadMutation(success=False)


class DeleteImage(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        id = graphene.ID()

    @classmethod
    def mutate(cls, root, info, **kwargs):
        obj = Image.objects.get(pk=kwargs["id"])
        obj.delete()
        return cls(ok=True)


class FaceType(DjangoObjectType):
    class Meta:
        model = Face
        fields = ("id", "surprise_likelihood", "headwear_likelihood", "blurred_likelihood", "under_exposed_likelihood", "anger_likelihood",
                  "sorrow_likelihood", "joy_likelihood", "landmarking_confidence", "detection_confidence", "tilt_angle", "roll_angle",  "vertices", 'landmarks')


class ImageType(DjangoObjectType):
    class Meta:
        model = Image
        fields = ("id", "image_src", "name", "faces", "image_with_face_bound_src")


class LandmarkType(DjangoObjectType):
    class Meta:
        model = Landmark
        fields = ("id", "type", "position_x",
                  "position_y", 'position_z', 'face')


class Mutation(graphene.ObjectType):
    upload_image = UploadMutation.Field()
    delete_image = DeleteImage.Field()


class Query(graphene.ObjectType):

    images = graphene.List(ImageType)

    def resolve_images(root, info):
        return Image.objects.all()
