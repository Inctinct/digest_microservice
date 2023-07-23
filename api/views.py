from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Post, Digest

from api.serializers import PostSerializer


class DigestView(APIView):
    """Endpoint for creating a post digest"""

    def get(self, request):
        """
        The main application is the formation of a digest of current posts
        according to certain filter parameters.

        Exceptions
        ---------
        If there is no user by input id - 404
        If there are no relevant posts to form a digest - 204
        if something went wrong while trying to create an Digest object - 400
        """
        try:
            user = User.objects.get(id=request.GET.get("user_id"))
        except Exception:
            return Response("User not found", status.HTTP_404_NOT_FOUND)
        user_posts = Post.objects.filter(subscription_id__user_id=user)
        user_digests = Digest.objects.filter(user_id=user)
        actual_posts = self.posts_scanner(user_posts, user_digests)
        filtration_posts = self.posts_filtration(actual_posts)
        try:
            digest = Digest.objects.create(user_id=user)
            try:
                if len(filtration_posts) > 0:
                    digest.posts_list.set(filtration_posts)
                else:
                    raise Exception
            except Exception:
                digest.delete()
                return Response(
                    "No current posts found", status=status.HTTP_204_NO_CONTENT
                )
        except Exception:
            return Response(
                "Something went wrong while creating the digest",
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = PostSerializer(data=filtration_posts, many=True)
        serializer.is_valid()
        return Response(serializer.data, status=200)

    def posts_scanner(self, posts, digests):
        """
        A method for scanning posts and selecting
        relevant ones (which are not in previous user digests)

        Parameters
        ----------
        :param posts: List
        :param digests: List
        :return: actual_posts: List

        As a post scanner to find new ones,
        I use posts that were not in previous digests
        """
        irrelevant_posts = []
        for digest in digests:
            irrelevant_posts.extend(digest.posts_list.all())
        actual_posts = list(filter(lambda post: post not in irrelevant_posts, posts))
        return actual_posts

    def posts_filtration(self, actual_posts):
        """
        The method filters the scanned posts according
        to the criteria that are passed in the request

        Parameters
        ----------
        :param actual_posts: List
        :return: filtration_post: List

        For real use, I would take the parameters not from the request,
        but by the user's fields (He must have spheres by
        which we can filter and the minimum popularity rating of the posts
        that he wants to see in the digests)
        """
        filtration_posts = list(
            filter(
                lambda post: post.popularity >= int(self.request.GET.get("popularity"))
                and post.sphere in self.request.GET.get("spheres"),
                actual_posts,
            )
        )
        return filtration_posts
