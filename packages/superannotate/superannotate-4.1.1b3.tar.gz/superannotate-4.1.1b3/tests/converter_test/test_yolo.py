from pathlib import Path

import superannotate as sa
from ..common import upload_project


def test_yolo_object_detection_web(tmpdir):
    project_name = "yolo_object_detection"

    input_dir = Path(
        'tests'
    ) / 'converter_test' / 'YOLO' / 'input' / 'toSuperAnnotate'
    out_dir = Path(tmpdir) / project_name
    sa.import_annotation(
        input_dir, out_dir, 'YOLO', '', 'Vector', 'object_detection'
    )

    description = 'yolo object detection'
    ptype = 'Vector'
    upload_project(out_dir, project_name, description, ptype)
