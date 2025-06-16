from django.utils.deprecation import MiddlewareMixin
class TenantMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Allow paths like admin, swagger, redoc etc.
        open_paths = [
            '/admin', '/swagger', '/redoc', '/favicon.ico', '/docs', '/openapi'
        ]

        # Allow POST /tenants/ to register without an API key
        if request.path.startswith('/tenants/') and request.method == 'POST':
            return

        if any(request.path.startswith(p) for p in open_paths):
            return

        api_key = request.headers.get('X-API-KEY')
        if not api_key:
            return JsonResponse({'error': 'API key required'}, status=401)

        try:
            tenant = Tenant.objects.get(api_key=api_key)
            request.tenant = tenant
        except Tenant.DoesNotExist:
            return JsonResponse({'error': 'Invalid API key'}, status=403)
