from datetime import datetime
import time
from typing import Callable, Type, Any


global_registry: dict[str, Type[Any]] = {}

def message(func: Callable) -> Callable:
    def wrapper(self, *args, **kwargs):
        print(f"[Message] → Appel de {func.__name__}()")
        result = func(self, *args, **kwargs)
        print(f"[Message] ← Fin de {func.__name__}() → {result}")
        return result
    return wrapper

class AddPerformanceTracking:
    def __call__(self, cls: Type[Any]) -> Type[Any]:
        if hasattr(cls, "evacuer"):
            original = cls.evacuer
            def tracked(self, *args, **kwargs):
                start_time = datetime.now()
                start = time.time()
                print(f"[Performance]  Début {cls.__name__}.evacuer à {start_time.strftime('%H:%M:%S')}")
                result = original(self, *args, **kwargs)
                end = time.time()
                end_time = datetime.now()
                # Inject a time window into the instance
                self.time_window = (start_time, end_time)
                print(f"[Performance]  Fin {cls.__name__}.evacuer ({end - start:.3f}s)")
                return result
            cls.evacuer = tracked
        return cls

class AutoConfigurationValidation:
    def __call__(self, cls: Type[Any]) -> Type[Any]:
        original_init = cls.__init__
        def new_init(self, *args, **kwargs):
            original_init(self, *args, **kwargs)
            if hasattr(cls, 'required_fields'):
                missing = [field for field in cls.required_fields if not hasattr(self, field)]
                if missing:
                    missing_str = ', '.join(missing)
                    raise ValueError(f"[Validation] {cls.__name__} manque le champ requis : {missing_str}")
        cls.__init__ = new_init
        return cls

class RegisterInGlobalRegistry:
    registry: dict[str, Type[Any]] = global_registry
    def __call__(self, cls: Type[Any]) -> Type[Any]:
        self.registry[cls.__name__] = cls
        print(f"[Registry] Classe enregistrée : {cls.__name__}")
        return cls

class AddCircuitBreaker:
    def __call__(self, cls: Type[Any]) -> Type[Any]:
        if hasattr(cls, "evacuer"):
            original = cls.evacuer
            def safe(self, *args, **kwargs):
                try:
                    return original(self, *args, **kwargs)
                except Exception as e:
                    print(f"[CircuitBreaker] Erreur interceptée dans {cls.__name__} : {e}")
                    return None
            cls.evacuer = safe
        return cls