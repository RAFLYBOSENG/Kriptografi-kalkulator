from datetime import datetime, timezone

from flask import Blueprint, Response, current_app, render_template, url_for
from ..services import history_service

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    return render_template("landing.html")


@main_bp.route("/kalkulator")
def kalkulator():
    return render_template("index.html")


@main_bp.route("/history")
def history():
    hist = history_service.load_history()
    return render_template("history.html", history=hist)


@main_bp.route("/robots.txt")
def robots_txt():
    site_url = current_app.config["SITE_URL"].rstrip("/")
    content = f"User-agent: *\nAllow: /\nSitemap: {site_url}/sitemap.xml\n"
    return Response(content, mimetype="text/plain")


@main_bp.route("/sitemap.xml")
def sitemap_xml():
    site_url = current_app.config["SITE_URL"].rstrip("/")
    lastmod = datetime.now(timezone.utc).date().isoformat()
    urls = [
        url_for("main.index"),
        url_for("main.kalkulator"),
        url_for("main.history"),
    ]
    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for path in urls:
        parts.extend(
            [
                "  <url>",
                f"    <loc>{site_url}{path}</loc>",
                f"    <lastmod>{lastmod}</lastmod>",
                "    <changefreq>weekly</changefreq>",
                "    <priority>0.8</priority>",
                "  </url>",
            ]
        )
    parts.append("</urlset>")
    return Response("\n".join(parts), mimetype="application/xml")
