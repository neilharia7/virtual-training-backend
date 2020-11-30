from typing import Optional

from fastapi import HTTPException
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security import OAuth2
from fastapi.security.base import SecurityBase
from fastapi.security.utils import get_authorization_scheme_param
from starlette.requests import Request
from starlette.status import HTTP_403_FORBIDDEN


class BasicAuth(SecurityBase):
	def __init__(self, scheme_name: str = None, auto_error: bool = True):
		"""

		:param scheme_name:
		:param auto_error:
		"""
		self.scheme_name = scheme_name or self.__class__.__name__
		self.auto_error = auto_error
	
	async def __call__(self, request: Request) -> Optional[str]:
		authorization: str = request.headers.get("Authorization")
		scheme, param = get_authorization_scheme_param(authorization)
		if not authorization or scheme.lower() != "basic":
			if self.auto_error:
				raise HTTPException(
					status_code=HTTP_403_FORBIDDEN, detail="Not authenticated"
				)
			else:
				return None
		return param


basic_auth = BasicAuth(auto_error=False)


class OAuth2PasswordBearerCookie(OAuth2):
	def __init__(
			self,
			tokenUrl: str,
			scheme_name: str = None,
			scopes: dict = None,
			auto_error: bool = True,
	):
		if not scopes:
			scopes = {}
		flows = OAuthFlowsModel(password={"tokenUrl": tokenUrl, "scopes": scopes})
		super().__init__(flows=flows, scheme_name=scheme_name, auto_error=auto_error)
	
	async def __call__(self, request: Request) -> Optional[str]:
		header_authorization: str = request.headers.get("Authorization")
		cookie_authorization: str = request.cookies.get("Authorization")
		
		header_scheme, header_param = get_authorization_scheme_param(header_authorization)
		cookie_scheme, cookie_param = get_authorization_scheme_param(cookie_authorization)
		
		if header_scheme.lower() == "bearer":
			authorization = True
			scheme = header_scheme
			param = header_param
		
		elif cookie_scheme.lower() == "bearer":
			authorization = True
			scheme = cookie_scheme
			param = cookie_param
		
		else:
			authorization = False
			scheme, param = str(), str()
		
		if not authorization or scheme.lower() != "bearer":
			if self.auto_error:
				raise HTTPException(
					status_code=HTTP_403_FORBIDDEN, detail="Not authenticated"
				)
			else:
				return None
		else:
			return param


oauth2_scheme = OAuth2PasswordBearerCookie(tokenUrl="/token")
