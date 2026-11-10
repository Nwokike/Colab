"""About, version metadata, legal terms settings section.

DDGS/KTV's About shape (owner's review, 2026-11-10): nothing hardcoded per
platform — the Rate row points at the Play Store on phones/TV and at the
GitHub repo on desktop, the More-apps row opens the Play developer listing
on mobile and the kiri.ng showcase elsewhere, the update line is LIVE from
the update feed, and the Edition row only exists on the Play channel.
"""

from __future__ import annotations

import logging

import flet as ft

from core import constants, tokens
from core.channel import CHANNEL
from core.styles import glass_card, section_header

logger = logging.getLogger(__name__)


def _get_cli_version() -> str:
    try:
        from colab_cli.auto_update import get_app_version as _get_cli_ver

        return _get_cli_ver()
    except Exception:
        return "latest"


def _open_version_dialog(page: ft.Page, state):
    """Open the version dialog — changelog when up to date, update UI when
    a newer build was found. The dialog reads observable state itself."""
    from components.version_dialog import show_version_dialog

    show_version_dialog(page)


def _is_store_device(page) -> bool:
    """Phones/TV/iOS are the Play audience; desktop has no listing (DDGS)."""
    try:
        return page.platform in (
            ft.PagePlatform.ANDROID,
            ft.PagePlatform.IOS,
            ft.PagePlatform.ANDROID_TV,
        )
    except Exception:
        return False


