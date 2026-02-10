from facugen.core import SUPPORTED_MODELS, ModelSpec


def resolve_model(model_name: str) -> ModelSpec:
    if model_name in SUPPORTED_MODELS:
        return SUPPORTED_MODELS[model_name]
    
    # Fallback: if it's not a known model, assume it's an Ollama model 
    # This allows users to use any local model they have pulled.
    return ModelSpec(provider="ollama", model=model_name)
