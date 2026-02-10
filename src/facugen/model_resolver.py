from facugen.models import SUPPORTED_MODELS, ModelSpec


def resolve_model(model_name: str) -> ModelSpec:
    try:
        return SUPPORTED_MODELS[model_name]
    except KeyError:
        supported = ", ".join(sorted(SUPPORTED_MODELS.keys()))
        raise ValueError(
            f"Unsupported model '{model_name}'. Supported models: {supported}"
        )
