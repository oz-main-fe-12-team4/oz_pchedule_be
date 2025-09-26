from rest_framework_simplejwt.authentication import JWTAuthentication


class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        # ✅ 쿠키에서 access_token 가져오기
        access_token = request.COOKIES.get("access_token")

        if not access_token:
            return None  # 쿠키 없으면 인증 안 됨

        try:
            validated_token = self.get_validated_token(access_token)
        except Exception:
            return None  # 유효하지 않으면 인증 실패

        return self.get_user(validated_token), validated_token
