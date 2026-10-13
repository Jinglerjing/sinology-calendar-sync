import os
import requests
from datetime import date, timedelta
from lunar_python import Solar
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

BASE_URL = "https://sinologystudio.com/rhythm"
WP_API_URL = "https://sinologystudio.com/wp-json/wp/v2/posts"

SOLAR_TERMS_DATA = {
    "立春": {"translation": "Start of Spring", "slug": "start-of-spring", "summary": "Plowing begins; ancient rituals welcome the Spring God.", "rituals": "Spring rolls (春饼), biting the spring (咬春) radishes."},
    "雨水": {"translation": "Rain Water", "slug": "rain-water", "summary": "Gentle rainfall nourishes winter wheat as nature awakens.", "rituals": "Nutritious soups, lotus seed porridge, visiting in-laws."},
    "惊蛰": {"translation": "Awakening of Insects", "slug": "awakening-of-insects", "summary": "Spring thunder wakes hibernating life; pest prevention begins.", "rituals": "Eating pears (梨) to nourish lungs, 'villain hitting' rituals."},
    "春分": {"translation": "Spring Equinox", "slug": "spring-equinox", "summary": "Equal day and night. Peak season for spring planting.", "rituals": "Standing eggs on end (立蛋), spring greens (春菜), flying kites."},
    "清明": {"translation": "Clear and Bright", "slug": "clear-and-bright", "summary": "Time for honoring ancestors, spring outings, and planting.", "rituals": "Tomb sweeping (祭祖), Qingtuan (青团), flying kites with lanterns."},
    "谷雨": {"translation": "Grain Rain", "slug": "grain-rain", "summary": "Warm rains accelerate crop growth; crucial tea harvest period.", "rituals": "Drinking Guyu spring tea (谷雨茶), fresh toon leaves (香椿)."},
    "立夏": {"translation": "Start of Summer", "slug": "start-of-summer", "summary": "Summer crops enter rapid growth as warm energy rises.", "rituals": "Lixia eggs (立夏蛋), fresh broad beans, cherries, bamboo shoots."},
    "小满": {"translation": "Grain Buds", "slug": "grain-buds", "summary": "Grains begin to fill and plump up across agricultural fields.", "rituals": "Wild bitter herbs (苦菜), wheat pastries, silkworm honors."},
    "芒种": {"translation": "Grain in Ear", "slug": "grain-in-ear", "summary": "Busiest farming season: harvesting wheat while planting rice.", "rituals": "Green plums, plum wine, farewell rituals for Flora."},
    "夏至": {"translation": "Summer Solstice", "slug": "summer-solstice", "summary": "The longest day of the year; peak solar abundance.", "rituals": "Summer Solstice noodles (夏至面), lychees, herbal cooling teas."},
    "小暑": {"translation": "Minor Heat", "slug": "minor-heat", "summary": "Summer heat intensifies; mid-day rest and cooling become essential.", "rituals": "Fresh lotus root, mung bean soup, airing books in the sun."},
    "大暑": {"translation": "Major Heat", "slug": "major-heat", "summary": "The hottest period of summer; peak growth for rice and corn.", "rituals": "Grass jelly (仙草), mutton soup, herbal cooling teas."},
    "立秋": {"translation": "Start of Autumn", "slug": "start-of-autumn", "summary": "Autumn begins as summer grains ripen and harvest approaches.", "rituals": "Fleshing out in autumn (贴秋膘), dumplings, drying crops (晒秋)."},
    "处暑": {"translation": "End of Heat", "slug": "end-of-heat", "summary": "Summer heat recedes; cool breeze and autumn harvest begin.", "rituals": "Eating duck, longans, floating river lanterns."},
    "白露": {"translation": "White Dew", "slug": "white-dew", "summary": "Temperatures drop sharply at night, forming dew on leaves.", "rituals": "Bailu tea (白露茶), longans, sweet potato porridge."},
    "秋分": {"translation": "Autumnal Equinox", "slug": "autumnal-equinox", "summary": "Equal day and night. Autumn harvest in full swing.", "rituals": "Hairy crab (大闸蟹), autumn pears, osmanthus wine."},
    "寒露": {"translation": "Cold Dew", "slug": "cold-dew", "summary": "Dew turns cold and near-freezing; earth turns inward.", "rituals": "Sesame, hawthorn berries, chrysanthemums, mountain hikes."},
    "霜降": {"translation": "Frost's Descent", "slug": "frosts-descent", "summary": "Final autumn term; morning dew transforms into light frost.", "rituals": "Persimmons (柿子), chestnuts, warm tonic stews."},
    "立冬": {"translation": "Start of Winter", "slug": "start-of-winter", "summary": "Winter arrives; crops are stored and nature rests.", "rituals": "Winter dumplings (饺子), mutton soups, ancestor offerings."},
    "小雪": {"translation": "Minor Snow", "slug": "minor-snow", "summary": "Cold air deepens; light snow begin in northern regions.", "rituals": "Cured meats (腊肉), preserved sausages, rice cakes."},
    "大雪": {"translation": "Major Snow", "slug": "major-snow", "summary": "Heavy snow covers the land, insulating winter crops.", "rituals": "Lamb hotpot, red bean porridge, winter citrus fruits."},
    "冬至": {"translation": "Winter Solstice", "slug": "winter-solstice", "summary": "The shortest day of the year; yang energy slowly begins to return.", "rituals": "Tangyuan (汤圆), dumplings, counting Nine-Nine winter days."},
    "小寒": {"translation": "Minor Cold", "slug": "minor-cold", "summary": "Deep winter freeze sets in; preparing for Spring Festival.", "rituals": "Laba porridge, glutinous rice with cured meats, mutton."},
    "大寒": {"translation": "Major Cold", "slug": "major-cold", "summary": "The final solar term; extreme cold before spring renewal.", "rituals": "Nian gao (年糕), ginseng chicken soup, home cleaning."}
}

