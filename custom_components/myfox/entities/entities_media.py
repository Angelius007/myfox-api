import logging
from typing import Any

from homeassistant.components.media_player import (MediaPlayerEntity, MediaClass, MediaType, MediaPlayerEntityFeature, MediaPlayerEnqueue)
from homeassistant.components.media_player.browse_media import BrowseMedia  # noqa: F401
from homeassistant.components import media_source

from .entity import MyFoxAbstractDeviceEntity
from ..devices import BaseDevice
from ..coordinator.myfox_coordinator import (MyFoxCoordinator)

_LOGGER = logging.getLogger(__name__)

# # ////////////////////////////////////////////////////////////////////////////
# # DEVICES
# # ////////////////////////////////////////////////////////////////////////////


class BaseMediaEntity(MediaPlayerEntity, MyFoxAbstractDeviceEntity):
    def __init__(self, coordinator: MyFoxCoordinator, device: BaseDevice, title: str, key: str):
        super().__init__(coordinator, device, title, key)

    async def async_browse_media(
        self, media_content_type: str | None = None, media_content_id: str | None = None
    ) -> BrowseMedia:
        """Implement the websocket media browsing helper."""
        browserMedias = None
        if media_content_type == MediaType.IMAGE or media_content_type == MediaType.VIDEO:
            coordinator: MyFoxCoordinator = self.coordinator
            medias = await coordinator.getMedia(self.idx)
            if media_content_type == MediaType.IMAGE :
                browserMedias = BrowseMedia("*", MediaClass.DIRECTORY, self.idx, MediaType.IMAGE, "Images-" + self.idx, False, False)
            elif media_content_type == MediaType.VIDEO :
                browserMedias = BrowseMedia("*", MediaClass.DIRECTORY, self.idx, MediaType.VIDEO, "Videos-" + self.idx, False, False)
            for media in medias:
                if "imageId" in media :
                    browserMedia = BrowseMedia("*", MediaClass.IMAGE, media["imageId"], MediaType.IMAGE, media["cameraLabel"], False, False)
                    browserMedias.children[browserMedias.children.count] = browserMedia
                elif "videoId" in media :
                    browserMedia = BrowseMedia("*", MediaClass.VIDEO, media["videoId"], MediaType.VIDEO, media["cameraLabel"], True, False)
                    browserMedias.children[browserMedias.children.count] = browserMedia
        # TODO : formater le retour en objet BrowseMedia
        return await media_source.async_browse_media(
            self.hass,
            media_content_id,
            content_filter=lambda item: item.media_content_type.startswith("video/"),
        )


class ImageMediaEntity(BaseMediaEntity):
    def __init__(self, coordinator: MyFoxCoordinator, device: BaseDevice, title: str, key: str):
        super().__init__(coordinator, device, title, key)
        self._attr_supported_features = MediaPlayerEntityFeature.BROWSE_MEDIA
        self._attr_media_content_type = MediaType.IMAGE


class VideoMediaEntity(BaseMediaEntity):
    def __init__(self, coordinator: MyFoxCoordinator, device: BaseDevice, title: str, key: str):
        super().__init__(coordinator, device, title, key)
        self._attr_supported_features = MediaPlayerEntityFeature.BROWSE_MEDIA | MediaPlayerEntityFeature.PLAY
        self._attr_media_content_type = MediaType.VIDEO

    async def async_play_media(
        self,
        media_type: str,
        media_id: str,
        enqueue: MediaPlayerEnqueue | None = None,
        announce: bool | None = None, **kwargs: Any
    ) -> None:
        """Play a piece of media."""
        coordinator: MyFoxCoordinator = self.coordinator
        await coordinator.playVideo(self.idx, int(media_id))
