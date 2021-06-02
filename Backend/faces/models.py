from django.db import models


class Image(models.Model):
    image_src =  models.CharField(max_length=1000)
    name = models.CharField(max_length=255, blank=True, null=True)
    image_with_face_bound_src = models.CharField(max_length=1000, blank=True , null=True) 
    

class Face(models.Model):
    surprise_likelihood = models.CharField(blank=True, null=True, max_length=255)
    image = models.ForeignKey("Image", related_name="faces", on_delete=models.CASCADE)
    headwear_likelihood =   models.CharField(blank=True, null=True, max_length=255)
    blurred_likelihood =  models.CharField(blank=True, null=True, max_length=255)
    under_exposed_likelihood =  models.CharField(blank=True, null=True, max_length=255)
    anger_likelihood = models.CharField(blank=True, null=True, max_length=255)
    sorrow_likelihood = models.CharField(blank=True, null=True, max_length=255)
    joy_likelihood =  models.CharField(blank=True, null=True, max_length=255)
    landmarking_confidence = models.CharField(blank=True, null=True, max_length=255)
    detection_confidence = models.CharField(blank=True, null=True, max_length=255)
    tilt_angle = models.CharField(blank=True, null=True, max_length=255)
    roll_angle =  models.CharField(blank=True, null=True, max_length=255)
    vertices =  models.CharField(blank=True, null=True, max_length=255)


class Landmark(models.Model):
    type = models.CharField(max_length=255, blank=True, null=True)
    position_x = models.FloatField(max_length=255, blank=True, null=True)
    position_y = models.FloatField(max_length=255, blank=True, null=True)
    position_z = models.FloatField(max_length=255, blank=True, null=True)
    face = models.ForeignKey("Face", on_delete=models.CASCADE, related_name='landmarks')

    def __str__(self) -> str:
        return self.type
