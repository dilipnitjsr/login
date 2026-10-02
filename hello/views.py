'''
Web-based Kite Connect login callback.

Secrets are loaded from environment variables. Do not hard-code API keys,
database passwords, access tokens, or bot credentials in this module.
'''

import logging
import os

from django.http import HttpResponse
from django.shortcuts import render
from django.utils.html import format_html
from kiteconnect import KiteConnect
import psycopg2
import telegram

logger = logging.getLogger(__name__)


def _required_env(name):
    value = os.environ.get(name)
    if not value:
        raise RuntimeError("Required environment variable {} is not set".format(name))
    return value


def _kite_client(api_key=None):
    return KiteConnect(api_key=api_key or _required_env("KITE_API_KEY"))


def _kite_login_url():
    return _kite_client().login_url()


def sendBot(message, token=None, contact=None):
    """Send an optional Telegram login notification."""
    token = token or os.environ.get("TELEGRAM_BOT_TOKEN")
    contact = contact or os.environ.get("TELEGRAM_CHAT_ID")

    if not token or not contact:
        logger.info("Telegram notification skipped: credentials are not configured")
        return

    try:
        bot = telegram.Bot(token)
        bot.send_message(chat_id=contact, text=message)
    except Exception:
        logger.exception("Unable to send Telegram login notification")


def kConnect(user_id, access_token, api_key=None):
    """Return a Kite client authenticated with the supplied access token."""
    del user_id  # retained for backwards-compatible function signature
    kite = _kite_client(api_key=api_key)
    kite.set_access_token(access_token)
    return kite


def opendb():
    """Open the database used to store the current Kite access token."""
    return psycopg2.connect(
        database=_required_env("DB_NAME"),
        user=_required_env("DB_USER"),
        password=_required_env("DB_PASSWORD"),
        host=_required_env("DB_HOST"),
        port=int(os.environ.get("DB_PORT", "5432")),
    )


def sendsql(kiteuser):
    """Persist the current Kite access token for the authenticated user."""
    conn = None
    try:
        conn = opendb()
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE userKite SET token = %s WHERE id = %s",
                (kiteuser["access_token"], kiteuser["user_id"]),
            )
        conn.commit()
        logger.info("Updated Kite access token for user_id=%s", kiteuser["user_id"])
        return True
    except psycopg2.DatabaseError:
        if conn:
            conn.rollback()
        logger.exception("Unable to update Kite access token")
        return False
    finally:
        if conn:
            conn.close()


def index(request):
    login_url = None
    try:
        login_url = _kite_login_url()
    except RuntimeError:
        logger.error("Kite login is unavailable because server credentials are missing")

    if request.method == "GET":
        request_token = request.GET.get("request_token")
        status = request.GET.get("status")

        # Never log the request token itself.
        logger.info(
            "Kite callback received: status=%s request_token_present=%s",
            status,
            bool(request_token),
        )

        if status == "success":
            if not request_token:
                return HttpResponse("Missing request_token", status=400)

            try:
                kite = _kite_client()
                kiteuser = kite.generate_session(
                    request_token=request_token,
                    api_secret=_required_env("KITE_API_SECRET"),
                )

                if not sendsql(kiteuser):
                    raise RuntimeError("Access token could not be persisted")

                user_id = kiteuser.get("user_id", "")
                user_name = kiteuser.get("user_name", "User")
                logger.info("Kite login successful for user_id=%s", user_id)
                sendBot("{} : LOGIN : {}".format(user_name, user_id))

                return HttpResponse(
                    format_html(
                        "<html><body><br><br><h1><center>"
                        "Welcome to DoD Automation!<hr><br><br>{} : Login Success"
                        "</center><br></h1><h4><a href='{}'>Another Login</a>"
                        "</h4></body></html>",
                        user_name,
                        login_url or "/",
                    )
                )
            except Exception:
                # Do not expose provider/database exception details or tokens to the browser.
                logger.exception("Kite login failed")
                return HttpResponse(
                    format_html(
                        "<html><body><br><br><h1><center>"
                        "<a href='{}'>Please Re-login</a>"
                        "</center></h1></body></html>",
                        login_url or "/",
                    ),
                    status=401,
                )

    return render(request, "index.html", {"kite_login_url": login_url})


def db(request):
    return render(request, "index.html", {"kite_login_url": None})
