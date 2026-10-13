from datetime import date, timedelta
from lunar_python import Solar
from icalendar import Calendar, Event
import os

# Base URL for Sinology Studio web guides
BASE_URL = "https://sinologystudio.com/rhythm"

SOLAR_TERMS_DATA = {
    "立春": {
        "en_title": "Lìchūn",
        "translation": "Start of Spring",
        "slug": "start-of-spring",
        "summary_text": "Plowing begins; ancient rituals welcome the Spring God.",
        "rituals": "Spring rolls (春饼), biting the spring (咬春) radishes."
    },
    "雨水": {
        "en_title": "Yǔshuǐ",
        "translation": "Rain Water",
        "slug": "rain-water",
        "summary_text": "Gentle rainfall nourishes winter wheat as nature awakens.",
        "rituals": "Nutritious soups, lotus seed porridge, visiting in-laws."
    },
    "惊蛰": {
        "en_title": "Jīngzhé",
        "translation": "Awakening of Insects",
        "slug": "awakening-of-insects",
        "summary_text": "Spring thunder wakes hibernating life; pest prevention begins.",
        "rituals": "Eating pears (梨) to nourish lungs, 'villain hitting' rituals."
    },
    "春分": {
        "en_title": "Chūnfēn",
        "translation": "Spring Equinox",
        "slug": "spring-equinox",
        "summary_text": "Equal day and night. Peak season for spring planting.",
        "rituals": "Standing eggs on end (立蛋), spring greens (春菜), flying kites."
    },
    "清明": {
        "en_title": "Qīngmíng",
        "translation": "Clear and Bright",
        "slug": "clear-and-bright",
        "summary_text": "Time for honoring ancestors, spring outings, and planting.",
        "rituals": "Tomb sweeping (祭祖), Qingtuan (青团), flying kites with lanterns."
    },
    "谷雨": {
        "en_title": "Gǔyǔ",
        "translation": "Grain Rain",
        "slug": "grain-rain",
        "summary_text": "Warm rains accelerate crop growth; crucial tea harvest period.",
        "rituals": "Drinking Guyu spring tea (谷雨茶), fresh toon leaves (香椿)."
    },
    "立夏": {
        "en_title": "Lìxià",
        "translation": "Start of Summer",
        "slug": "start-of-summer",
        "summary_text": "Summer crops enter rapid growth as warm energy rises.",
        "rituals": "Lixia eggs (立夏蛋), fresh broad beans, cherries, bamboo shoots."
    },
    "小满": {
        "en_title": "Xiǎomǎn",
        "translation": "Grain Buds",
        "slug": "grain-buds",
        "summary_text": "Grains begin to fill and plump up across agricultural fields.",
        "rituals": "Wild bitter herbs (苦菜), wheat pastries, silkworm honors."
    },
    "芒种": {
        "en_title": "Mángzhòng",
        "translation": "Grain in Ear",
        "slug": "grain-in-ear",
        "summary_text": "Busiest farming season: harvesting wheat while planting rice.",
        "rituals": "Green plums, plum wine, farewell rituals for Flora."
    },
    "夏至": {
        "en_title": "Xiàzhì",
        "translation": "Summer Solstice",
        "slug": "summer-solstice",
        "summary_text": "The longest day of the year; peak solar abundance.",
        "rituals": "Summer Solstice noodles (夏至面), lychees, herbal cooling teas."
    },
    "小暑": {
        "en_title": "Xiǎoshǔ",
        "translation": "Minor Heat",
        "slug": "minor-heat",
        "summary_text": "Summer heat intensifies; mid-day rest and cooling become essential.",
        "rituals": "Fresh lotus root, mung bean soup, airing books in the sun."
    },
    "大暑": {
        "en_title": "Dàshǔ",
        "translation": "Major Heat",
        "slug": "major-heat",
        "summary_text": "The hottest period of summer; peak growth for rice and corn.",
        "rituals": "Grass jelly (仙草), mutton soup, herbal cooling teas."
    },
    "立秋": {
        "en_title": "Lìqiū",
        "translation": "Start of Autumn",
        "slug": "start-of-autumn",
        "summary_text": "Autumn begins as summer grains ripen and harvest approaches.",
        "rituals": "Fleshing out in autumn (贴秋膘), dumplings, drying crops (晒秋)."
    },
    "处暑": {
        "en_title": "Chùshǔ",
        "translation": "End of Heat",
        "slug": "end-of-heat",
        "summary_text": "Summer heat recedes; cool breeze and autumn harvest begin.",
        "rituals": "Eating duck, longans, floating river lanterns."
    },
    "白露": {
        "en_title": "Báilù",
        "translation": "White Dew",
        "slug": "white-dew",
        "summary_text": "Temperatures drop sharply at night, forming dew on leaves.",
        "rituals": "Bailu tea (白露茶), longans, sweet potato porridge."
    },
    "秋分": {
        "en_title": "Qiūfēn",
        "translation": "Autumnal Equinox",
        "slug": "autumnal-equinox",
        "summary_text": "Equal day and night. Autumn harvest in full swing.",
        "rituals": "Hairy crab (大闸蟹), autumn pears, osmanthus wine."
    },
    "寒露": {
        "en_title": "Hánlù",
        "translation": "Cold Dew",
        "slug": "cold-dew",
        "summary_text": "Dew turns cold and near-freezing; earth turns inward.",
        "rituals": "Sesame, hawthorn berries, chrysanthemums, mountain hikes."
    },
    "霜降": {
        "en_title": "Shuāngjiàng",
        "translation": "Frost's Descent",
        "slug": "frosts-descent",
        "summary_text": "Final autumn term; morning dew transforms into light frost.",
        "rituals": "Persimmons (柿子), chestnuts, warm tonic stews."
    },
    "立冬": {
        "en_title": "Lìdōng",
        "translation": "Start of Winter",
        "slug": "start-of-winter",
        "summary_text": "Winter arrives; crops are stored and nature rests.",
        "rituals": "Winter dumplings (饺子), mutton soups, ancestor offerings."
    },
    "小雪": {
        "en_title": "Xiǎoxuě",
        "translation": "Minor Snow",
        "slug": "minor-snow",
        "summary_text": "Cold air deepens; light snow begin in northern regions.",
        "rituals": "Cured meats (腊肉), preserved sausages, rice cakes."
    },
    "大雪": {
        "en_title": "Dàxuě",
        "translation": "Major Snow",
        "slug": "major-snow",
        "summary_text": "Heavy snow covers the land, insulating winter crops.",
        "rituals": "Lamb hotpot, red bean porridge, winter citrus fruits."
    },
    "冬至": {
        "en_title": "Dōngzhì",
        "translation": "Winter Solstice",
        "slug": "winter-solstice",
        "summary_text": "The shortest day of the year; yang energy slowly begins to return.",
        "rituals": "Tangyuan (汤圆), dumplings, counting Nine-Nine winter days."
    },
    "小寒": {
        "en_title": "Xiǎohán",
        "translation": "Minor Cold",
        "slug": "minor-cold",
        "summary_text": "Deep winter freeze sets in; preparing for Spring Festival.",
        "rituals": "Laba porridge, glutinous rice with cured meats, mutton."
    },
    "大寒": {
        "en_title": "Dàhán",
        "translation": "Major Cold",
        "slug": "major-cold",
        "summary_text": "The final solar term; extreme cold before spring renewal.",
        "rituals": "Nian gao (年糕), ginseng chicken soup, home cleaning."
    }
}

