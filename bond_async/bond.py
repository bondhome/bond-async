"""Bond Local API wrapper."""

from typing import Any, Callable, List, Optional
from xmlrpc.client import Boolean

from aiohttp import ClientSession, ClientTimeout
from aiohttp.client_exceptions import ServerDisconnectedError, ClientOSError

from bond_async.bond_type import BondType

from .action import Action


class Bond:
    """Bond API."""

    def __init__(
        self,
        host: str,
        token: str,
        *,
        session: Optional[ClientSession] = None,
        timeout: Optional[ClientTimeout] = None,
    ):
        """Initialize Bond with provided host and token."""
        self._host = host
        self._api_kwargs = {"headers": {"BOND-Token": token}}
        if timeout:
            self._api_kwargs["timeout"] = timeout
        self._session = session

    async def version(self) -> dict:
        """Return the version of Bond reported by API."""
        return await self.__get("/v2/sys/version")

    async def bond_type(self) -> BondType:
        """Return the BondType based on the serial number reported by API."""
        version = await self.version()
        return BondType.from_serial(version["bondid"])

    async def token(self) -> dict:
        """Return the token after power rest or proof of ownership event."""
        return await self.__get("/v2/token")

    async def bridge(self) -> dict:
        """Return the name and location of the bridge."""
        return await self.__get("/v2/bridge")

    async def devices(self) -> List[str]:
        """Return the list of available device IDs reported by API."""
        json = await self.__get("/v2/devices")
        return [
            key for key in json if not key.startswith("_") and type(json[key]) is dict
        ]

    async def device(self, device_id: str) -> dict:
        """Return main device metadata reported by API."""
        return await self.__get(f"/v2/devices/{device_id}")

    async def device_properties(self, device_id: str) -> dict:
        """Return device properties reported by API."""
        return await self.__get(f"/v2/devices/{device_id}/properties")

    async def device_state(self, device_id: str) -> dict:
        """Return current device state reported by API."""
        return await self.__get(f"/v2/devices/{device_id}/state")

    async def device_skeds(self, device_id: str) -> dict:
        """Return current device schedules reported by API."""
        return await self.__get(f"/v2/devices/{device_id}/skeds")

    async def action(self, device_id: str, action: Action) -> None:
        """Execute given action for a given device."""
        if action.name == Action.SET_STATE_BELIEF:
            path = f"/v2/devices/{device_id}/state"

            async def patch(session: ClientSession) -> None:
                async with session.patch(
                    f"http://{self._host}{path}",
                    **self._api_kwargs,
                    json=action.argument,
                ) as response:
                    response.raise_for_status()

            await self.__call(patch)
        else:
            path = f"/v2/devices/{device_id}/actions/{action.name}"

            async def put(session: ClientSession) -> None:
                async with session.put(
                    f"http://{self._host}{path}",
                    **self._api_kwargs,
                    json=action.argument,
                ) as response:
                    response.raise_for_status()

            await self.__call(put)

    async def supports_groups(self) -> Boolean:
        """Return 'True' if the Bond supports the Groups feature."""
        json = await self.__get("/v2/")
        return "groups" in json

    async def groups(self) -> List[str]:
        """Return the list of available group IDs reported by API."""
        json = await self.__get("/v2/groups")
        return [
            key for key in json if not key.startswith("_") and type(json[key]) is dict
        ]

    async def group(self, group_id: str) -> dict:
        """Return main group metadata reported by API."""
        return await self.__get(f"/v2/groups/{group_id}")

    async def group_properties(self, group_id: str) -> dict:
        """Return group properties reported by API."""
        return await self.__get(f"/v2/groups/{group_id}/properties")

    async def group_state(self, group_id: str) -> dict:
        """Return current group state reported by API."""
        return await self.__get(f"/v2/groups/{group_id}/state")

    async def group_skeds(self, group_id: str) -> dict:
        """Return current group schedules reported by API."""
        return await self.__get(f"/v2/groups/{group_id}/skeds")

    async def group_action(self, group_id: str, action: Action) -> None:
        """Execute given action for a given group."""
        if action.name == Action.SET_STATE_BELIEF:
            path = f"/v2/groups/{group_id}/state"

            async def patch(session: ClientSession) -> None:
                async with session.patch(
                    f"http://{self._host}{path}",
                    **self._api_kwargs,
                    json=action.argument,
                ) as response:
                    response.raise_for_status()

            await self.__call(patch)
        else:
            path = f"/v2/groups/{group_id}/actions/{action.name}"

            async def put(session: ClientSession) -> None:
                async with session.put(
                    f"http://{self._host}{path}",
                    **self._api_kwargs,
                    json=action.argument,
                ) as response:
                    response.raise_for_status()

            await self.__call(put)

    async def __get(self, path) -> dict:
        async def get(session: ClientSession) -> dict:
            async with session.get(
                f"http://{self._host}{path}", **self._api_kwargs
            ) as response:
                response.raise_for_status()
                return await response.json()

        return await self.__call(get)

    async def __call(self, handler: Callable[[ClientSession], Any]):
        if not self._session:
            async with ClientSession() as request_session:
                return await handler(request_session)
        else:
            try:
                return await handler(self._session)
            except (ClientOSError, ServerDisconnectedError):
                # bond has a short connection close time
                # so we need to retry if we idled for a bit
                return await handler(self._session)
