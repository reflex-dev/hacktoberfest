import reflex as rx


class DigitspanConfig(rx.Config):
    pass


config = DigitspanConfig(
    app_name="digit_span",
    telemetry_enabled=False,
    deploy_url="https://memory-span.vercel.app/",
)
