import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
import logging

logger = logging.getLogger("sentry-init")

def init_sentry():
    try:
        sentry_sdk.init(
            dsn="https://de6d172532d5846fb8004ce69225441b@o4509850316308480.ingest.us.sentry.io/4509850325221376",
            integrations=[FastApiIntegration()],
            send_default_pii=True,
            traces_sample_rate=0.5,
        )
        logger.info("✅ Sentry initialized successfully.")
    except Exception as e:
        logger.error(f"❌ Sentry initialization failed: {e}")

