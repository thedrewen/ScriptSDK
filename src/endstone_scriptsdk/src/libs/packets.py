from bedrock_protocol import (
    DataItemEntry,
    DataItemBytePayload,
    DataItemShortPayload,
    DataItemIntPayload,
    DataItemFloatPayload,
    DataItemStringPayload,
    DataItemCompoundTagPayload,
    DataItemPosPayload,
    DataItemInt64Payload,
    DataItemVec3Payload,
    SynchedActorData,
    PropertySyncData,
    SetActorDataPacket as _NativeSetActorDataPacket,
    encode,
)

_PAYLOAD_TYPES = {
    0: DataItemBytePayload,     # Byte
    1: DataItemShortPayload,    # Short
    2: DataItemIntPayload,      # VarInt
    3: DataItemFloatPayload,    # Float
    4: DataItemStringPayload,   # String
    5: DataItemCompoundTagPayload,  # Compound tag
    6: DataItemPosPayload,      # Block pos (ints)
    7: DataItemInt64Payload,    # Int64
    8: DataItemVec3Payload,     # Vec3 (floats)
}


class SetActorDataPacket:
    def __init__(self, targetRuntimeId: int = 0, actorData: list = [], intProperties: list = [], floatProperties: list = [], tick: int = 0) -> None:
        self.targetRuntimeId = targetRuntimeId
        self.actorData = actorData
        self.intProperties = intProperties
        self.floatProperties = []
        self.tick = tick

    def _build_entry(self, item: dict) -> DataItemEntry:
        payload_cls = _PAYLOAD_TYPES.get(item["type"])
        if payload_cls is None:
            raise ValueError(f"Unsupported actor data type {item['type']!r}")
        return DataItemEntry(id=item["id"], payload=payload_cls(value=item["value"]))

    def serialize(self) -> bytes:
        packet = _NativeSetActorDataPacket(
            id=int(self.targetRuntimeId),
            packed_items=SynchedActorData.CopyableDataList(
                data=[self._build_entry(item) for item in self.actorData]
            ),
            synched_properties=PropertySyncData(
                int_entries=[
                    PropertySyncData.PropertySyncIntEntry(property_index=prop["index"], data=prop["value"])
                    for prop in self.intProperties
                ],
                float_entries=[
                    PropertySyncData.PropertySyncFloatEntry(property_index=prop["index"], data=prop["value"])
                    for prop in self.floatProperties
                ],
            ),
            tick=int(self.tick),
        )
        return encode(packet)