FESTIVALS_DATA = {
    "春节": {"translation": "Chinese New Year", "slug": "spring-festival", "summary": "The most significant traditional holiday celebrating family reunion.", "rituals": "Dumplings, Nian Gao, red envelopes (压岁钱), dragon dances."},
    "元宵节": {"translation": "Lantern Festival", "slug": "lantern-festival", "summary": "Marks the final day of traditional Chinese New Year celebrations.", "rituals": "Tangyuan (汤圆), lantern riddle guessing, lion dances."},
    "端午节": {"translation": "Dragon Boat Festival", "slug": "dragon-boat-festival", "summary": "A summer solstice festival honoring poet Qu Yuan.", "rituals": "Zongzi (粽子), dragon boat races, hanging mugwort."},
    "七夕节": {"translation": "Qixi Festival / Chinese Valentine's", "slug": "qixi-festival", "summary": "Celebrates the celestial reunion of the Weaver Girl and Cowherd.", "rituals": "Qiaoguo (巧果) pastries, stargazing, needlework tests."},
    "中元节": {"translation": "Ghost Festival", "slug": "ghost-festival", "summary": "A day devoted to honoring ancestors and guiding departed spirits.", "rituals": "Floating water lanterns, ancestral veneration, burning incense."},
    "中秋节": {"translation": "Mid-Autumn Festival", "slug": "mid-autumn-festival", "summary": "A harvest festival centered on lunar appreciation and family.", "rituals": "Mooncakes (月饼), moon gazing, osmanthus wine."},
    "重阳节": {"translation": "Double Ninth Festival", "slug": "double-ninth-festival", "summary": "An autumn day dedicated to health, longevity, and mountain climbing.", "rituals": "Chongyang cake (重阳糕), chrysanthemum tea, mountain walks."},
    "腊八节": {"translation": "Laba Festival", "slug": "laba-festival", "summary": "A traditional winter day marking the prelude to Chinese New Year.", "rituals": "Laba porridge (腊八粥), pickling Laba green garlic."}
}

def fetch_wp_excerpts():
    """Fetches live excerpts from WordPress REST API to override default summaries."""
    excerpts = {}
    try:
        response = requests.get(f"{WP_API_URL}?per_page=100", timeout=10)
        if response.status_code == 200:
            posts = response.json()
            for post in posts:
                slug = post.get("slug")
                excerpt = post.get("excerpt", {}).get("rendered", "")
                # Clean HTML tags from excerpt text
                clean_excerpt = requests.utils.unquote(excerpt).replace("<p>", "").replace("</p>", "").strip()
                if slug and clean_excerpt:
                    excerpts[slug] = clean_excerpt
    except Exception as e:
        print(f"⚠️ WordPress API fetch skipped (using default summaries): {e}")
    return excerpts

