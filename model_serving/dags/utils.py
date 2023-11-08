from pathlib import Path

import pendulum
from airflow.models import Variable
from docker.types import Mount


class AppConst:
    DOCKER_USER = Variable.get("DOCKER_USER", "longlam071")


class AppPath:
    MLOPS_CRASH_COURSE_CODE_DIR = Path(
        Variable.get("MLOPS_CRASH_COURSE_CODE_DIR")
    )
    MODEL_SERVING_DIR = MLOPS_CRASH_COURSE_CODE_DIR / "model_serving"
    FEATURE_REPO = MODEL_SERVING_DIR / "feature_repo"
    ARTIFACTS = MODEL_SERVING_DIR / "artifacts"
    DATA = MODEL_SERVING_DIR / "data"


class DefaultConfig:
    DEFAULT_DAG_ARGS = {
        "owner": "longlam071",
        "retries": 0,
        "retry_delay": pendulum.duration(seconds=20),
    }

    DEFAULT_DOCKER_OPERATOR_ARGS = {
        "image": f"{AppConst.DOCKER_USER}/model_serving:latest",
        "api_version": "auto",
        "auto_remove": True,
        "network_mode": "bridge",
        "docker_url": "tcp://docker-proxy:2375",
        "mounts": [
            # feature repo
            Mount(
                source="/d/Main/mlops-practice-course/model_serving/feature_repo",
                target="/model_serving/feature_repo",
                type="bind",
            ),
            # artifacts
            Mount(
                source="/d/Main/mlops-practice-course/model_serving/artifacts",
                target="/model_serving/artifacts",
                type="bind",
            ),
            # data
            Mount(
                source="/d/Main/mlops-practice-course/model_serving/data",
                target="/model_serving/data",
                type="bind",
            ),
        ],
    }
