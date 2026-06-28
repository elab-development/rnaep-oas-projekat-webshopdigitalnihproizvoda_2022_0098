import time
from enum import Enum
from typing import Callable
import httpx

class CircuitState(Enum):
    CLOSED = "closed"       #normalan rad
    OPEN = "open"           #nedostupan servis, odbija zahteve
    HALF_OPEN = "half_open" #testira da li je servis oporavio

class CircuitBreaker:
    def __init__(self, failure_threshold: int = 3, recovery_timeout: int = 30):
        self.failure_threshold = failure_threshold  #broj gresaka pre otvaranja
        self.recovery_timeout = recovery_timeout    #sekundi pre pokusaja oporavka
        self.failure_count = 0
        self.last_failure_time = None
        self.state = CircuitState.CLOSED

    def _should_attempt_reset(self) -> bool:
        return (
            self.last_failure_time and
            time.time() - self.last_failure_time >= self.recovery_timeout
        )

    def call_allowed(self) -> bool:
        if self.state == CircuitState.CLOSED:
            return True
        if self.state == CircuitState.OPEN:
            if self._should_attempt_reset():
                self.state = CircuitState.HALF_OPEN
                return True
            return False
        return True  # HALF_OPEN

    def record_success(self):
        self.failure_count = 0
        self.state = CircuitState.CLOSED

    def record_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN

    def get_status(self) -> dict:
        return {
            "state": self.state.value,
            "failure_count": self.failure_count,
            "failure_threshold": self.failure_threshold
        }

#instanca Circuit Breaker za svaki mikroservis
circuit_breakers = {
    "user-service": CircuitBreaker(),
    "product-service": CircuitBreaker(),
    "order-service": CircuitBreaker(),
    "notification-service": CircuitBreaker()
}

async def protected_request(service_name: str, method: str, url: str, **kwargs):
    """
    Izvršava HTTP zahtev ka mikroservisu uz Circuit Breaker zaštitu.
    Ako je Circuit Breaker otvoren, odmah vraća fallback odgovor.
    """
    cb = circuit_breakers[service_name]

    if not cb.call_allowed():
        raise httpx.HTTPError(
            f"Circuit Breaker OPEN: {service_name} is unavailable. "
            f"Try again in {cb.recovery_timeout} seconds."
        )

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await getattr(client, method)(url, **kwargs)
            response.raise_for_status()
            cb.record_success()
            return response
    except (httpx.HTTPError, httpx.TimeoutException) as e:
        cb.record_failure()
        raise