FESTIVALS_DATA = {
    "春节": {
        "en_title": "Spring Festival",
        "translation": "Chinese New Year",
        "slug": "spring-festival",
        "summary_text": "The most significant traditional holiday celebrating family reunion and spring renewal.",
        "rituals": "Dumplings, Nian Gao, red envelopes (压岁钱), dragon dances."
    },
    "元宵节": {
        "en_title": "Yuánxiāo Jié",
        "translation": "Lantern Festival",
        "slug": "lantern-festival",
        "summary_text": "Marks the final day of traditional Chinese New Year celebrations under the full moon.",
        "rituals": "Tangyuan (汤圆), lantern riddle guessing, lion dances."
    },
    "端午节": {
        "en_title": "Duānwǔ Jié",
        "translation": "Dragon Boat Festival",
        "slug": "dragon-boat-festival",
        "summary_text": "A summer solstice festival honoring poet Qu Yuan and warding off seasonal disease.",
        "rituals": "Zongzi (粽子), dragon boat races, hanging mugwort and calamus."
    },
    "七夕节": {
        "en_title": "Qīxī Jié",
        "translation": "Qixi Festival / Chinese Valentine's",
        "slug": "qixi-festival",
        "summary_text": "Celebrates the annual celestial reunion of the Weaver Girl and Cowherd stars.",
        "rituals": "Qiaoguo (巧果) pastries, stargazing, needlework skill tests."
    },
    "中元节": {
        "en_title": "Zhōngyuán Jié",
        "translation": "Ghost Festival",
        "slug": "ghost-festival",
        "summary_text": "A day devoted to honoring ancestors and guiding departed spirits with light.",
        "rituals": "Floating water lanterns, ancestral veneration, burning incense."
    },
    "中秋节": {
        "en_title": "Zhōngqiū Jié",
        "translation": "Mid-Autumn Festival",
        "slug": "mid-autumn-festival",
        "summary_text": "A harvest festival centered on lunar appreciation, harmony, and family gathering.",
        "rituals": "Mooncakes (月饼), moon gazing, osmanthus wine, tea pairings."
    },
    "重阳节": {
        "en_title": "Chóngyáng Jié",
        "translation": "Double Ninth Festival",
        "slug": "double-ninth-festival",
        "summary_text": "An autumn day dedicated to health, longevity, climbing mountains, and honoring elders.",
        "rituals": "Chongyang cake (重阳糕), chrysanthemum tea/wine, mountain walks."
    },
    "腊八节": {
        "en_title": "Làbā Jié",
        "translation": "Laba Festival",
        "slug": "laba-festival",
        "summary_text": "A traditional winter day marking the prelude to Chinese New Year preparations.",
        "rituals": "Laba porridge (腊八粥), pickling Laba green garlic."
    }
}

