from typing import Callable, Dict, List, TypeVar, Union, Any

from .domain import (
    CardEvent,
    CarryEvent,
    DataRecord,
    Dataset,
    Dimension,
    Event,
    EventDataset,
    EventType,
    Frame,
    Orientation,
    PassEvent,
    PassResult,
    PitchDimensions,
    ShotEvent,
    TrackingDataset,
    Transformer,
    Provider,
    build_coordinate_system,
    CodeDataset,
    Code,
    CoordinateSystem,
)


DatasetT = TypeVar("DatasetT")


def transform(
    dataset: Dataset,
    to_orientation=None,
    to_pitch_dimensions=None,
    to_coordinate_system: Union[CoordinateSystem, Provider] = None,
) -> Dataset:

    if to_pitch_dimensions and to_coordinate_system:
        raise ValueError(
            "You can't do both a PitchDimension and CoordinateSysetm on the same dataset transformation"
        )

    if to_orientation and isinstance(to_orientation, str):
        to_orientation = Orientation[to_orientation]

    if to_pitch_dimensions and (
        isinstance(to_pitch_dimensions, list)
        or isinstance(to_pitch_dimensions, tuple)
    ):
        to_pitch_dimensions = PitchDimensions(
            x_dim=Dimension(*to_pitch_dimensions[0]),
            y_dim=Dimension(*to_pitch_dimensions[1]),
        )
        return Transformer.transform_dataset(
            dataset=dataset,
            to_orientation=to_orientation,
            to_pitch_dimensions=to_pitch_dimensions,
        )

    if to_coordinate_system and isinstance(to_coordinate_system, Provider):
        to_coordinate_system = build_coordinate_system(
            provider=to_coordinate_system,
            length=dataset.metadata.coordinate_system.length,
            width=dataset.metadata.coordinate_system.width,
        )

    return Transformer.transform_dataset(
        dataset=dataset,
        to_orientation=to_orientation,
        to_coordinate_system=to_coordinate_system,
    )

