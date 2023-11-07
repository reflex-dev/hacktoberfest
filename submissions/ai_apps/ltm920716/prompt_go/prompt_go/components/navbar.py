import reflex as rx


def navbar():
    return rx.box(
        rx.hstack(
            rx.link(
                rx.box(
                    rx.image(src="/logo.png", width=50, height="auto"),
                    p="1",
                    border_radius="6",
                    bg="#F0F0F0",
                    mr="2"
                ),
                href="/"
            ),
            rx.heading("PromptGo", size="xl")
        ),
        width="100%",
        top="0",
        px="6",
        position="sticky",
        bg="white",
        h="100%",
        margin="10px auto"
    )