def _row(icon, title: str, subtitle: str, on_click) -> ft.Container:
    """KTV/DDGS about row: icon + title/subtitle + open-in-new, whole row tappable."""
    return ft.Container(
        content=ft.Row(
            controls=[
                ft.Icon(icon, size=tokens.ICON_SM, color=ft.Colors.ON_SURFACE_VARIANT),
                ft.Column(
                    controls=[
                        ft.Text(title, size=tokens.FONT_SM, weight=ft.FontWeight.W_500),
                        ft.Text(
                            subtitle,
                            size=tokens.FONT_XS,
                            color=ft.Colors.ON_SURFACE_VARIANT,
                        ),
                    ],
                    spacing=0,
                    tight=True,
                    expand=True,
                ),
                ft.Icon(
                    ft.Icons.OPEN_IN_NEW_ROUNDED,
                    size=tokens.ICON_XS,
                    color=ft.Colors.ON_SURFACE_VARIANT,
                ),
            ],
            spacing=tokens.SPACE_SM,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=ft.Padding(6, 8, 6, 8),
        border_radius=tokens.RADIUS_MD,
        ink=True,
        on_click=on_click,
    )


def build_about_section(page: ft.Page, state, services) -> ft.Column:
    """App metadata, version info, contact/rate/more-apps, and terms links."""
    cli_version = _get_cli_version()
    store_device = _is_store_device(page)

    # The Rate and More-apps targets are platform-dependent, never hardcoded
    # to one store (DDGS's exact split).
    rate_url = constants.PLAY_STORE_URL if store_device else constants.GITHUB_REPO_URL
    rate_subtitle = "Rate us on Google Play" if store_device else "Star us on GitHub"
    more_apps_url = (
        constants.KIRI_APPS_PLAY_URL if store_device else constants.KIRI_APPS_URL
    )
    more_apps_subtitle = (
        "All our apps on Google Play"
        if store_device
        else "Sherlock, DDGS, ColabShell and more"
    )

    async def _launch(url: str):
        try:
            await ft.UrlLauncher().launch_url(url)
        except Exception:
            logger.exception("Suppressed exception")

    edition_row = (
        ft.Row(
            controls=[
                ft.Text("Edition", size=tokens.FONT_SM),
                ft.TextButton(
                    content=ft.Text(
                        "Google Play Edition · Full edition on GitHub",
                        size=tokens.FONT_SM,
                        weight=ft.FontWeight.W_600,
                        color=ft.Colors.PRIMARY,
                    ),
                    on_click=lambda e: page.run_task(
                        _launch, constants.GITHUB_REPO_URL
                    ),
                    style=ft.ButtonStyle(padding=ft.Padding(0, 0, 0, 0)),
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )
        if CHANNEL == "play"
        else None
    )

    update_available = bool(getattr(state, "update_available", False))

    return ft.Column(
        controls=[
            section_header("ABOUT"),
            glass_card(
                ft.Column(
                    controls=[
                        ft.Container(
                            content=ft.Image(
                                src="icon.png",
                                width=tokens.HERO_ICON_SIZE,
                                height=tokens.HERO_ICON_SIZE,
                                fit=ft.BoxFit.CONTAIN,
                            ),
                            alignment=ft.Alignment.CENTER,
                            margin=ft.Margin(0, tokens.SPACE_SM, 0, tokens.SPACE_XS),
                        ),
                        ft.Text(
                            "Cloud GPUs and Notebooks from your phone",
                            size=tokens.FONT_SM,
                            color=ft.Colors.ON_SURFACE_VARIANT,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        ft.Container(height=tokens.SPACE_SM),
                        # The version header: LIVE status line from the update
                        # feed (KTV/DDGS shape) — tap opens the changelog/update
                        # dialog.
                        ft.Container(
                            content=ft.Row(
                                controls=[
                                    ft.Column(
                                        controls=[
                                            ft.Text(
                                                constants.APP_NAME,
                                                size=tokens.FONT_MD,
                                                weight=ft.FontWeight.W_700,
                                            ),
                                            ft.Text(
                                                "Update available · tap to view"
                                                if update_available
                                                else (
                                                    f"Version {constants.APP_VERSION} · "
                                                    f"Flet {ft.__version__}"
                                                ),
                                                size=tokens.FONT_XS,
                                                color=(
                                                    ft.Colors.PRIMARY
                                                    if update_available
                                                    else ft.Colors.ON_SURFACE_VARIANT
                                                ),
                                            ),
                                        ],
                                        spacing=0,
                                        tight=True,
                                    ),
                                ],
                            ),
                            padding=ft.Padding(4, 8, 4, 8),
                            ink=True,
                            tooltip="Tap to view changelog",
                            on_click=lambda e: _open_version_dialog(page, state),
                        ),
                        ft.Row(
                            controls=[
                                ft.Text("Powered by", size=tokens.FONT_SM),
                                ft.Text(
                                    f"Google Colab (CLI v{cli_version})",
                                    size=tokens.FONT_SM,
                                    color=ft.Colors.ON_SURFACE_VARIANT,
                                    weight=ft.FontWeight.W_500,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        ft.Divider(
                            height=1,
                            color=ft.Colors.with_opacity(0.06, ft.Colors.ON_SURFACE),
                        ),
                        ft.Container(height=tokens.SPACE_XS),
                        *([edition_row] if edition_row is not None else []),
                        _row(
                            ft.Icons.MAIL_OUTLINE_ROUNDED,
                            "Contact developer",
                            constants.CONTACT_EMAIL,
                            lambda e: page.run_task(
                                _launch, f"mailto:{constants.CONTACT_EMAIL}"
                            ),
                        ),
                        _row(
                            ft.Icons.STAR_ROUNDED,
                            "Rate 5 stars",
                            rate_subtitle,
                            lambda e: page.run_task(_launch, rate_url),
                        ),
                        _row(
                            ft.Icons.APPS_ROUNDED,
                            "More apps from Kiri",
                            more_apps_subtitle,
                            lambda e: page.run_task(_launch, more_apps_url),
                        ),
                        ft.Divider(
                            height=1,
                            color=ft.Colors.with_opacity(0.06, ft.Colors.ON_SURFACE),
                        ),
                        ft.Row(
                            controls=[
                                ft.TextButton(
                                    "Privacy Policy",
                                    icon=ft.Icons.PRIVACY_TIP_ROUNDED,
                                    style=ft.ButtonStyle(color=ft.Colors.PRIMARY),
                                    on_click=lambda e: page.run_task(
                                        _launch, constants.PRIVACY_POLICY_URL
                                    ),
                                ),
                                ft.TextButton(
                                    "Terms of Service",
                                    icon=ft.Icons.GAVEL_ROUNDED,
                                    style=ft.ButtonStyle(color=ft.Colors.PRIMARY),
                                    on_click=lambda e: page.run_task(
                                        _launch, constants.TERMS_OF_SERVICE_URL
                                    ),
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                        ),
                        ft.Text(
                            "Disclaimer: Unofficial client application. Not affiliated with, authorized, sponsored, or endorsed by Google LLC.",
                            size=tokens.FONT_XXS,
                            color=ft.Colors.ON_SURFACE_VARIANT,
                            italic=True,
                            text_align=ft.TextAlign.CENTER,
                        ),
                    ],
                    spacing=tokens.SPACE_SM,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                margin=ft.Margin(
                    tokens.SPACE_LG, tokens.SPACE_XS, tokens.SPACE_LG, tokens.SPACE_XS
                ),
            ),
        ],
        spacing=0,
    )
