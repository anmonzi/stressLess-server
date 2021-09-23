from django.db import models



class Post(models.Model):
    """Post Model"""
    app_user = models.ForeignKey("AppUser", on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    image_url = models.TextField()
    publication_date = models.DateTimeField()
    reactions = models.ManyToManyField("AppUser", through="PostReaction", related_name="favorited")

    @property
    def owner(self):
        """returns owner of post"""
        return self.__owner

    @owner.setter
    def owner(self, value):
        self.__owner = value

    @property
    def comment_count(self):
        return self.__comment_count

    @comment_count.setter
    def comment_count(self, value):
        self.__comment_count = value

    @property
    def favorited(self):
        return self.__favorited

    @favorited.setter
    def favorited(self, value):
        self.__favorited = value

    @property
    def reactions_count(self):
        length = len(self.reactions.all())
        return length

    @reactions_count.setter
    def reactions_count(self, value):
        self.__reactions_count = value