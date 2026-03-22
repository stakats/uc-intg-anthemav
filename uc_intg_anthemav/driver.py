"""
Anthem A/V integration driver for Unfolded Circle Remote.

:copyright: (c) 2025 by Meir Miyara.
:license: MPL-2.0, see LICENSE for more details.
"""

import logging

from ucapi_framework import BaseIntegrationDriver

from .config import AnthemDeviceConfig
from .device import AnthemDevice
from .media_player import AnthemMediaPlayer
from .remote import AnthemRemote
from .sensor import create_sensors
from .select import AnthemListeningModeSelect

_LOG = logging.getLogger(__name__)


def _create_all_entities(config: AnthemDeviceConfig, device: AnthemDevice) -> list:
    """Create all entities for all enabled zones."""
    entities = []

    for zone_config in config.zones:
        if not zone_config.enabled:
            continue

        entities.append(AnthemMediaPlayer(config, device, zone_config))
        entities.append(AnthemRemote(config, device, zone_config))
        entities.append(AnthemListeningModeSelect(config, device, zone_config))

        if zone_config.zone_number == 1:
            entities.extend(create_sensors(config, device))

    return entities


class AnthemDriver(BaseIntegrationDriver[AnthemDevice, AnthemDeviceConfig]):
    """Anthem A/V integration driver."""

    def __init__(self):
        super().__init__(
            device_class=AnthemDevice,
            entity_classes=[_create_all_entities],
            require_connection_before_registry=True,
        )