cal = Calendar()
cal.add('prodid', '-//Sinology Studio Living Calendar//sinologystudio.com//')
cal.add('version', '2.0')

for year in range(2026, 2028):
    start_date = date(year, 1, 1)
    end_date = date(year, 12, 31)
    current_ordinal = start_date.toordinal()
    
    while current_ordinal <= end_date.toordinal():
        d = date.fromordinal(current_ordinal)
        next_day = d + timedelta(days=1)
        
        solar = Solar.fromYmd(d.year, d.month, d.day)
        lunar = solar.getLunar()
        
        # 1. Solar Terms
        jieqi = lunar.getJieQi()
        if jieqi in SOLAR_TERMS_DATA:
            info = SOLAR_TERMS_DATA[jieqi]
            event = Event()
            
            event.add('summary', f"{info['translation']} ({jieqi})")
            event.add('dtstart', d)
            event.add('dtend', next_day)
            event.add('uid', f"solar-term-{year}-{info['slug']}@sinologystudio.com")
            
            article_url = f"{BASE_URL}/{info['slug']}/"
            desc = (
                f"{info['translation']} · {jieqi}\n\n"
                f"{info['summary_text']}\n\n"
                f"🌿 Seasonal Rituals: {info['rituals']}\n\n"
                f"📖 Read Full Seasonal Guide & Printable Postcard:\n"
                f"{article_url}"
            )
            event.add('description', desc)
            cal.add_component(event)
            
        # 2. Traditional Festivals
        festivals = lunar.getFestivals()
        for fest in festivals:
            if fest in FESTIVALS_DATA:
                info = FESTIVALS_DATA[fest]
                event = Event()
                
                event.add('summary', f"Festival: {info['translation']} ({fest})")
                event.add('dtstart', d)
                event.add('dtend', next_day)
                event.add('uid', f"festival-{year}-{info['slug']}@sinologystudio.com")
                
                article_url = f"{BASE_URL}/{info['slug']}/"
                desc = (
                    f"{info['translation']} · {fest}\n\n"
                    f"{info['summary_text']}\n\n"
                    f"🧧 Traditions & Foods: {info['rituals']}\n\n"
                    f"📖 Read Cultural Guide:\n"
                    f"{article_url}"
                )
                event.add('description', desc)
                cal.add_component(event)
            
        current_ordinal += 1

# Save directly to your Desktop directory
desktop_path = os.path.expanduser("~/Desktop")
output_file = os.path.join(desktop_path, "sinology_full_calendar.ics")

with open(output_file, "wb") as f:
    f.write(cal.to_ical())

print("Full calendar (Solar Terms + Festivals) successfully generated!")