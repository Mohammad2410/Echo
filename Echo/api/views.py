from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Post
from .chroma_helper import add_post_to_chroma, search_posts

@api_view(["POST"])
def add_post(request):
    """Add a new post with embedding."""
    title = request.data.get("title")
    content = request.data.get("content")

    if not title or not content:
        return Response({"error": "Title and content are required."}, status=400)

    post = Post.objects.create(title=title, content=content)
    add_post_to_chroma(title, content)

    return Response({"message": "Post added successfully!"})


from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET"])  # ✅ Ensure GET method is allowed
def search(request):
    """Search posts using hybrid semantic search."""
    query = request.GET.get("query", "").strip()

    if not query:
        return Response({"error": "Query parameter is required."}, status=400)

    results = search_posts(query)  # Make sure this function works correctly

    return Response({"results": results})