def get_calendar_service():
    creds = Credentials(
        token=None,
        refresh_token=os.environ["GOOGLE_REFRESH_TOKEN"],
        client_id=os.environ["GOOGLE_CLIENT_ID"],
        client_secret=os.environ["GOOGLE_CLIENT_SECRET"],
        token_uri="https://oauth2.googleapis.com/token",
        scopes=["https://www.googleapis.com/auth/calendar"]
    )
    return build("calendar", "v3", credentials=creds)

def fetch_existing_events(service, calendar_id):
    """Smart Diffing: Fetches existing calendar events to prevent unnecessary API writes."""
    existing = {}
    page_token = None
    while True:
        events_result = service.events().list(calendarId=calendar_id, pageToken=page_token).execute()
        for item in events_result.get('items', []):
            existing[item['id']] = {
                "summary": item.get("summary"),
                "description": item.get("description"),
                "start": item.get("start", {}).get("date"),
                "end": item.get("end", {}).get("date")
            }
        page_token = events_result.get('nextPageToken')
        if not page_token:
            break
    return existing

def main():
    service = get_calendar_service()
    calendar_id = os.environ["CALENDAR_ID"]
    
    wp_excerpts = fetch_wp_excerpts()
    existing_events = fetch_existing_events(service, calendar_id)
    
    skipped_count = 0
    updated_count = 0

    for year in range(2026, 2031):
        start_date = date(year, 1, 1)
        end_date = date(year, 12, 31)
        current_ordinal = start_date.toordinal()
        added_festivals_this_year = set()

        while current_ordinal <= end_date.toordinal():
            d = date.fromordinal(current_ordinal)
            next_day = d + timedelta(days=1)
            solar = Solar.fromYmd(d.year, d.month, d.day)
            lunar = solar.getLunar()

            # 1. Solar Terms
            jieqi = lunar.getJieQi()
            if jieqi in SOLAR_TERMS_DATA:
                info = SOLAR_TERMS_DATA[jieqi]
                slug = info['slug']
                summary_text = wp_excerpts.get(slug, info['summary'])
                
                uid = f"solar-term-{year}-{slug}@sinologystudio.com".replace("@", "-at-").replace(".", "-dot-")
                desc = f"{info['translation']} · {jieqi}\n\n{summary_text}\n\n🌿 Seasonal Rituals: {info['rituals']}\n\n📖 Read Full Seasonal Guide & Printable Postcard:\n{BASE_URL}/{slug}/"
                
                event_body = {
                    "id": uid,
                    "summary": f"{info['translation']} ({jieqi})",
                    "description": desc,
                    "start": {"date": d.isoformat()},
                    "end": {"date": next_day.isoformat()}
                }

                if is_changed(existing_events.get(uid), event_body):
                    service.events().import_(calendarId=calendar_id, body=event_body).execute()
                    updated_count += 1
                else:
                    skipped_count += 1

            # 2. Traditional Festivals
            festivals = lunar.getFestivals()
            for fest in festivals:
                if fest in FESTIVALS_DATA and fest not in added_festivals_this_year:
                    info = FESTIVALS_DATA[fest]
                    slug = info['slug']
                    summary_text = wp_excerpts.get(slug, info['summary'])
                    
                    uid = f"festival-{year}-{slug}@sinologystudio.com".replace("@", "-at-").replace(".", "-dot-")
                    desc = f"{info['translation']} · {fest}\n\n{summary_text}\n\n🧧 Traditions & Foods: {info['rituals']}\n\n📖 Read Cultural Guide:\n{BASE_URL}/{slug}/"
                    
                    event_body = {
                        "id": uid,
                        "summary": f"Festival: {info['translation']} ({fest})",
                        "description": desc,
                        "start": {"date": d.isoformat()},
                        "end": {"date": next_day.isoformat()}
                    }

                    if is_changed(existing_events.get(uid), event_body):
                        service.events().import_(calendarId=calendar_id, body=event_body).execute()
                        updated_count += 1
                    else:
                        skipped_count += 1

                    added_festivals_this_year.add(fest)

            current_ordinal += 1

    print(f"✨ Sync Complete! Skipped (unchanged): {skipped_count} | Updated/Created: {updated_count}")

def is_changed(existing, target):
    """Returns True if the event needs to be updated in Google Calendar."""
    if not existing:
        return True
    return (
        existing["summary"] != target["summary"] or
        existing["description"] != target["description"] or
        existing["start"] != target["start"]["date"] or
        existing["end"] != target["end"]["date"]
    )

if __name__ == "__main__":
    main()
