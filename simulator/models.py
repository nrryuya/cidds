from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from safedelete.models import SafeDeleteModel
import uuid
import os

def get_image_path(instance, filename):
    return os.path.join('images', str(instance.id), filename)

class SimulationResults(SafeDeleteModel):
    # unique id for each simulation
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # User who initiated the error
    user = models.ForeignKey(
        User,
        null=True,
        editable=False,
        on_delete=models.PROTECT,
        verbose_name="Created by user",
        help_text="User who created the simulation"
    )
# Number of processes
    num_process = models.IntegerField(blank=False, null=False, default= 1)

# Number of transactions
    transactions = models.IntegerField(blank=False, null=False, default = 10)


    alpha = models.FloatField(blank=False, null=False, default=1)

# Degree of randomness
    randomness = models.FloatField(blank=False, null=False, default=1)

# Tip selection algorithm
    algorithm = models.CharField(blank=True, max_length=10,
                                help_text="A short description of the simulation")

    # reference text for the simulation
    reference =  models.TextField(blank=True,
                                  help_text= "A short description of the simulation" )

    # Picked version of the entire tangle
    tangle = models.TextField(blank=True,
                                  help_text= "The tangle result from the simulation" )


    # resultant plotted image
    image = models.ImageField(upload_to=get_image_path, blank=True, null=True)

    # Created time
    created = models.DateTimeField(editable=False, default=timezone.now())

    # modified time
    modified = models.DateTimeField(null=True)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(SimulationResults, self).save(*args, **kwargs)






