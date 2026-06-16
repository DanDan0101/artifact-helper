from pathlib import Path

import imageio.v3 as iio

from artifact_helper.preprocessing import n_frames, iter_frames


def test_n_frames() -> None:
    for file_path in Path("./samples").glob("*.mkv"):
        frames = 0
        for _ in iter_frames(file_path):
            frames += 1
        assert frames == n_frames(
            file_path
        ), f"Expected {n_frames(file_path)} frames, but got {frames} for {file_path}"
